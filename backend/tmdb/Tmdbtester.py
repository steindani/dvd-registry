'''
Created on Nov 8, 2015

@author: benjo
'''

import tmdbsimple as tmdb

tmdb.API_KEY = '13ed7e5e07699386ba2c32a52aed7ae6'

movie = tmdb.Movies( 603 )
posters = movie.images()

movie_infos = movie.info()

print( "Original title: " + movie_infos['original_title'] )
print( "Genres: " + str( [genre['name'] for genre in movie_infos['genres']] ) )
print( "Plot: " + movie_infos['overview'] )
print( "Year: " + str( movie_infos['release_date'] )[0:4] )
print( "Poster path (w185): https://image.tmdb.org/t/p/w185" + movie_infos['poster_path'] )
print( "Poster path (original): https://image.tmdb.org/t/p/original" + movie_infos['poster_path'] )

movie_credits = movie.credits()

print( "Cast: " + str( sorted( [ cast['name'] for cast in movie_credits['cast']] ) ) )

movie_videos = movie.videos()

print( "Trailer: https://www.youtube.com/watch?v=" + movie_videos['results'][0]['key'] )
print( " -------------------------------------------- " )

search = tmdb.Search()
response = search.movie( query = 'The Fif' )

print( "First five titles: " + str( [( result['original_title'], result['id'] ) for result in response['results'] if response['results'].index( result ) < 5 ] ) )
print( "First title data: " + str( [( result['original_title'], result['overview'], 'https://image.tmdb.org/t/p/w185' + result['poster_path'], result['id'] ) for result in response['results'] if response['results'].index( result ) < 1 ] ) )
