'''
@author:  benedekh
'''

from db.entities.Base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


movie_cast_association_table = Table( 'moviecast', Base.metadata,
    Column( 'left_id', Integer, ForeignKey( 'movies.id' ) ),
    Column( 'right_id', Integer, ForeignKey( 'cast.id' ) )
 )

movie_genre_association_table = Table( 'moviegenre', Base.metadata,
    Column( 'left_id', Integer, ForeignKey( 'movies.id' ) ),
    Column( 'right_id', Integer, ForeignKey( 'genres.id' ) )
 ) 

class Movie( Base ):
    __tablename__ = 'movies'
    
    id = Column( Integer, Sequence( 'movie_id_seq' ), primary_key = True )
    title = Column( String )
    year = Column( Integer )
    plot = Column( String )
    trailer = Column( String )
    poster = Column( String )
    
    triplet = relationship( 'db.entities.OwnershipTriplet.OwnershipTriplet', uselist = False, lazy = 'joined' )
    
    cast = relationship( 'db.entities.Person.Person',
                    secondary = movie_cast_association_table,
                    backref = backref( 'movies' ), lazy = 'joined' )
    genre = relationship( 'db.entities.Genre.Genre',
                    secondary = movie_genre_association_table,
                    backref = backref( 'movies' ), lazy = 'joined' )
