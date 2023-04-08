import googleapiclient.discovery
import google.oauth2.credentials
import os


# Define the scopes that the application needs
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def extract_data(search_query, api_key):
    # Authenticate the user using API key
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    
    # Search for videos matching the search query
    request = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=5
    )
    response = request.execute()
    
    # Extract the video ids and titles from the search results
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        
        # Get the video statistics for the video
        video_request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        video_response = video_request.execute()
        
        # Extract the statistics data from the response
        statistics = video_response['items'][0]['statistics']
        
        # Get the comments for the video
        comments_request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        comments_response = comments_request.execute()
        
        # Extract the comment text from the response
        comments = []
        for comment_item in comments_response['items']:
            comment = comment_item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        videos.append({'id': video_id, 'title': title, 'comments': comments, 'statistics': statistics})
    
    # Return the list of videos
    return videos
