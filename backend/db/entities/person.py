from db.entities.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

class Person( Base ):
    __tablename__ = 'cast'
    
    id = Column( Integer, Sequence( 'person_id_seq' ), primary_key = True )
    name = Column( String, nullable = False )
    
    movie_id = Column( Integer, ForeignKey( 'moviesextra.id' ) )
    
    
    
