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

# movie = helper.getMovieByID( 296100 )
# print_dict( movie )
    
# fragments = helper.getFirstFiveResults( 'The Fifth Element' )
# print_dict( fragments )

# print(helper.getMovieByTitle('The Fifth Element))


fragments = helper.getFirstFiveResults( ' ' )
print( fragments )

#===============================================================================
# fragment = 'the fifth(1997) element '
#         
# if ( '(' in fragment ) and ( ')' in fragment ):
#     opening_index = fragment.find( '(' )
#     closing_index = fragment.find( ')' )
#     if( opening_index > closing_index ):
#         result = helper.getFirstFiveResults( fragment )
#     else:
#         subs = fragment[opening_index + 1:closing_index]
#         if ( '(' in subs ) or ( ')' in subs ):
#             result = helper.getFirstFiveResults( fragment )
#         else:
#             try:
#                 year = int( subs )
#                 if( len( fragment[closing_index + 1:].strip() ) > 0 ):
#                     # there is something after the year parenthesis
#                     result = helper.getFirstFiveResults( fragment )    
#                 else:
#                     result = helper.getFirstFiveResults( title_fragment = fragment[:opening_index], year = year )
#             except ValueError:
#                 result = helper.getFirstFiveResults( fragment )
# else:
#     result = helper.getFirstFiveResults( fragment )
#                 
# print( result )
#===============================================================================
