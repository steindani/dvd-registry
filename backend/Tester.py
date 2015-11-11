'''
@author: benjo
'''
from db.dbmanager import DBManager
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User


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

medium2 = Medium( name = "World" )
medium2.user = user

dbc.add_medium( medium2 )

ownertrip = OwnershipTriplet( user, moviebase, medium )
dbc.add_ownertriplet( ownertrip )

user2 = User( googleid = 11 )

basetwo = MovieBase( title = "silver", cover = "http://silvertwo" )
basetwoextra = MovieExtra( year = 1928, plot = "BLOBLOBLOB", trailer = "http://wiasjdi" )
basetwo.extra = basetwoextra
ownertriptwo = OwnershipTriplet( user, basetwo, medium )
dbc.add_ownertriplet( ownertriptwo )


# res = dbc.get_movie_by_id(1)
# print(res.extra.genres[0].name)

res = dbc.get_movie_by_id_and_by_googleid( 1, 12 )
print( res.extra.year )

# print( dbc.get_users()[0].googleid )
# print(dbc.get_user_with_media_by_googleid(12).media[0].name)
# print( dbc.get_users()[0].triplet[0].movie.title )
# print( dbc.get_user_by_googleid( 12 ).id )

# m = dbc.get_movie_by_id( 1 )

# print( m.title )
# print( m.extra.genres[0].name )
# print( m.extra.cast[0].name )


''' TODO: eager loading helyett megcsinalni,hogy querykre legyen csak eager loading, hogy amikor a usert keressuk, akkor ne szedje le az egesz adatbazist! 
AZAZ: lazy = 'joined' helyett lazy  = 'dynamic' - et irni a relationshipnel
 '''
