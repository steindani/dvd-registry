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
basetwo.extra = basetwoextra
ownertriptwo = OwnershipTriplet( user, basetwo, medium )
dbc.add_ownertriplet( ownertriptwo )


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
    
    TODO authentikacio, hogy a user be van-e jelentkezve
    TODO hibakezeles
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
    
    TODO authentikacio, hogy a user be van-e jelentkezve
    TODO hibakezeles
    '''
    
    googleid = str( request.cookies.get( 'googleid' ) )
    
    user = dbc.get_movie_bases_by_googleid( googleid )
    movie_bases = [{"movie_id": triple.movie.id, "title": triple.movie.title, "cover": triple.movie.cover} for triple in user.triplet]
    
    return jsonify( movies = movie_bases )

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
    
    TODO authentikacio, hogy a user be van-e jelentkezve
    TODO hibakezeles
    
    TODO frissíteni, hogy a movie extrát mikor kérték le, ezt átvezetni az adatbázisba, létrehozni egy új oszlopot neki.
    '''
    
    googleid = str( request.cookies.get( 'googleid' ) )
    movie = dbc.get_movie_by_id_and_by_googleid( movie_id, googleid )
    
    result = {}
    if not ( movie is None ):
        result['title'] = movie.title
        result['year'] = movie.extra.year
        result['genres'] = [genre.name for genre in movie.extra.genres]
        result['actors'] = [actor.name for actor in movie.extra.cast]
        result['plot'] = movie.extra.plot
        result['trailer'] = movie.extra.trailer
        result['backdrop_path'] = movie.cover
        result['medium'] = movie.triplet.medium.name
    
    return jsonify( result )

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
    
    TODO authentikacio, hogy a user be van-e jelentkezve
    TODO hibakezeles
    '''
    pass

if __name__ == '__main__':
    app.run()
