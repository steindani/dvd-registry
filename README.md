# DVD-registry

It is a DVD registry which stores the user's home DVD movies. Its features include: 

 * Google Single Sign-On authentication
 * Fetch movie data from The Movie Database (TMDb - themoviedb.org)
 * Fetch movie trailer from YouTube
 * Translate plot to Hungarian via Yandex
 * List stored movies
 * Order movies by year, title
 * View the movie details
 * Random movie recommendation 

This was a homework task for Software Architecture course at Budapest University of Technology and Economics in year 2015.

Slideshow: http://www.slideshare.net/steindani/otthoni-dvd-nyilvntart-rendszer

Future work:

* SSL integration
* Translate GUI to English

**Pull requests are warmly welcome!**


## Technical instructions

### Used technologies

* Floating Action Button https://www.google.com/design/spec/components/buttons-floating-action-button.html
* AngularJS: https://angularjs.org/ 
* Satellizer: https://github.com/sahat/satellizer
* JWT: http://jwt.io/
* tmdbsimple: https://github.com/celiao/tmdbsimple
* google-api-python-client: https://github.com/google/google-api-python-client 
* SQLAlchemy: http://www.sqlalchemy.org/
* Flask: http://flask.pocoo.org/
* flask-cors: https://pypi.python.org/pypi/Flask-Cors/
* Yandex Translate API: https://tech.yandex.com/translate/
* YouTube API: https://developers.google.com/youtube/v3/getting-started
* TMDB API: https://www.themoviedb.org/documentation/api
* requests: http://docs.python-requests.org/en/latest/

### Installation instructions

Tested on Ubuntu 14.04.3 LTS.
Dependency versions are as of 25.12.2015.

Get latest release of the dependencies:
`sudo apt-get update`

#### Frontend:
Install npm, bower and git:
* `sudo apt-get install npm git`
* `sudo npm install -g bower`

Install ruby-compass:
* `sudo apt-get install rubygems1.9 ruby-dev`
* `sudo gem install rubygems-update`
* `sudo update_rubygems`
* `sudo gem install compass`

Clone repository:
* `git clone https://github.com/steindani/dvd-registry`
* `cd dvd-registry/frontend`

Install dependencies in Bowerfile.json:
`bower install`

*******************************************************
IF */usr/bin/env: node: No such file or directory error* 

THEN `sudo ln -s /usr/bin/nodejs /usr/bin/node`
*******************************************************
*May bower anonymously report usage satistics to improve the tool over time?* **n**
*******************************************************

Install dependencies in package.json:
* `sudo npm install`
* `sudo npm install -g grunt-cli`


#### Backend
Install Python 3 and pip: `sudo apt-get install python3 python3-pip`

Install Python modules via pip: `sudo pip3 install flask sqlalchemy tmdbsimple flask-cors jinja2 markupsafe werkzeug itsdangerous pyjwt requests requests-oauthlib google-api-python-client`

### Deployment instructions

#### Frontend
* `cd dvd-registry/frontend`
* `grunt serve --force`

#### Backend (in a separate command-line than the frontend):
* `cd dvd-registry/backend`
* `python3 backendapi.py`

The website is available at http://localhost:9000
