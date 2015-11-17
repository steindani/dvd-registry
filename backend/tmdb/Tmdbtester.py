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

movie = helper.getMovieByID( 296100 )
print_dict( movie )
    
fragments = helper.getFirstFiveResults( 'the fif' )
print_dict( fragments )
