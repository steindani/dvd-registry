'''
@author: benjo
'''
from datetime import datetime, timedelta
from db.dbmanager import DBManager
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
from db.entityhelper import EntityFactory, EntityConnector
from random import randrange

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
print( movieextra.last_access )

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
# basetwoextra.last_access = datetime.now()
ownertriptwo = OwnershipTriplet( user, basetwo, medium )
dbc.add_ownertriplet( ownertriptwo )

res = dbc.get_movie_by_id_and_by_googleid( 1, 12 )
print( res.extra.last_access )
print( datetime.now() - res.extra.last_access )

res = dbc.get_movie_bases_by_googleid( 12 )
print( res.triplet[0].movie.title )
print( res.triplet[1].movie.title )

print( dbc.get_movie_bases_not_seen_in_last_time_by_googleid( 1 ) )

print( dbc.get_user_with_media_by_googleid( 11 ) )

print( 'MEDIA TEST' )

dbc.add_user( user2 )

# mtest = Medium( name = "fmedium" )
# mtest.user = user2
# dbc.add_medium( mtest )
mtest2 = Medium( name = "firstmedium" )
mtest2.user = user2
dbc.add_medium( mtest2 )
print( len( dbc.get_user_with_media_by_googleid( 11 ).media ) )
print( dbc.add_medium_to_user( "firstmedium", 11 ).name )
print( dbc.add_medium_to_user( "smedium", 11 ) )
print( dbc.add_medium_to_user( "dmedium", 11 ) )
print( dbc.add_medium_to_user( "firstmedium", 11 ).name )

miu = dbc.add_medium_to_user( "firstmedium", 11 )
miu.name = 'kafka'
dbc.add_movie( miu )
print( dbc.add_medium_to_user( "firstmedium", 11 ) )

print( len( dbc.get_user_with_media_by_googleid( 11 ).media ) )

user3 = User( googleid = 18 )
m = EntityFactory.create_movie( 'title', 'cover', 123, 'plot', 'trailer', ['a', 'b'], ['c', 'd'] )
medium3 = Medium( name = "alaa" )
dbc.add_movie( m )

ot = EntityConnector.connect_user_with_movie_and_medium( user3, m, medium3 )
dbc.add_ownertriplet( ot )

dbc.get_movie_by_id_and_by_googleid( 3, 18 )
print( dbc.get_movie_not_seen_in_last_time_by_googleid( 18 ).extra.year )
