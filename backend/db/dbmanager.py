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
from datetime import datetime, timedelta
from random import randrange

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
    
    def _add_object( self, obj, session = None ):
        # create session
        if not session:
            _session_creator = self.create_session()
            _session = _session_creator()
        else:
            _session = session
        
        # insert and commit
        _session.add( obj )
        _session.flush()
        _session.refresh( obj )
        _session.commit()
        
        # remove session
        if not session:
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
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user = session.query( User ).filter_by( googleid = googleid ).first()
        if user is not None:
            user.media
        
        # remove session
        session_creator.remove()
        
        return user
    
    def get_user_only_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user = session.query( User ).filter_by( googleid = googleid ).first()
        
        # remove session
        session_creator.remove()
        
        return user
    
    def get_movie_bases_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user = session.query( User ).filter_by( googleid = googleid ).first()
        if user is not None:
            for triplet in user.triplet:
                triplet.movie
            
        # remove session
        session_creator.remove()
        
        return user
    
    
    def get_movie_by_id_and_by_googleid( self, movieid, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user_ownertriplet_moviebase_tuple = session.query( User, OwnershipTriplet, MovieBase ).join( OwnershipTriplet ).join( MovieBase ).filter( User.googleid == googleid ).filter( MovieBase.id == movieid ).first()
        
        if user_ownertriplet_moviebase_tuple is None:
            # remove session
            session_creator.remove()
            return None
        else:
            movie = user_ownertriplet_moviebase_tuple[2]
            self._refresh_movie_extra_fields( movie, session )
            
            # remove session
            session_creator.remove()
            return movie
    
    
    def _refresh_movie_extra_fields( self, movie, session ):
         # update last access time for movie
        self.update_movie_last_access( movie.extra, session )    
        # load required data
        movie.triplet.medium
        movie.extra
        movie.extra.cast
        movie.extra.genres
    
    
    def get_movie_not_seen_in_last_time_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        last_seen_date_threshold = datetime.now() - timedelta( days = 0 )
        user_ownertrip_movie_tuple_list = session.query( User, OwnershipTriplet, MovieBase, MovieExtra ).join( OwnershipTriplet ).join( MovieBase ).join( MovieExtra ).filter( User.googleid == googleid ).filter( MovieExtra.last_access < last_seen_date_threshold ).all()
        
        if user_ownertrip_movie_tuple_list == []:
            # remove session
            session_creator.remove()
            return None
        else:
            result_length = len( user_ownertrip_movie_tuple_list )
            index = randrange( result_length )
            movie = user_ownertrip_movie_tuple_list[index][2]
            
            self._refresh_movie_extra_fields( movie, session )
            
            # remove session
            session_creator.remove()
            return movie
    
    
    def get_movie_bases_not_seen_in_last_time_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        last_seen_date_threshold = datetime.now() - timedelta( days = 0 )
        user_ownertrip_movie_tuple_list = session.query( User, OwnershipTriplet, MovieBase, MovieExtra ).join( OwnershipTriplet ).join( MovieBase ).join( MovieExtra ).filter( User.googleid == googleid ).filter( MovieExtra.last_access < last_seen_date_threshold ).all()
        
        if user_ownertrip_movie_tuple_list == []:
            # remove session
            session_creator.remove()
            return None
        else:
            movie_bases = [record[2] for record in user_ownertrip_movie_tuple_list]
            
            # remove session
            session_creator.remove()
            return movie_bases
    
        
    def get_user_login_time( self, googleid ):
        login_time = None
        
        # fetch result
        user = self.get_user_only_by_googleid( googleid )
        if user is not None:
            login_time = user.login_time
        
        return login_time
    
    
    def get_user_logout_time( self, googleid ):
        logout_time = None
        
        # fetch result
        user = self.get_user_only_by_googleid( googleid )
        if user is not None:
            logout_time = user.logout_time
        
        return logout_time
    
    
    ''' IS METHODS BY QUERY '''
    
    def is_user_logged_in( self, googleid ):
        login_time = self.get_user_login_time( 12 )
        logout_time = self.get_user_logout_time( 12 )
        
        if ( login_time is None ) or ( logout_time is None ):
            return None
        
        now = datetime.now()
        user_is_logged_in = ( login_time > logout_time ) and ( now > login_time ) 
        
        return user_is_logged_in


    ''' UPDATE METHODS '''

    def update_movie_last_access( self, movie_extra_obj, session ):
        movie_extra_obj.last_access = datetime.now()
        self._add_object( movie_extra_obj, session )
        
    def update_user_login_time( self, googleid ):
        user = self.get_user_only_by_googleid( googleid )
        if user is not None:
            user.login_time = datetime.now()
            self._add_object( user )
        
    def update_user_logout_time( self, googleid ):
        user = self.get_user_only_by_googleid( googleid )
        if user is not None:
            user.logout_time = datetime.now()
            self._add_object( user )
    

    ''' UPDATE METHODS '''
    ''' TODO: film hozzáadásának folyamatát végiggondolni, mit kell visszaadni a JS-nek, mit nem adunk már vissza neki, mi az amit nekünk kell most még eközben megcsinálnunk szerveroldalon (hogyan kapom vissza az adatokat kliensoldalró, hogy most akkor mit választott a felhasználó, hogymit ad hozzá az adatbázishoz)
        TODO: google atuhentikációt integrálni ehhez
        TODO: https-et integrálni az egészhez, megnézni hogy a flask tudja-e (kell-e tudnia)
     '''
