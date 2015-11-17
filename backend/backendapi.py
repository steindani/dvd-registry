from datetime import datetime, timedelta
from db.dbmanager import DBManager
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
from flask import Flask, g, send_file, request, redirect, url_for, jsonify, abort
from functools import wraps
from jwt import DecodeError, ExpiredSignature
from urllib.parse import urlencode
import json
import jwt
import os
import requests

from flask_cors import CORS
from flask_cors import cross_origin
from tmdb.tmdbhelper import TMDBHelper

# Configuration

current_path = os.path.dirname( __file__ )
client_path = os.path.abspath( os.path.join( current_path, '..', '..', 'client' ) )

app = Flask( __name__ , static_url_path = '', static_folder = client_path )
app.config.from_object( 'config' )

cors = CORS( app, resources = {
    r"/helper/search": {
        "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
        "send_wildcard": True
        },
    
    r"/auth/google": {
        "origins": [{"localhost:9000"}, {"localhost:5000"}]
        }
    })

dbc = DBManager()
dbc.init_db()

tmdb = TMDBHelper()


# # TEST DATA
medium = Medium( name = "Hello" )
person = Person( name = "John Doe" )
user = User( googleid = 12 )
genre = Genre( name = "Action" )
moviebase = MovieBase( title = "Bronze", cover = "http://waaa" )
movieextra = MovieExtra( year = 1923, plot = "BLALALALAAL", trailer = "http://woo" )
# movieextra.last_access = datetime.now()

moviebase.extra = movieextra

movieextra.genres.append( genre )
movieextra.cast.append( person )

dbc.add_movie( moviebase )

medium.user = user
dbc.add_medium( medium )

ownertrip = OwnershipTriplet( user, moviebase, medium )
dbc.add_ownertriplet( ownertrip )

basetwo = MovieBase( title = "silver", cover = "http://silvertwo" )
basetwoextra = MovieExtra( year = 1928, plot = "BLOBLOBLOB", trailer = "http://wiasjdi" )
# basetwoextra.last_access = datetime.now()
basetwo.extra = basetwoextra
ownertriptwo = OwnershipTriplet( user, basetwo, medium )
dbc.add_ownertriplet( ownertriptwo )

user2 = User( googleid = 11 )
dbc.add_user( user2 )

# # TEST DATA

def create_result_from_movie( movie ):
    result = {}
    if movie is not None:
        result['title'] = movie.title
        result['year'] = movie.extra.year
        result['genres'] = [genre.name for genre in movie.extra.genres]
        result['actors'] = [actor.name for actor in movie.extra.cast]
        result['plot'] = movie.extra.plot
        result['trailer'] = movie.extra.trailer
        result['backdrop_path'] = movie.cover
        result['medium'] = movie.triplet.medium.name
        return jsonify( result )
    else: 
        abort( 400 )
    
def convert_movie_base_obj( movie_base ):
    return {"movie_id": movie_base.id, "title": movie_base.title, "cover": movie_base.cover} 


''' AUTHENTICATION '''

def create_token( user ):
    payload = {
        'sub': user.googleid,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta( days = 14 )
    }
    token = jwt.encode( payload, app.config['TOKEN_SECRET'] )
    return token.decode( 'unicode_escape' )


def parse_token( req ):
    token = req.headers.get( 'Authorization' ).split()[1]
    return jwt.decode( token, app.config['TOKEN_SECRET'] )


def login_required( f ):
    @wraps( f )
    def decorated_function( *args, **kwargs ):
        if not request.headers.get( 'Authorization' ):
            response = jsonify( message = 'Missing authorization header' )
            response.status_code = 401
            return response

        try:
            payload = parse_token( request )
        except DecodeError:
            response = jsonify( message = 'Token is invalid' )
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify( message = 'Token has expired' )
            response.status_code = 401
            return response

        g.googleid = payload['sub']

        return f( *args, **kwargs )

    return decorated_function

@app.route( '/movies', methods = ['POST'] )
def add_movie():
    '''
    POST /movies 
    { 
       “name”: “The Fifth Element”, 
        “location”: “WD HDD”
    }
    
    TODO authentikacio, hogy a user be van-e jelentkezve
    TODO hibakezeles
    '''
    pass

@app.route( '/helper/search', methods = ['POST'] )
@cross_origin(supports_credentials = True)
@login_required
def search_tmdb():
    '''
    GET /helper/search 
    { 
        “fragment”: “The Fif” 
    }
    
    { 
        “possible_titles”: [ 
            “The Fifth Element”, 
            “The Fifth Commandment” ], 
        “first_result”:  { 
            "original_title": "The Fifth Element", 
            "overview": "It’s the year 2257 and a taxi driver has been unintentionally given 
            the task of saving a young girl who is part of the key that will ensure the survival of 
            humanity. The Fifth Element takes place in a futuristic metropolitan city and is filmed 
            in a French comic book aesthetic by a British, French and American lineup.", 
            "poster_path": 
            "https://image.tmdb.org/t/p/w185/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg", 
        } 
    } 
    
    TODO ezt kiszedni, hogy ne legyen publikus!
    '''
    result = {}
    try:
        if request.json is None:
            raise KeyError()
        fragment = str( request.json['fragment'] )
        result = tmdb.getFirstFiveResults( fragment )
    except KeyError:
        pass
    if result == {}:
        abort( 400 )
    else:
        return jsonify( result )
    
    
