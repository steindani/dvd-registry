import tmdbsimple as tmdb
from requests.exceptions import HTTPError
from translate.yandexhelper import translate 

''' TMDB lib: https://github.com/celiao/tmdbsimple '''

class TMDBHelper( object ):
    _API_KEY = '13ed7e5e07699386ba2c32a52aed7ae6'
    
    def getMovieByID( self, movie_id ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        result_movie = {}
        
        try:
            movie = tmdb.Movies( int( movie_id ) )
            
            movie_posters = movie.images()
            movie_infos = movie.info( language = 'hu' )
            movie_credits = movie.credits()
            movie_videos = movie.videos()
            
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
                result_movie['trailer'] = ''
        except HTTPError:
            pass
        
        return result_movie
    
    
    def getMovieByTitle( self, title_fragment ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        result_movie = {}
        
        try:
            search = tmdb.Search()
            response = search.movie( query = str( title_fragment ), language = 'hu' )
            if( len( response['results'] ) > 0 ):
                tmdb_id = response['results'][0]['id']
                result_movie = self.getMovieByID( tmdb_id )
        except HTTPError:
             pass
         
        return result_movie
    
    
    def getFirstFiveResults( self, title_fragment, year = None ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        result_movies = {}
        result_movies['results'] = []
        result_movies['first_result'] = {}
        
        try:
            search = tmdb.Search()
            response = search.movie( query = str( title_fragment ), year = year, language = 'hu' )
            
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
        
        except HTTPError:
             pass
         
        return result_movies
