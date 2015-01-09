#!/usr/bin/env python

import os
import re
import bs4
import json
import time
import config
import urllib
import requests
import soundcloud

soundcloud_client = soundcloud.Client(
    client_id=config.soundcloud_client_id,
    client_secret=config.soundcloud_client_secret,
    username=config.soundcloud_username,
    password=config.soundcloud_password
)

def main():
    graph = {'@context': 'http://schema.org/', '@graph': []}
    add_listen_content(graph)
    add_diy_content(graph)
    open('storycorps.json', 'w').write(json.dumps(graph, indent=2))

def add_listen_content(graph):
    offset = 0
    while True:
        time.sleep(1)
        results = get_listen_results(offset)
        i = 0
        while True:
            if str(i) in results:
                graph['@graph'].append(get_listen_item(results[str(i)]))
            else:
                break
            i += 1
            offset += 1
        if i == 0:
            break

def get_listen_results(offset):
    url = 'http://storycorps.org/wordpress/wp-admin/admin-ajax.php'
    data = {
        "action": "sc-load-more-stories",
        "offset": offset,
        "order": "DESC",
    }
    return requests.post(url, data).json()

def get_listen_item(d):
    i = {
        '@type': 'RadioClip',
        '@id': d['url'],
        'name': d['title'],
        'description': d['excerpt'].split('...', 1)[0],
        'contributor': [],
        'contentLocation': []
    }

    # get the mp3
    m = re.search('(http://.+?\.mp3)', d['shortcode'])
    if m:
        i['audio'] = m.group(1)

    # get the thumbnail
    m = re.search('(http://[^"]+?\.jpg)', d['shortcode'])
    if m:
        i['image'] = m.group(1)

    # contributors
    if 'facilitator' in d:
        i['contributor'].append(d['facilitator'])
    if 'producer' in d:
        i['contributor'].append(d['producer'])

    # org
    if 'partnership' in d:
        i['sourceOrganization'] = d['partnership']

    # locations
    if 'location' in d:
        for m in re.finditer(r'<a href="(.+?)">(.+?)</a>', d['location']):
            i['contentLocation'].append({
                '@type': 'Place',
                '@id': m.group(1),
                'name': m.group(2)
            })

    # get the topics
    i['about'] = []
    for t in re.findall('>([^>]+)<', d['topics']):
        slug = t.lower().replace(' ', '-')
        i['about'].append({
            "@type": "Thing",
            "@id": "http://storycorps.org/themes/" + slug,
            "name": t
        })
  
    # remove empty lists
    for k, v in i.items():
        if not v:
            i.pop(k)

    print i['@id']
    return i

def add_diy_content(graph):
    url = 'http://diy.storycorps.org/listen/page/%i/'
    i = 0
    while True:
        i += 1
        html = requests.get(url % i).content
        doc = bs4.BeautifulSoup(html)
        found = False
        for a in doc.select('div[class="ndl_share"] a'):
            found = True
            graph['@graph'].append(get_diy_item(a['href']))
        if not found:
            break

def get_diy_item(url):
    i = {
        '@type': 'RadioClip', 
        '@id': url, 
        'about': []
    }
    time.sleep(1)
    html = requests.get(url).content
    doc = bs4.BeautifulSoup(html)
    post = doc.select('div[class="post"]')[0]
    audio_url, creator = get_soundcloud_info(post.select('iframe')[0]['src'])
    if audio_url:
        i['audio'] = audio_url
    if creator:
        i['creator'] = creator
    i['name'] = post.select('h2')[0].text
    for a in post.select('div[class="single_text"] p a'):
        if '/locations/' in a['href']:
            if 'contentLocation' not in i:
                i['contentLocation'] = []
            i['contentLocation'].append({
                '@type': 'Place', 
                'url': a['href'], 
                'name': a.text
            })
        if '/tag/' in a['href']:
            i['about'].append({
                '@type': 'Thing',
                'url': a['href'],
                'name': a.text
            })
        if '/category/' in a['href']:
            i['about'].append({
                '@type': 'Thing',
                'url': a['href'],
                'name': a.text
            })
        if '/organizations/' in a['href']:
            if a.text != 'DIY':
                i['sourceOrganization'] = {
                    '@type': 'Organization',
                    'url': a['href'],
                    'name': a.text
                }

    print i['@id']
    return i

def get_soundcloud_info(iframe_url):
    track_id = re.search(r'%2F(\d+)&', iframe_url).group(1)
    try:
        track = soundcloud_client.get('/tracks/' + track_id)
        return track.permalink_url, track.user.username
    except:
        return None, None

if __name__ == "__main__":
    main()
