'''
@author: benedekh
'''
from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
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
    
    
    '''ADDER METHODS'''
    
    def _add_object( self, obj ):
        # create session
        _session_creator = self.create_session()
        _session = _session_creator()
        
        # insert and commit
        _session.add( obj )
        _session.flush()
        _session.refresh( obj )
        _session.commit()
        
        # remove session
        _session_creator.remove()
    
    def add_user( self, user ):
        self._add_object( user )
        
    def add_medium( self, medium ):
        self._add_object( medium )
    
    def add_movie( self, movie ):
        self._add_object( movie )
   
    def add_ownertriplet( self, ownertriplet ):
        self._add_object( ownertriplet )
    
    '''GETTER METHODS BY QUERY'''
    
    def get_user_with_media_by_googleid( self, googleid ):
        # create session
        _session_creator = self.create_session()
        _session = _session_creator()
        
        # fetch result
        user = _session.query( User ).filter_by( googleid = googleid ).first()
        user.media
        
        # remove session
        _session_creator.remove()
        
        return user
    
    
    def get_user_only_by_googleid( self, googleid ):
        # create session
        _session_creator = self.create_session()
        _session = _session_creator()
        
        # fetch result
        user = _session.query( User ).filter_by( googleid = googleid ).first()
        
        # remove session
        _session_creator.remove()
        
        return user
    
    
    def get_movie_bases_by_googleid( self, googleid ):
        # create session
        _session_creator = self.create_session()
        _session = _session_creator()
        
        # fetch result
        user = _session.query( User ).filter_by( googleid = googleid ).first()
        for triplet in user.triplet:
            triplet.movie
            
        # remove session
        _session_creator.remove()
        
        return user
    
    def get_movie_by_id_and_by_googleid( self, movieid, googleid ):
        # create session
        _session_creator = self.create_session()
        _session = _session_creator()
        
        # fetch result
        user_ownertriplet_moviebase_tuple = _session.query( User, OwnershipTriplet, MovieBase ).join( OwnershipTriplet ).join( MovieBase ).filter( User.googleid == googleid ).filter( MovieBase.id == movieid ).first()
        movie = user_ownertriplet_moviebase_tuple[2]
        movie.triplet.medium
        movie.extra
        movie.extra.cast
        movie.extra.genres
        
        # remove session
        _session_creator.remove()
        
        return movie
