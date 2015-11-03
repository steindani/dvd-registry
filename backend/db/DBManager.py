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
    
    def add_movie( self, movie ):
        _session_creator = self.session_factory
        #_session_creator = self.create_session()
        _session = _session_creator()
        
        _session.add( movie )
        
        _session.flush()
        _session.refresh( movie )
        _session.commit()
        
        #_session_creator.remove()
    
    def get_movie_by_title( self, titlequery ):
        _session_creator = self.session_factory
        #_session_creator = self.create_session()
        _session = _session_creator()
        
        result = _session.query( Movie ).filter_by( title = titlequery ).all()
        #_session_creator.remove()
        
        return result
