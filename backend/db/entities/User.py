'''
@author:  benedekh
'''

from entities.Base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


user_movie_association_table = Table( 'usermovie', Base.metadata,
    Column( 'left_id', Integer, ForeignKey( 'users.id' ) ),
    Column( 'right_id', Integer, ForeignKey( 'movies.id' ) )
 ) 

class User( Base ):
    __tablename__ = 'users'
    
    id = Column( Integer, Sequence( 'user_id_seq' ), primary_key = True )
    googleid = Column( String )
    
    media = relationship( 'Medium', backref = backref( 'media' ) )
    
    movies = relationship( 'Movie',
                    secondary = user_movie_association_table,
                    backref = backref( 'users' ) )
    
