'''
@author: benedekh
'''
from db.entities.Base import Base
from db.entities.Genre import Genre
from db.entities.Medium import Medium
from db.entities.Movie import Movie
from db.entities.Person import Person
from db.entities.User import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from db.entities.OwnershipTriplet import OwnershipTriplet


class DBManager( object ):
    
    def __init__( self ):
        self.engine = create_engine( 'sqlite:///:memory:', echo = False )
        
        try:
            self.engine.connect().close()
        except Exception:
            # TODO better error handling
            raise

        self.session_factory = sessionmaker( bind = self.engine )
        
    def init_db( self ):
        Base.metadata.create_all( bind = self.engine )
        
    def create_session( self ):
        """
        Returns a scoped session object from the Session Factory.
        PostgreSQLAlchemyConnector should never create any session (scoped, or otherwise) to access the database.
        Instead, the session returned by this method should be supplied to the functions in PostgreSQLAlchemyConnector
        wherever there is a need for a session to access the database.
        :return: sqlalchemy.orm.session.Session
        """
        
        return scoped_session( self.session_factory )
    
    
    '''ADDER METHODS'''
    
    def _add_object( self, obj ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        _session.add( obj )
        
        _session.flush()
        _session.refresh( obj )
        _session.commit()
        
        _session_creator.remove()
    
    def add_user( self, user ):
        self._add_object( user )
        
    def add_medium( self, medium ):
        self._add_object( medium )
    
    def add_movie( self, movie ):
        self._add_object( movie )
   
    def add_ownertriplet( self, ownertriplet ):
        self._add_object( ownertriplet )
        
    '''GETTER METHODS'''
        
    def get_media( self ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( Medium ).all()
        _session_creator.remove()
        
        return result
    
    def get_users( self ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( User ).all()
        _session_creator.remove()
        
        return result
        
    def get_ownertriplet( self ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( OwnershipTriplet ).all()
        _session_creator.remove()
        
        return result
    
    def get_movies( self ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( Movie ).all()
        _session_creator.remove()
        
        return result
    
    
    '''GETTER METHODS BY QUERY'''
    
    def get_medium_by_userid( self, userid ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( Medium ).filter_by( user_id = userid ).first()
        _session_creator.remove()
        
        return result
    
    def get_user_by_googleid( self, googleid ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( User ).filter_by( id = googleid ).first()
        _session_creator.remove()
        
        return result
    
    def get_movie_by_id( self, movieid ):
        _session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( Movie ).filter_by( id = movieid ).first()
        _session_creator.remove()
        
        return result
