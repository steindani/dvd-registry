'''
@author: benjo
'''
from db.DBManager import DBManager
from db.entities.Base import Base
from db.entities.Genre import Genre
from db.entities.Medium import Medium
from db.entities.Movie import MovieBase, MovieExtra
from db.entities.OwnershipTriplet import OwnershipTriplet
from db.entities.Person import Person
from db.entities.User import User


dbc = DBManager()
dbc.init_db()

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

print( dbc.get_users()[0].googleid )
print( dbc.get_user_by_googleid( 12 ).id )

m = dbc.get_movie_by_id( 1 )

print( m.title )
print( m.extra.genres[0].name )
print( m.extra.cast[0].name )


''' TODO: eager loading helyett megcsinalni,hogy querykre legyen csak eager loading, hogy amikor a usert keressuk, akkor ne szedje le az egesz adatbazist! 
AZAZ: lazy = 'joined' helyett lazy  = 'dynamic' - et irni a relationshipnel
 '''
