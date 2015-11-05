'''
@author:  benedekh
'''

from db.entities.Base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class MovieBase( Base ):
    __tablename__ = 'movies'
    
    id = Column( Integer, Sequence( 'movie_id_seq' ), primary_key = True )
    title = Column( String )
    cover = Column( String )
    
    triplet = relationship( 'db.entities.OwnershipTriplet.OwnershipTriplet', uselist = False, lazy = 'joined' )
    extra = relationship( 'db.entities.Movie.MovieExtra', uselist = False, lazy = 'joined' )
    
class MovieExtra( Base ):
    __tablename__ = 'moviesextra'
    
    id = Column( Integer, Sequence( 'movie_id_seq' ), primary_key = True )
    year = Column( Integer )
    plot = Column( String )
    trailer = Column( String )
    
    moviebase_id = Column( Integer, ForeignKey( 'movies.id' ) )
    
    cast = relationship( 'db.entities.Person.Person', lazy = 'joined' )
    genres = relationship( 'db.entities.Genre.Genre', lazy = 'joined' )

