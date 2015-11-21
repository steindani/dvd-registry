from tmdb.tmdbhelper import TMDBHelper

def print_dict( dics ):
    for key in dics:
        print( key, dics[key] )
    print( '-----------------------' )

helper = TMDBHelper()

#===============================================================================
# movie = helper.get_movie_by_id( 296100 )
# print_dict( movie )
#  
# print(TMDBHelper._movie_data_cache)
#  
# movie = helper.get_movie_by_id( 296100 )
# #print_dict( movie )
# print(TMDBHelper._movie_data_cache)
# 
# movie = helper.get_movie_by_title( 'The Night Before' )
# print_dict( movie )
# print( TMDBHelper._movie_data_cache )
#   
# print( '---------------------------------' )
#  
# movie = helper.get_movie_by_id( 296100, title_fragment = 'The Night Before' )
# print( TMDBHelper._movie_data_cache )
# print_dict( movie )
#  
# print( '---------------------------------' )
#  
# movie = helper.get_movie_by_title( 'The Night Before' )
# print_dict( movie )
# print( TMDBHelper._movie_data_cache )
#  
# print( '---------------------------------' )
# print( '---------------------------------' )
# print( '---------------------------------' )
#  
# fragments = helper.get_first_five_results( 'The Fif' )
# print_dict( fragments )
#  
# print( len( TMDBHelper._short_query_cache ) )
#  
# print( '---------------------------------' )
#===============================================================================
 
#===============================================================================
# fragments = helper.get_first_five_results( 'The Fif' )
# print_dict( fragments )
# fragment = 'the fifth(1997) element '
#          
# if ( '(' in fragment ) and ( ')' in fragment ):
#     opening_index = fragment.find( '(' )
#     closing_index = fragment.find( ')' )
#     if( opening_index > closing_index ):
#         result = helper.get_first_five_results( fragment )
#     else:
#         subs = fragment[opening_index + 1:closing_index]
#         if ( '(' in subs ) or ( ')' in subs ):
#             result = helper.get_first_five_results( fragment )
#         else:
#             try:
#                 year = int( subs )
#                 if( len( fragment[closing_index + 1:].strip() ) > 0 ):
#                     # there is something after the year parenthesis
#                     result = helper.get_first_five_results( fragment )    
#                 else:
#                     result = helper.get_first_five_results( title_fragment = fragment[:opening_index], year = year )
#             except ValueError:
#                 result = helper.get_first_five_results( fragment )
# else:
#     result = helper.get_first_five_results( fragment )
#                  
# print( result )
#===============================================================================
