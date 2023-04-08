import googleapiclient.discovery
from googleapiclient.errors import HttpError
# Define the scopes that the application needs
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
def extract_comments(youtube, video_id):
    """
    Extracts comments for a given video using the YouTube API.

    Args:
        youtube: A YouTube API client object.
        video_id (str): The ID of the video for which to extract comments.

    Returns:
        List[str]: A list of comments for the given video.

    Raises:
        Exception: If there is an error with the YouTube API request or response.
    """
    try:
        # Get the comments for the video
        comments = []
        next_page_token = None
        while True:
            comments_request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=50,
                pageToken=next_page_token
            )
            comments_response = comments_request.execute()

            # Extract the comment text from the response
            for comment_item in comments_response['items']:
                comment = comment_item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Check if there are more comments to retrieve
            if 'nextPageToken' in comments_response:
                next_page_token = comments_response['nextPageToken']
                if len(comments) >= 100:
                    break
            else:
                break

        return comments

    except HttpError as e:
        # Check if comments are disabled for the video
        if "commentsDisabled" in str(e):
            #print(f"Comments are disabled for video ID {video_id}")
            comments = []
            return comments
        else:
            # Raise an exception if there is an error with the YouTube API request or response
            raise Exception(f"Error with YouTube API request or response: {str(e)}")






def extract_data(search_query, api_key):
    """
    Extracts video data from YouTube API.

    Args:
        search_query (str): The search query to look up in YouTube.
        api_key (str): The Google API key to use for the YouTube API.

    Returns:
        List[dict]: A list of dictionaries, where each dictionary contains information about a video.

    Raises:
        ValueError: If the search_query or api_key parameters are None or empty.
        Exception: If there is an error with the YouTube API request or response.
    """
    if not search_query:
        raise ValueError('search_query parameter cannot be None or empty')
    if not api_key:
        raise ValueError('api_key parameter cannot be None or empty')

    # Authenticate the user using API key
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    try:
        videos = []
        next_page_token = None
        while True:
            # Search for videos matching the search query
            request = youtube.search().list(
                q=search_query,
                type='video',
                part='id,snippet',
                maxResults=10,
                pageToken=next_page_token
            )
            response = request.execute()

            # Extract the video ids and titles from the search results
            for item in response['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                publish_date = item['snippet']['publishedAt']

                # Get the video statistics for the video
                video_request = youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                )
                video_response = video_request.execute()

                # Extract the statistics data from the response
                statistics = video_response['items'][0]['statistics']
                views = statistics['viewCount'] if 'viewCount' in statistics else 0
                likes = statistics['likeCount'] if 'likeCount' in statistics else 0
                channel_id = video_response['items'][0]['snippet']['channelId']
                # Get the channel statistics to extract the subscriber count
                channel_request = youtube.channels().list(
                    part='statistics',
                    id=channel_id
                )
                channel_response = channel_request.execute()
                channel_statistics = channel_response['items'][0]['statistics']
                subscribers = channel_statistics['subscriberCount'] if 'subscriberCount' in channel_statistics else 0

                # Extract comments for the video
                comments = []
                try:
                    comments = extract_comments(youtube, video_id)
                except Exception as e:
                    print(f'Error extracting comments for video ID {video_id}: {str(e)}')

                # Create a dictionary with video information
                video_dict = {
                    'video_id': video_id,
                    'title': title,
                    'publish_date': publish_date,
                    'views': views,
                    'likes': likes,
                    'subscribers': subscribers,
                    'comments': comments
                }
                videos.append(video_dict)
            
            # Check if there are more results to fetch
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
            else:
                break
                
            # Stop iterating if we have reached the maximum number of videos
            if len(videos) >= 50:
                break

        return videos
    except Exception as e:
        # Raise an exception if there is an error with the YouTube API request or response
        raise Exception(f'Error with YouTube API request or response: {str(e)}')
"""
search_query = "python programming"
api_key = "AIzaSyBcUS4oDeIMm3WPa2pa3wfWHwhnB0wXwPQ"
videos = extract_data(search_query, api_key)
"""
