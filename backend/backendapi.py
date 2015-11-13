from datetime import datetime
from db.dbmanager import DBManager
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
from flask import Flask, request, jsonify, abort

from flask.ext.cors import CORS
from tmdb.tmdbhelper import TMDBHelper


app = Flask( __name__ )
CORS( app )

dbc = DBManager()
dbc.init_db()

tmdb = TMDBHelper()


# # TEST DATA
medium = Medium( name = "Hello" )
person = Person( name = "John Doe" )
user = User( googleid = 12 )
user.login_time = datetime.now()
user.logout_time = datetime.now()
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
user2.login_time = datetime.now()
user2.logout_time = datetime.now()
dbc.add_user( user2 )

# # TEST DATA

''' Aborts if either googleid is None, or user is not logged in yet.'''
def authenticate_user( googleid ):
    if googleid == 'None':
        abort( 403 )
    user_is_logged_in = dbc.is_user_logged_in( googleid )
    if not user_is_logged_in:
        abort( 403 )
    
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


@app.route( '/login', methods = ['POST'] )
def login():
    googleid = str( request.cookies.get( 'googleid' ) )
    if googleid == 'None':  
        abort( 403 )
    
    is_user_logged_in = dbc.is_user_logged_in( googleid )
    if is_user_logged_in:
        return jsonify()
    else:
        last_login = dbc.get_user_login_time( googleid )
        last_logout = dbc.get_user_logout_time( googleid )
          
        if ( last_login is None ) or ( last_logout is None ):
            abort( 403 )
        
        now = datetime.now()
        is_later = ( last_login < last_logout ) and ( now > last_logout ) 
        if is_later:
            dbc.update_user_login_time( googleid )
            return jsonify()
        else:
            abort( 403 )
    

@app.route( '/logout', methods = ['POST'] )
def logout():
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
    dbc.update_user_logout_time( googleid )
    return jsonify()
    
    
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
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
    
    user = dbc.get_user_with_media_by_googleid( googleid )
    
    media = []
    if user is not None:
        media = [medium.name for medium in user.media]
        return jsonify( media = media )
    else:
        abort( 400 )
        

@app.route( '/medium', methods = ['POST'] )
def add_medium():
    '''
    POST / medium
    { 
        "location": "Kiscica pendrive"
    }
    '''
    
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
    
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
    
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
        
    user = dbc.get_movie_bases_by_googleid( googleid )
    
    if user is not None:
        movie_bases = [convert_movie_base_obj( triple.movie ) for triple in user.triplet]
        return jsonify( movies = movie_bases )
    else:
        abort( 400 )
    

@app.route( '/movie/<int:movie_id>', methods = ['GET'] )
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
    
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
        
    movie = dbc.get_movie_by_id_and_by_googleid( movie_id, googleid )
    return create_result_from_movie( movie )
    

@app.route( '/random', methods = ['GET'] )
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
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
    
    movie_bases_list = dbc.get_movie_bases_not_seen_in_last_time_by_googleid( googleid )

    if movie_bases_list is not None:
        movie_bases_result = [convert_movie_base_obj( movie_base ) for movie_base in movie_bases_list]
        return jsonify( movies = movie_bases_result )
    else:
        abort( 400 )
        

@app.route( '/random/one', methods = ['GET'] )
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
    googleid = str( request.cookies.get( 'googleid' ) )
    authenticate_user( googleid )
    
    movie = dbc.get_movie_not_seen_in_last_time_by_googleid( googleid )
    return create_result_from_movie( movie )

if __name__ == '__main__':
    app.run( debug = False )
