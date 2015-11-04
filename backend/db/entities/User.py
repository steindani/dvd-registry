'''
@author:  benedekh
'''

from db.entities.Base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class User( Base ):
    __tablename__ = 'users'
    
    id = Column( Integer, Sequence( 'user_id_seq' ), primary_key = True )
    googleid = Column( String )
    
    triplet = relationship( 'db.entities.OwnershipTriplet.OwnershipTriplet', uselist = False, lazy = 'joined' )
    
    media = relationship( 'db.entities.Medium.Medium', lazy = 'joined' )