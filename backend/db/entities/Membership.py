'''
@author: benedekh
'''
 
from db.entities.Base import Base
from db.entities.User import User
from db.entities.Movie import Movie

from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
class Membership( Base ):
    __tablename__ = 'memberships'
    
    user_id = Column( Integer, ForeignKey( 'users.id' ), primary_key = True )
    movie_id = Column( Integer, ForeignKey( 'movies.id' ), primary_key = True )
    medium_id = Column( Integer, ForeignKey( 'media.id' ), primary_key = True )
 
    UniqueConstraint( 'user_id', 'movie_id', 'medium_id' )
    user = relationship( 'db.entities.User.User', uselist = False, backref = 'memberships', lazy = 'joined' )
    movie = relationship( 'db.entities.Movie.Movie', uselist = False, backref = 'memberships', lazy = 'joined' )
    medium = relationship( 'db.entities.Medium.Medium', uselist = False, backref = 'memberships', lazy = 'joined' )
 
    def __init__( self, user, movie, medium ):
        self.user = user
        self.movie = movie
        self.medium = medium
