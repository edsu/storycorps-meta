# storycorps-meta

[StoryCorps](http://storycorps.org) has collected over 50,000 interviews
with over 90,000 Americans. It is one of the largest oral history projects
of its kind. A small portion of the interviews are available 
[on the Web](http://storycorps.org/listen) and the entire archive is held by 
the [American Folklife Center](http://www.loc.gov/folklife/) at the 
[Library of Congress](http://loc.gov).

This is a simple program that calls the REST API that serves up their
[listen](http://storycorps.org/listen) view, and saves the data as 
[JSON-LD](http://www.w3.org/TR/json-ld/) using the
[schema.org](http://schema.org) vocabulary. It also walks the stories that
have been uploaded to their [DIY](http://diy.storycorps.org/) service, which
hosts audio on [SoundCloud](http://soundcloud.com). 

Here's an example of the json-ld for an interview:

```javascript
    {
      "@id": "http://storycorps.org/listen/alton-yates-and-toni-yates/", 
      "@type": "RadioClip", 
      "name": "Alton Yates and Toni Yates"
      "description": "Alton Yates tells his daughter, Toni, about being part of a small group of Air...",
      "audio": "http://cdn.storycorps.org/wordpress/wp-content/uploads/yatesweb.mp3", 
      "image": "http://cdn.storycorps.org/wordpress/wp-content/uploads/yatesa3.jpg", 
      "about": [
        {
          "@id": "http://storycorps.org/themes/family", 
          "@type": "Thing", 
          "name": "Family"
        }, 
        {
          "@id": "http://storycorps.org/themes/griot", 
          "@type": "Thing", 
          "name": "Griot"
        }, 
        {
          "@id": "http://storycorps.org/themes/growing-up", 
          "@type": "Thing", 
          "name": "Growing Up"
        }, 
        {
          "@id": "http://storycorps.org/themes/military", 
          "@type": "Thing", 
          "name": "Military"
        }, 
        {
          "@id": "http://storycorps.org/themes/work", 
          "@type": "Thing", 
          "name": "Work"
        }
      ], 
    } 
```

## Run

    brew install pyenv-virtualenvwrapper
    mkvirtualenv storycorps-meta
    git clone http://github.com/edsu/storycorps-meta
    cd storycorps-meta
    pip install -r requirements.txt
    cp config.py.template config.py # and add soundcloud credentials
    ./storycorps.py
    cat storycorps.json

## License

* I'm not sure what the license is associated with this content. If you can
  figure it out please let me know!

