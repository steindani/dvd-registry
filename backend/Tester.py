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

movie.genre.append( genre )
movie.cast.append( person )

dbc.add_movie( movie )

medium.user = user
dbc.add_medium( medium )

ownertrip = OwnershipTriplet( user, movie, medium )
dbc.add_ownertriplet( ownertrip )

print( dbc.get_user_by_googleid( 12 ).id )
print( dbc.get_medium_by_userid( user.id ) )

''' TODO: eager loading helyett megcsinalni,hogy querykre legyen csak eager loading, hogy amikor a usert keressuk, akkor ne szedje le az egesz adatbazist! 
AZAZ: lazy = 'joined' helyett lazy  = 'dynamic' - et irni a relationshipnel
 '''

# ownersh = dbc.get_ownertriplet()

# print( ownersh[0].user.googleid )
#===============================================================================
# print( ownersh[0].medium.name )
# print( ownersh[0].movie.title )
# print( ownersh[0].movie.year )
# print( ownersh[0].movie.plot )
# print( ownersh[0].movie.trailer )
# print( ownersh[0].movie.poster )
# print( ownersh[0].movie.genre[0].name )
# print( ownersh[0].movie.cast[0].name )
# 
# moovie = dbc.get_movies()
# 
# print( moovie[0].title )
# print( moovie[0].triplet.user.googleid )
#===============================================================================

