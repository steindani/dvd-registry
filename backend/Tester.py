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
from db.entities.OwnershipTriplet import OwnershipTriplet


dbc = DBManager()
dbc.init_db()

medium = Medium( name = "Hello" )
person = Person( name = "John Doe" )
user = User( googleid = 12 )
genre = Genre( name = "Action" )
movie = Movie( title = "Bronze", year = 1923, plot = "BLALALALAAL", trailer = "http://woo", poster = "http://waaa" )

membership = OwnershipTriplet( user, movie, medium )

movie.genre.append( genre )
movie.cast.append( person )

dbc.add_movie( movie )
dbc.add_ownertriplet( membership )

print( "addeddDONE" )

ownersh = dbc.get_ownertriplet()

print( ownersh[0].user.googleid )
print( ownersh[0].medium.name )
print( ownersh[0].movie.title )
print( ownersh[0].movie.year )
print( ownersh[0].movie.plot )
print( ownersh[0].movie.trailer )
print( ownersh[0].movie.poster )
print( ownersh[0].movie.genre[0].name )
print( ownersh[0].movie.cast[0].name )

# res = dbc.get_movie_by_title( "Bronze" )
# print( "hello" )
# for mooovie in res:
#    print( mooovie.year )
#    #print( mooovie.media.name )
#    print( mooovie.genre[0].name )
#    print( mooovie.cast[0].name )
    # print( mooovie.users[0].googleid )
