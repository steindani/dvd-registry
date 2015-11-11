'''
@author:  benedekh
'''

from db.entities.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class User( Base ):
    __tablename__ = 'users'
    
    id = Column( Integer, Sequence( 'user_id_seq' ), primary_key = True )
    googleid = Column( String )
    
    triplet = relationship( 'db.entities.ownershiptriplet.OwnershipTriplet', lazy = 'joined' )
    media = relationship( 'db.entities.medium.Medium', lazy = 'joined' )