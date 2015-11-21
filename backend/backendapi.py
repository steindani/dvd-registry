from auth.authentication import create_token, parse_token, login_required
from db.dbmanager import DBManager
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.user import User
from db.entityhelper import EntityFactory, EntityConnector, EntityConverter
from flask import Flask, g, url_for, send_file, request, jsonify, abort
from flask_cors import cross_origin
import config.configuration
import json
import requests

from tmdb.tmdbhelper import TMDBHelper


config.configuration.init( __file__, __name__ )
app = config.configuration.app

dbc = DBManager()
dbc.init_db()

tmdb = TMDBHelper()

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
    
    {
        movie_id: 42 
        title: “movie title”, 
        cover: “cover URL”,
        year: 1978
    }
    '''
    req = request.json
    if ( not req ) or ( 'media' not in req ) or ( ( 'title' not in req ) and ( 'id' not in req ) ):
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
            movie = tmdb.get_movie_by_id( tmdb_id )
            if movie == {}:
                abort( 400 )
            else:
                db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )        
        except ValueError:
            if 'title' in req:
                tmdb_title = str( req['title'] )
                movie = tmdb.get_movie_by_title( tmdb_title )
                if movie == {}:
                    abort( 400 )
                else:
                    db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )                      
            else:
                abort( 400 )
    elif 'title' in req:
        tmdb_title = str( req['title'] )
        movie = tmdb.get_movie_by_title( tmdb_title )
        if movie == {}:
            abort( 400 )
        else:
            db_movie = EntityFactory.create_movie( title = movie['title'], cover_small = movie['poster_path'], cover_large = movie['poster_original_path'], year = movie['year'], plot = movie['plot'], trailer = movie['trailer'], cast = movie['cast'], genres = movie['genres'] )            
    else:
        abort( 400 )
        
    ot = EntityConnector.connect_user_with_movie_and_medium( user = user, medium = medium, movie = db_movie )
    dbc.add_ownertriplet_exists_check( ot )
    
    ownertrip = dbc.get_ownertrip_by_year_title_googleid( googleid, movie['year'], movie['title'] )
    return jsonify( EntityConverter.convert_movie_base_to_return_format( ownertrip.movie ) )


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
    
    req = request.json
    if ( not req ) or ( 'fragment' not in req ):
        abort( 400 )
    
    result = {}
    fragment = str( req['fragment'] )
        
    if ( '(' in fragment ) and ( ')' in fragment ):
        opening_index = fragment.find( '(' )
        closing_index = fragment.find( ')' )
        if( opening_index > closing_index ):
            # parenthesis are in incorrect order
            result = tmdb.get_first_five_results( fragment )
        else:
            subs = fragment[opening_index + 1:closing_index]
            if ( '(' in subs ) or ( ')' in subs ):
                # there are more parenthesis nested in each other
                result = tmdb.get_first_five_results( fragment )
            else:
                try:
                    year = int( subs )
                    if( len( fragment[closing_index + 1:].strip() ) > 0 ):
                        # there is something after the year parenthesis
                        result = tmdb.get_first_five_results( fragment )    
                    else:
                        result = tmdb.get_first_five_results( title_fragment = fragment[:opening_index], year = year )
                except ValueError:
                    result = tmdb.get_first_five_results( fragment )
    else:
        result = tmdb.get_first_five_results( fragment )
    
    return jsonify( result )
    
    
@app.route( '/search/movies', methods = ['POST'] )
@cross_origin( supports_credentials = True )
@login_required
def search_movies():
    ''' 
    POST /search/movies 
    { 
        criteria: "query"
    }
    
    {
        movies: [ 1,2,3,4,5,28]
    }
    '''
    
    req = request.json
    if ( not req ) or ( 'criteria' not in req ):
        abort( 400 )

    googleid = g.googleid
    criteria = str( req['criteria'] ).strip()
    
    movies_id = []
    criteria_parts = criteria.split( ' ' )
    
    for criteria_part in criteria_parts:
        criteria_part = criteria_part.strip()
        if len( criteria_part ) > 0:
            ownertrip = dbc.get_ownertriplet_by_googleid_and_criteria( googleid, criteria_part )
            if ownertrip is not None:
                if ownertrip.movie.extra.id not in movies_id:
                    movies_id.append( ownertrip.movie.extra.id )
    
    return jsonify( movies = movies_id )
    
    
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
                cover: “cover URL”,
                year: 1978 
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
        movie_id: 42 
        title: “movie title”, 
        cover: “cover URL”,
        year: 1978 
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
