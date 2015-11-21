import tmdbsimple as tmdb
from requests.exceptions import HTTPError
from translate.yandexhelper import translate 
from copy import deepcopy
from youtube.search import youtube_search

''' TMDB lib: https://github.com/celiao/tmdbsimple '''

class TMDBHelper( object ):
    _API_KEY = '13ed7e5e07699386ba2c32a52aed7ae6'
    _movie_data_cache = []
    _short_query_cache = []
    
    def _remove_unused_fields( self, movie_data ):
        movie_data = deepcopy( movie_data )
        movie_data.pop( 'tmdb_id', None )
        movie_data.pop( 'title_fragment', None )
        return movie_data
    
    
    def _get_movie_from_short_query_cache( self, title_fragment ):
        for short_query_record in TMDBHelper._short_query_cache:
            if short_query_record['title_fragment'] == title_fragment:
                return self._remove_unused_fields( short_query_record )


    def _get_movie_from_movie_data_cache( self, title_fragment ):
        for movie_data in TMDBHelper._movie_data_cache:
            if movie_data['title_fragment'] == title_fragment:
                return self._remove_unused_fields( movie_data )
            
            
    def _get_movie_from_movie_data_cache_by_id( self, tmdb_id ):
        for movie_data in TMDBHelper._movie_data_cache:
            if movie_data['tmdb_id'] == tmdb_id:
                return self._remove_unused_fields( movie_data )


    def getMovieByID( self, movie_id, title_fragment = None ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        
        tmdb_id = int( movie_id )
        result_movie = self._get_movie_from_movie_data_cache_by_id( tmdb_id ) 
        
        if result_movie is None:
            try:    
                movie = tmdb.Movies( tmdb_id )
                
                movie_posters = movie.images()
                movie_infos = movie.info( language = 'hu' )
                movie_credits = movie.credits()
                movie_videos = movie.videos()
                
                result_movie = {}
                result_movie['title'] = movie.title
                result_movie['genres'] = [genre['name'] for genre in movie.genres]
    
                if movie.overview is None:
                    movie_infos = movie.info()
                    plot = movie.overview
                    if plot is None: 
                        plot = ''
                    result_movie['plot'] = translate( plot )
                else:
                    result_movie['plot'] = movie.overview
                
                result_movie['year'] = movie.release_date [0:4]
                result_movie['poster_path'] = 'https://image.tmdb.org/t/p/w185' + movie.poster_path
                result_movie['poster_original_path'] = 'https://image.tmdb.org/t/p/w1280' + movie.poster_path
                result_movie['cast'] = sorted( [ cast['name'] for cast in movie.cast] )
                if( len( movie_videos['results'] ) > 0 ):
                    result_movie['trailer'] = 'https://www.youtube.com/embed/' + movie_videos['results'][0]['key']
                else:
                    result_movie['trailer'] = youtube_search( result_movie['title'] )
                    
                if title_fragment is not None:
                    result_movie['title_fragment'] = str( title_fragment )
                else:
                    result_movie['title_fragment'] = ''
                    
                result_movie['tmdb_id'] = tmdb_id
                    
                TMDBHelper._movie_data_cache.append( result_movie )
                result_movie = self._remove_unused_fields( result_movie )
            except HTTPError:
                pass
        
        return result_movie
    
    
    def getMovieByTitle( self, title_fragment ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        result_movie = {}
        title = str( title_fragment )
        
        result_movie = self._get_movie_from_movie_data_cache( title )        

        if result_movie is None:
            try:
                search = tmdb.Search()
                response = search.movie( query = title, language = 'hu' )
                if( len( response['results'] ) > 0 ):
                    tmdb_id = response['results'][0]['id']
                    result_movie = self.getMovieByID( tmdb_id, title_fragment )
            except HTTPError:
                 pass
         
        return result_movie
    
    
    def getFirstFiveResults( self, title_fragment, year = None ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        title = str( title_fragment )
        
        result_movies = self._get_movie_from_short_query_cache( title )
        
        if result_movies is None:
            result_movies = {}
            result_movies['title_fragment'] = title
            result_movies['results'] = []
            result_movies['first_result'] = {}
        
            try:
                search = tmdb.Search()
                response = search.movie( query = title, year = year, language = 'hu' )
                
                if( len( response['results'] ) > 0 ):
                    if len( response['results'][0]['overview'] ) == 0:
                        response = search.movie( query = str( title_fragment ), year = year )
                        plot = response['results'][0]['overview']
                        if plot is None:
                            plot = ''
                        response['results'][0]['overview'] = translate( plot )
                
                possible_results = [( result['id'], result['title'] ) for result in response['results'] if response['results'].index( result ) < 5 ]
                result_movies['results'] = [{'id': result[0], "title":result[1]} for result in possible_results]
                
                if( len( possible_results ) > 0 ):
                    result_movies['first_result']['id'] = response['results'][0]['id']
                    result_movies['first_result']['title'] = response['results'][0]['title']
                    result_movies['first_result']['overview'] = response['results'][0]['overview']
                    result_movies['first_result']['poster_path'] = 'https://image.tmdb.org/t/p/w185' + response['results'][0]['poster_path']
                    
                TMDBHelper._short_query_cache.append( result_movies )
                result_movies = self._remove_unused_fields( result_movies )
            except HTTPError:
                 pass
         
        return result_movies
