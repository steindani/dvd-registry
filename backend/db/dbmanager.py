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
from datetime import datetime


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
        
        # update last access time for movie
        self.update_movie_last_access( movie.extra, _session )
        
        # load required data
        movie.triplet.medium
        movie.extra
        movie.extra.cast
        movie.extra.genres
        
        # remove session
        _session_creator.remove()
        
        return movie

    ''' UPDATE METHODS '''

    def update_movie_last_access( self, movie_extra_obj, session ):
        movie_extra_obj.last_access = datetime.now()
        self._add_object( movie_extra_obj, session )

    ''' UPDATE METHODS '''
    ''' TODO: felhasználóhoz hozzávenni, hogy mikor jelentkezett be utoljára, ha nincsen belépve akkor 0000 legyen a dátum helyette (vagy helyette egy kijeleentkezés dátumot)
        TODO: felhasználóhoz a legutolsó bejeletnkezést átírni 0000-ra, ha kijelentkezett (vagy helyette egy kijelenektezési dátumot)
        TODO: a felhasználó bejelentkezettségét le lehessen kérdezni egy get metódussal, ami visszaadja, a legutolsó bejelentkezés dátumát (vagy helyette egy kijelentkezési dátumot és az alapján megnézni, hogy ő most be van-e lépve)
        TODO: film hozzáadásának folyamatát végiggondolni, mit kell visszaadni a JS-nek, mit nem adunk már vissza neki, mi az amit nekünk kell most még eközben megcsinálnunk szerveroldalon (hogyan kapom vissza az adatokat kliensoldalró, hogy most akkor mit választott a felhasználó, hogymit ad hozzá az adatbázishoz)
        TODO: minden hívásnál megvizsgálni, hogy a user be van-e jelentkezve, mert ha nincsen, akkor 403-at (access denied-ot) visszaküldeni
        TODO: google atuhentikációt integrálni ehhez
        TODO: https-et integrálni az egészhez, megnézni hogy a flask tudja-e (kell-e tudnia)
     '''
