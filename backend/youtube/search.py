from apiclient.discovery import build
from apiclient.errors import HttpError

import config.configuration

def youtube_search( movie_title ):
    youtube = build( 'youtube', 'v3', developerKey = config.configuration.app.config['YOUTUBE_KEY'] )
    query = movie_title.strip() + ' trailer'
    video_url = ''
    
    try:
        search_response = youtube.search().list( q = query, part = "id", order = 'viewCount', maxResults = 1 ).execute()
        
        for search_result in search_response.get( "items", [] ):
            if search_result["id"]["kind"] == "youtube#video":
                video_url = 'https://www.youtube.com/embed/' + str( search_result["id"]["videoId"] )
                break
    except HttpError:
        pass
    
    return video_url
