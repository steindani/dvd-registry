'''
@author: benjo
'''
from db.DBManager import DBManager
from db.entities.Base import Base
from db.entities.Genre import Genre
from db.entities.Medium import Medium
from db.entities.Movie import Movie
from db.entities.Person import Person
from db.entities.User import User


dbc = DBManager()
dbc.init_db()

medium = Medium( name = "Hello" )
person = Person( name = "John Doe" )
user = User( googleid = 12 )
genre = Genre( name = "Action" )
movie = Movie( title = "Bronze", year = 1923, plot = "BLALALALAAL", trailer = "http://woo", poster = "http://waaa" )

user.media.append( medium )
medium.movies.append( movie )
movie.genre.append( genre )
movie.cast.append( person )
user.movies.append( movie )

dbc.add_movie( movie )

print("addedd")

res = dbc.get_movie_by_title("Bronze")
print("hello")
for mooovie in res:
    print( mooovie.year )
    print( mooovie.media.name )
    print( mooovie.genre[0].name )
    print( mooovie.cast[0].name )
    print( mooovie.users[0].googleid )