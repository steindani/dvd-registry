from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
from flask import jsonify, abort

class EntityFactory( object ):
    
    @staticmethod
    def create_movie( title, cover_small, cover_large, year, plot, trailer, cast, genres ):
        moviebase = MovieBase( title = title, cover_small = cover_small )
        movieextra = MovieExtra( cover_large = cover_large, year = year, plot = plot, trailer = trailer )
        moviebase.extra = movieextra
        
        for genre_name in genres:
            genre = EntityFactory.create_genre( genre_name )
            movieextra.genres.append( genre )
        for actor_name in cast:
            actor = EntityFactory.create_cast( actor_name )
            movieextra.cast.append( actor )
        
        return moviebase
        
    @staticmethod
    def create_cast( name ):
        return Person( name = name )
    
    @staticmethod
    def create_genre( name ):
        return Genre( name = name )
    
    
class EntityConnector( object ):
    @staticmethod
    def connect_user_with_movie_and_medium( user, movie, medium ):
        return OwnershipTriplet( user = user, movie = movie, medium = medium )


class EntityConverter( object ):
    @staticmethod
    def convert_movie_to_json( movie ):
        result = {}
        if movie is not None:
            result['title'] = movie.title
            result['year'] = movie.extra.year
            result['genres'] = [genre.name for genre in movie.extra.genres]
            result['actors'] = [actor.name for actor in movie.extra.cast]
            result['plot'] = movie.extra.plot
            result['trailer'] = movie.extra.trailer
            result['backdrop_path'] = movie.extra.cover_large
            result['medium'] = movie.triplet.medium.name
            return jsonify( result )
        else: 
            abort( 400 )
            
    @staticmethod
    def convert_movie_base_to_return_format( movie_base ):
        return {"movie_id": movie_base.extra.id, "title": movie_base.title, "cover": movie_base.cover_small, "year": movie_base.extra.year }
