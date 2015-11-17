import tmdbsimple as tmdb
from requests.exceptions import HTTPError

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
            
            result_movie['original_title'] = movie.original_title
            result_movie['genres'] = [genre['name'] for genre in movie.genres]
            result_movie['plot'] = movie.overview
            result_movie['year'] = movie.release_date [0:4]
            result_movie['poster_path'] = 'https://image.tmdb.org/t/p/w185' + movie.poster_path
            result_movie['poster_original_path'] = 'https://image.tmdb.org/t/p/original' + movie.poster_path
            result_movie['cast'] = sorted( [ cast['name'] for cast in movie.cast] )
            result_movie['trailer'] = 'https://www.youtube.com/watch?v=' + movie_videos['results'][0]['key']
        except HTTPError:
            pass
        
        return result_movie
    
    def getFirstFiveResults( self, title_fragment ):
        tmdb.API_KEY = TMDBHelper._API_KEY
        
        result_movies = {}
        
        try:
            search = tmdb.Search()
            response = search.movie( query = str( title_fragment ), language = 'hu' )
            
            possible_results = [( result['original_title'], result['id'], result['overview'], result['poster_path'] ) for result in response['results'] if response['results'].index( result ) < 5 ]
            result_movies['possible_ids'] = [result[1] for result in possible_results]
            result_movies['possible_titles'] = [result[0] for result in possible_results]
            result_movies['first_result'] = {}
            
            if( len( possible_results ) > 0 ):
                result_movies['first_result']['original_title'] = possible_results[0][0] 
                result_movies['first_result']['overview'] = possible_results[0][2] 
                result_movies['first_result']['poster_path'] = 'https://image.tmdb.org/t/p/w185' + possible_results[0][3] 
        
        except HTTPError:
             pass
         
        return result_movies
