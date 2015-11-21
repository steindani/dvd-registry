from db.entities.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Enum


class Genre( Base ):
    __tablename__ = 'genres'
    
    id = Column( Integer, Sequence( 'genre_id_seq' ), primary_key = True )
    name = Column( String )
    
    movie_id = Column( Integer, ForeignKey( 'moviesextra.id' ) )
