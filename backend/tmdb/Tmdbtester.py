'''
Created on Nov 8, 2015

@author: benjo
'''

from tmdb.tmdbhelper import TMDBHelper

def print_dict( dics ):
    for key in dics:
        print( key, dics[key] )
    print( '-----------------------' )

helper = TMDBHelper()

movie = helper.getMovieByID( 123 )
print_dict( movie )
    
fragments = helper.getFirstFiveResults( 'The Fif' )
print_dict( fragments )
