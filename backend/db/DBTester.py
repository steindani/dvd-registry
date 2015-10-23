'''
@author:  benedekh
'''

from entities.Base import Base
from entities.Genre import Genre
from entities.Medium import Medium
from entities.Movie import Movie
from entities.Person import Person
from entities.User import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine( 'sqlite:///:memory:', echo = False )
Base.metadata.create_all( engine )

Session = sessionmaker( bind = engine )  # do it once (session pools)
session = Session()  # do it any time you need a session (TODO read about session management)

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

session.add( movie )
session.commit()

for mooovie in session.query( Movie ).filter_by( title = "Bronze" ):
    print( mooovie.year )
    print( mooovie.media.name )
    print( mooovie.genre[0].name )
    print( mooovie.cast[0].name )
    print( mooovie.users[0].googleid )
    
for caast in session.query( Person ).filter_by( name = "John Doe" ):
    print( caast.movies[0].title )
    
for geenre in session.query( Genre ).filter_by( name = "Action" ):
    print( geenre.movies[0].users[0].googleid )
