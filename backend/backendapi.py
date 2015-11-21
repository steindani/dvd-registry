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
from db.entityhelper import EntityFactory, EntityConnector, EntityConverter

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
        
    r"/media": {
        "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
        "send_wildcard": True
        },
        
    r"/movies": {
        "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
        "send_wildcard": True
        },
        
    r"/random": {
        "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
        "send_wildcard": True
        },
        
    r"/random/one": {
        "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
        "send_wildcard": True
        },
    
    r"/auth/google": {
        "origins": [{"localhost:9000"}, {"localhost:5000"}]
        }
    } )

dbc = DBManager()
dbc.init_db()

tmdb = TMDBHelper()

# # TEST DATA
user2 = User( googleid = 11 )
dbc.add_user( user2 )
# # TEST DATA

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
@cross_origin( supports_credentials = True )
@login_required
def add_movie():
    '''
    POST /movies 
    { 
       “title”: “The Fifth Element”, 
       "id": 42,
       “media”: “WD HDD”
    }
    
    '''
    req = request.json
    if ( not req ) or ( 'media' not in request.json ) or ( ( 'title' not in req ) and ( 'id' not in req ) ):
        abort( 400 )
        
    googleid = g.googleid
        
    media_name = str( req['media'] )
    media_name = media_name.strip()
    
    if len( media_name ) == 0:
        abort( 400 )
    
    user = dbc.get_user_only_by_googleid( googleid )
    medium = dbc.add_medium_to_user( media_name, googleid )
        
    if 'id' in req:
        try:
            tmdb_id = int( req['id'] )
            movie = tmdb.getMovieByID( tmdb_id )
            if movie == {}:
                abort( 400 )
            else:
                db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )        
        except ValueError:
            if 'title' in req:
                tmdb_title = str( req['title'] )
                movie = tmdb.getMovieByTitle( tmdb_title )
                if movie == {}:
                    abort( 400 )
                else:
                    db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )                      
            else:
                abort( 400 )
    elif 'title' in req:
        tmdb_title = str( req['title'] )
        movie = tmdb.getMovieByTitle( tmdb_title )
        if movie == {}:
            abort( 400 )
        else:
            db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )            
    else:
        abort( 400 )
        
    ot = EntityConnector.connect_user_with_movie_and_medium( user = user, medium = medium, movie = db_movie )
    dbc.add_ownertriplet_exists_check( ot )
        
    return jsonify( {} )           


@app.route( '/helper/search', methods = ['POST'] )
@cross_origin( supports_credentials = True )
@login_required
def search_tmdb():
    '''
    POST /helper/search 
    { 
        “fragment”: “The Fif” 
    }
    
    { 
        "results": [
            {
              "id": 18,
              "title": "Az \u00f6t\u00f6dik elem"
            },
            {
              "id": 162903,
              "title": "A WikiLeaks-botr\u00e1ny"
            },
            {
              "id": 14075,
              "title": "The Fifth Commandment"
            },
            {
              "id": 231735,
              "title": "The Dandy Fifth"
            },
            {
              "id": 54415,
              "title": "Sinbad: The Fifth Voyage"
            }
        ],
        “first_result”:  { 
            "title": "Az \u00f6t\u00f6dik elem", 
            "overview": "It’s the year 2257 and a taxi driver has been unintentionally given 
            the task of saving a young girl who is part of the key that will ensure the survival of 
            humanity. The Fifth Element takes place in a futuristic metropolitan city and is filmed 
            in a French comic book aesthetic by a British, French and American lineup.", 
            "poster_path": "https://image.tmdb.org/t/p/w185/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg", 
        } 
    } 
    '''
    result = {}
    try:
        if request.json is None:
            raise KeyError()
        fragment = str( request.json['fragment'] )
        
        if ( '(' in fragment ) and ( ')' in fragment ):
            opening_index = fragment.find( '(' )
            closing_index = fragment.find( ')' )
            if( opening_index > closing_index ):
                # parenthesis are in incorrect order
                result = tmdb.getFirstFiveResults( fragment )
            else:
                subs = fragment[opening_index + 1:closing_index]
                if ( '(' in subs ) or ( ')' in subs ):
                     # there are more parenthesis nested in each other
                    result = tmdb.getFirstFiveResults( fragment )
                else:
                    try:
                        year = int( subs )
                        if( len( fragment[closing_index + 1:].strip() ) > 0 ):
                            # there is something after the year parenthesis
                            result = tmdb.getFirstFiveResults( fragment )    
                        else:
                            result = tmdb.getFirstFiveResults( title_fragment = fragment[:opening_index], year = year )
                    except ValueError:
                        result = tmdb.getFirstFiveResults( fragment )
        else:
            result = tmdb.getFirstFiveResults( fragment )
    except KeyError:
        pass
    if result == {}:
        abort( 400 )
    else:
        return jsonify( result )
    
    
@app.route( '/media', methods = ['GET'] )
@cross_origin( supports_credentials = True )
@login_required
def get_media():
    '''
    GET /media [no JSON]
    { 
        "media": [
            "WD HDD",
            "BlueRay"
        ]
    }
    '''
    googleid = g.googleid
    user = dbc.get_user_with_media_by_googleid( googleid )
    
    media = []
    if user is not None:
        media = [medium.name for medium in user.media]
    return jsonify( media = media )
        

@app.route( '/movies', methods = ['GET'] )
@cross_origin( supports_credentials = True )
@login_required
def get_movies():
    '''
    GET /movies [no JSON] 
    { 
        “movies”: [ 
            { 
            movie_id: 42 
            title: “movie title”, 
            cover: “cover URL” 
            } 
        ] 
    } 
    '''
    googleid = g.googleid
    
    user = dbc.get_movie_bases_by_googleid( googleid )
    if user is not None:
        movie_bases = [EntityConverter.convert_movie_base_to_return_format( triple.movie ) for triple in user.triplet]
        return jsonify( movies = movie_bases )
    else:
        return jsonify( movies = [] )
    

@app.route( '/movie/<int:movie_id>', methods = ['GET'] )
@cross_origin( supports_credentials = True )
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
    return EntityConverter.convert_movie_to_json( movie )
    

@app.route( '/random', methods = ['GET'] )
@cross_origin( supports_credentials = True )
@login_required
def get_random_movies():
    '''
    GET /random [no JSON] 
    {  
    “movies”: [ 
            { 
            movie_id: 42 
            title: “movie title”, 
            cover: “cover URL”, 
            } 
        ] 
     } 
    '''
    googleid = g.googleid
    
    movie_bases_list = dbc.get_movie_bases_not_seen_in_last_time_by_googleid( googleid )

    if movie_bases_list is not None:
        movie_bases_result = [EntityConverter.convert_movie_base_to_return_format( movie_base ) for movie_base in movie_bases_list]
        return jsonify( movies = movie_bases_result )
    else:
        return jsonify( movies = [] )
        

@app.route( '/random/one', methods = ['GET'] )
@cross_origin( supports_credentials = True )
@login_required
def get_random_movie():
    '''
    GET /random [no JSON] 
     { 
        movie_id: 42 
        title: “movie title”, 
        cover: “cover URL”, 
    } 
    '''
    
    googleid = g.googleid
    
    movie = dbc.get_movie_not_seen_in_last_time_by_googleid( googleid )
    
    if movie is not None:
        return jsonify( EntityConverter.convert_movie_base_to_return_format( movie ) )
    else:
        return jsonify( {} )


@app.route( '/auth/google', methods = ['POST'] )
@cross_origin( supports_credentials = True )
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
    app.run( debug = False, threaded = False )
