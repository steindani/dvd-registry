from flask import Flask, request, jsonify
from db.dbmanager import DBManager
from tmdb.tmdbhelper import TMDBHelper
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User

app = Flask( __name__ )

dbc = DBManager()
dbc.init_db()

tmdb = TMDBHelper()


# # DEBUG
medium = Medium( name = "Hello" )
person = Person( name = "John Doe" )
user = User( googleid = 12 )
genre = Genre( name = "Action" )
moviebase = MovieBase( title = "Bronze", cover = "http://waaa" )
movieextra = MovieExtra( year = 1923, plot = "BLALALALAAL", trailer = "http://woo" )

moviebase.tmdb_id = 1
moviebase.extra = movieextra

movieextra.genres.append( genre )
movieextra.cast.append( person )

dbc.add_movie( moviebase )

medium.user = user
dbc.add_medium( medium )

ownertrip = OwnershipTriplet( user, moviebase, medium )
dbc.add_ownertriplet( ownertrip )
# # DEBUG

@app.route( '/login', methods = ['POST'] )
def login():
    pass

@app.route( '/logout', methods = ['POST'] )
def logout():
    pass

@app.route( '/movies', methods = ['POST'] )
def add_medium():
    '''
    POST /movies 
    { 
       “name”: “The Fifth Element”, 
        “location”: “WD HDD”, 
    }
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
    '''
    fragment = str( request.json['fragment'] )
    result = tmdb.getFirstFiveResults( fragment )
    return jsonify( result )
    

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
    user = dbc.get_user_by_googleid( googleid )
    result = [{"movie_id": triple.movie.id, "title": triple.movie.title, "cover": triple.movie.cover} for triple in user.triplet]
    return jsonify( movies = result )

@app.route( '/movie/<int:movie_id>', methods = ['GET'] )
def get_movie( movie_id ):
    '''
    GET /movie/moveid [no JSON] 
    {  
        title: “movie title”, 
        year: “creation year”, 
        genders: [“action”, “adventure”], 
        actors: [“Will Smith”, “Anne Hathaway”], 
        plot: “plot in hungarian”, 
        trailer: “youtube URL”, poster_path: “poster URL”, 
        backdrop_path: “backdrop URL”, 
        medium: “iStore” 
    } 
    '''
    pass

@app.route( '/random', methods = ['GET'] )
def get_random_movie():
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
    pass

if __name__ == '__main__':
    app.run()
