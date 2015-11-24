from db.entities.base import Base
from db.entities.genre import Genre
from db.entities.medium import Medium
from db.entities.movie import MovieBase, MovieExtra
from db.entities.ownershiptriplet import OwnershipTriplet
from db.entities.person import Person
from db.entities.user import User
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta, date, MINYEAR
from random import randrange

class DBManager( object ):
    
    def __init__( self ):
        self.engine = create_engine( 'sqlite:///movies.db', echo = False )
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
        
        if not session:
            # remove session
            _session_creator.remove()
    
    
    def add_user( self, user ):
        self._add_object( user )
        
    def add_medium( self, medium, session = None ):
        self._add_object( medium, session )
    
    def add_movie( self, movie ):
        self._add_object( movie )
    
    def add_ownertriplet( self, ownertriplet ):
        self._add_object( ownertriplet )
   
    def add_ownertriplet_exists_check( self, ownertriplet ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # params for query
        googleid = ownertriplet.user.googleid
        medium_name = ownertriplet.medium.name
        title = ownertriplet.movie.title
        year = ownertriplet.movie.extra.year
        
        # query similary ownertrip
        ownertrip_exists = session.query( OwnershipTriplet ) \
                                    .join( OwnershipTriplet.user ).join( OwnershipTriplet.movie ).join( OwnershipTriplet.medium ).join( MovieBase.extra ) \
                                    .filter( User.googleid == googleid ) \
                                    .filter( Medium.name == medium_name ) \
                                    .filter( MovieBase.title == title ) \
                                    .filter( MovieExtra.year == year ) \
                                    .first()
                                    
        if ownertrip_exists:
            # remove session
            session_creator.remove()
            return True

        # add ownertriplet
        ownertriplet.movie.extra.last_access = date( MINYEAR, 1, 1 )
        self._add_object( ownertriplet, session )
        
        # remove session
        session_creator.remove()
        return False
        
        
    def add_medium_to_user( self, medium_name, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch user
        user = session.query( User ).filter_by( googleid = str( googleid ) ).first()
        
        if user:
            user_media = self.get_user_with_media_by_googleid( googleid, session = session )
            
            media_names = [medium.name for medium in user_media.media]
            if ( not user_media ) or not( medium_name in media_names ):
                medium = Medium( name = medium_name )
                medium.user = user
                self.add_medium( medium, session = session )
            else:
                medium = [medium for medium in user_media.media if medium.name == medium_name][0]
                
            medium.name
            # remove session
            session_creator.remove()
            return medium
        else:
            # remove session
            session_creator.remove()
            return None
        
    
    '''GETTER METHODS BY QUERY'''

    def get_user_with_media_by_googleid( self, googleid, session = None ):
        # create session
        if not session:
            _session_creator = self.create_session()
            _session = _session_creator()
        else:
            _session = session
        
        # fetch result
        user = _session.query( User ).filter_by( googleid = str( googleid ) ).first()
        
        if user is not None:
            user.media
        
        # remove session
        if not session:
            _session_creator.remove()
        
        return user
    
    
    def get_user_only_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user = session.query( User ).filter_by( googleid = str( googleid ) ).first()

        # remove session
        session_creator.remove()
        
        return user
    
    
    def get_movie_bases_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user = session.query( User ).filter_by( googleid = str( googleid ) ).first()
        
        if user is not None:
            for triplet in user.triplet:
                triplet.movie
                triplet.movie.extra
            
        # remove session
        session_creator.remove()
        
        return user
    
    
    def get_ownertrip_by_year_title_googleid( self, googleid, year, title ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        ownertrip = session.query( OwnershipTriplet ) \
                            .join( OwnershipTriplet.user ).join( OwnershipTriplet.movie ).join( MovieBase.extra ) \
                            .filter( User.googleid == str( googleid ) ) \
                            .filter( MovieBase.title == str( title ) ) \
                            .filter( MovieExtra.year == int( year ) ) \
                            .first()                 

        if ownertrip is not None:
            ownertrip.movie
            ownertrip.movie.extra
            
        # remove session
        session_creator.remove()
        
        return ownertrip
    
    
    def get_ownertriplet_by_googleid_and_criteria( self, googleid, criteria ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        criteria_old = criteria
        try:
            criteria = int( criteria )
        except ValueError:
            criteria = '%' + str( criteria_old ) + '%'
        
        ownertrip_list = session.query( OwnershipTriplet ) \
                            .join( OwnershipTriplet.user ).join( OwnershipTriplet.movie ).join( MovieBase.extra ).join( MovieExtra.cast ).join( MovieExtra.genres ) \
                            .filter( User.googleid == str( googleid ) ) \
                            .filter( or_( 
                                        MovieBase.title.like( criteria ),
                                        MovieExtra.year == criteria,
                                        MovieExtra.plot.like( criteria ),
                                        Person.name.like( criteria ),
                                        Genre.name.like( criteria )
                                    ) ).all()
        
        if len( ownertrip_list ) > 0:
            for ownertrip in ownertrip_list:
                ownertrip.movie
                ownertrip.movie.extra
            
        # remove session
        session_creator.remove()
        return ownertrip_list
    
    
    def get_movie_by_id_and_by_googleid( self, movieid, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        user_ownertriplet_moviebase_tuple = session.query( User, OwnershipTriplet, MovieBase ) \
                                                    .join( OwnershipTriplet ).join( MovieBase ) \
                                                    .filter( User.googleid == str( googleid ) ) \
                                                    .filter( MovieBase.id == int( movieid ) ) \
                                                    .first()
        
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
        last_seen_date_threshold = datetime.now() - timedelta( seconds = 30 )
        user_ownertrip_movie_tuple_list = session.query( User, OwnershipTriplet, MovieBase, MovieExtra ) \
                                                    .join( OwnershipTriplet ).join( MovieBase ).join( MovieExtra ) \
                                                    .filter( User.googleid == str( googleid ) ) \
                                                    .filter( MovieExtra.last_access < last_seen_date_threshold ) \
                                                    .all()
        
        if user_ownertrip_movie_tuple_list == []:
            # remove session
            session_creator.remove()
            return None
        else:
            result_length = len( user_ownertrip_movie_tuple_list )
            index = randrange( result_length )
            movie = user_ownertrip_movie_tuple_list[index][2]
            movie.extra
            
            # remove session
            session_creator.remove()
            return movie
    
    
    def get_movie_bases_not_seen_in_last_time_by_googleid( self, googleid ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        last_seen_date_threshold = datetime.now() - timedelta( seconds = 30 )
        user_ownertrip_movie_tuple_list = session.query( User, OwnershipTriplet, MovieBase, MovieExtra ) \
                                                    .join( OwnershipTriplet ).join( MovieBase ).join( MovieExtra ) \
                                                    .filter( User.googleid == str( googleid ) ) \
                                                    .filter( MovieExtra.last_access < last_seen_date_threshold ) \
                                                    .all()
        
        if user_ownertrip_movie_tuple_list == []:
            # remove session
            session_creator.remove()
            return None
        else:
            movie_bases = [record[2] for record in user_ownertrip_movie_tuple_list]
            for movie_base in movie_bases:
                movie_base.extra
            
            # remove session
            session_creator.remove()
            return movie_bases    


    ''' UPDATE METHODS '''

    def update_movie_last_access( self, movie_extra_obj, session ):
        movie_extra_obj.last_access = datetime.now()
        self._add_object( movie_extra_obj, session )
        
        
    ''' DELETE METHODS '''
    
    def remove_movie_by_id_from_db( self, googleid, movie_id ):
        # create session
        session_creator = self.create_session()
        session = session_creator()
        
        # fetch result
        ownertrip = session.query( OwnershipTriplet ) \
                            .join( OwnershipTriplet.user ).join( OwnershipTriplet.movie ).join( MovieBase.extra ) \
                            .filter( User.googleid == str( googleid ) ) \
                            .filter( MovieExtra.id == int( movie_id ) ).first()
        
        if ownertrip is not None:
            session.delete( ownertrip )
            session.commit()
            # remove session
            session_creator.remove()
            return True
        
        # remove session
        session_creator.remove()
        
        return False