@app.route( '/media', methods = ['GET'] )
@login_required
def get_media():
    '''
    GET /media 
    { 
        "media": [
            "WD HDD",
            "BlueRay",
            "Kiscica pendrive"
        ]
    }
    '''
    googleid = g.googleid
    user = dbc.get_user_with_media_by_googleid( googleid )
    
    media = []
    if user is not None:
        media = [medium.name for medium in user.media]
        return jsonify( media = media )
    else:
        abort( 400 )
        

@app.route( '/medium', methods = ['POST'] )
@login_required
def add_medium():
    '''
    POST / medium
    { 
        "location": "Kiscica pendrive"
    }
    '''
    googleid = g.googleid
    try:
        if request.json is None:
            raise KeyError()
        location = str( request.json['location'] )
        is_ok = dbc.add_medium_to_user( location, googleid )
        if is_ok:
            return jsonify( {} )
        else:
            abort( 400 )
    except KeyError:
        abort( 400 )


@app.route( '/movies', methods = ['GET'] )
@login_required
def get_movies():
    '''
    GET /movies 
    { 
        “movies”: [ 
            { 
            movie_id: 42 
            title: “movie title”, 
            cover: “cover URL / cover itself”, 
            } 
        ] 
    } 
    '''
    googleid = g.googleid
    
    user = dbc.get_movie_bases_by_googleid( googleid )
    
    if user is not None:
        movie_bases = [convert_movie_base_obj( triple.movie ) for triple in user.triplet]
        return jsonify( movies = movie_bases )
    else:
        abort( 400 )
    

@app.route( '/movie/<int:movie_id>', methods = ['GET'] )
@login_required
def get_movie( movie_id ):
    '''
    GET /movie/moveid [no JSON] 
    {  
        title: “movie title”, 
        year: “creation year”, 
        genres: [“action”, “adventure”], 
        actors: [“Will Smith”, “Anne Hathaway”], 
        plot: “plot in hungarian”, 
        trailer: “youtube URL”, poster_path: “poster URL”, 
        backdrop_path: “backdrop URL”, 
        medium: “iStore” 
    } 
    '''
    googleid = g.googleid
        
    movie = dbc.get_movie_by_id_and_by_googleid( movie_id, googleid )
    return create_result_from_movie( movie )
    

@app.route( '/random', methods = ['GET'] )
@login_required
def get_random_movies():
    '''
    GET /random [no JSON] 
    {  
    “movies”: [ 
            { 
            movie_id: 42 
            title: “movie title”, 
            cover: “cover URL / cover itself”, 
            } 
        ] 
     } 
    '''
    googleid = g.googleid
    
    movie_bases_list = dbc.get_movie_bases_not_seen_in_last_time_by_googleid( googleid )

    if movie_bases_list is not None:
        movie_bases_result = [convert_movie_base_obj( movie_base ) for movie_base in movie_bases_list]
        return jsonify( movies = movie_bases_result )
    else:
        abort( 400 )
        

@app.route( '/random/one', methods = ['GET'] )
@login_required
def get_random_movie():
    '''
    GET /random [no JSON] 
    {   
        title: “movie title”, 
        year: “creation year”, 
        genres: [“action”, “adventure”], 
        actors: [“Will Smith”, “Anne Hathaway”], 
        plot: “plot in hungarian”, 
        trailer: “youtube URL”, poster_path: “poster URL”, 
        backdrop_path: “backdrop URL”, 
        medium: “iStore” 
    } 
    '''
    googleid = g.googleid
    
    movie = dbc.get_movie_not_seen_in_last_time_by_googleid( googleid )
    return create_result_from_movie( movie )


@app.route( '/auth/google', methods = ['POST'] )
@cross_origin(supports_credentials = True)
def google_authentication():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict( client_id = request.json['clientId'],
                   redirect_uri = request.json['redirectUri'],
                   client_secret = app.config['GOOGLE_SECRET'],
                   code = request.json['code'],
                   grant_type = 'authorization_code' )

    # Step 1. Exchange authorization code for access token.
    r = requests.post( access_token_url, data = payload )
    token = json.loads( r.text )
    headers = {'Authorization': 'Bearer {0}'.format( token['access_token'] )}

    # Step 2. Retrieve information about the current user.
    r = requests.get( people_api_url, headers = headers )
    profile = json.loads( r.text )

    user = dbc.get_user_only_by_googleid( profile['sub'] )
    token = None
    if user:
        token = create_token( user )
    else:
        newuser = User( googleid = profile['sub'] )
        dbc.add_user( newuser )
        token = create_token( newuser )
    return jsonify( token = token )


if __name__ == '__main__':
    app.run( debug = False )
