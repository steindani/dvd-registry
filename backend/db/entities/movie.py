'''
@author:  benedekh
'''

from db.entities.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class MovieBase( Base ):
    __tablename__ = 'movies'
    
    id = Column( Integer, Sequence( 'movie_id_seq' ), primary_key = True )
    title = Column( String )
    cover = Column( String )
    
    triplet = relationship( 'db.entities.ownershiptriplet.OwnershipTriplet', uselist = False )
    extra = relationship( 'db.entities.movie.MovieExtra', uselist = False )
    
class MovieExtra( Base ):
    __tablename__ = 'moviesextra'
    
    id = Column( Integer, Sequence( 'movie_id_seq' ), primary_key = True )
    year = Column( Integer )
    plot = Column( String )
    trailer = Column( String )
    
    moviebase_id = Column( Integer, ForeignKey( 'movies.id' ) )
    
    cast = relationship( 'db.entities.person.Person' )
    genres = relationship( 'db.entities.genre.Genre' )

