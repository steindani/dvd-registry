'''
@author:  benedekh
'''

from db.entities.Base import Base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class Medium( Base ):
    __tablename__ = 'media'
    
    id = Column( Integer, Sequence( 'medium_id_seq' ), primary_key = True )
    name = Column( String )