import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Define a function to get the transcript for a given video ID
def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_list:
            transcript += ' ' + i['text']
        return transcript
    except:
        return None

# Define a function to get the sentiment scores for a given text
def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores['compound']

# Define a function to get the video data for a given video ID
def get_video_data(video_id):
    video_data = {}
    video_data['VideoID'] = video_id
    video_data['Transcript'] = get_transcript(video_id)
    if video_data['Transcript'] is not None:
        video_data['Sentiment'] = get_sentiment(video_data['Transcript'])
    else:
        video_data['Sentiment'] = None
    return video_data

# Define a function to get the top videos for a given search query and date range
def get_top_videos(query, start_date, end_date):
    api_key = os.environ.get('YOUTUBE_API_KEY')
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&maxResults=25&q={query}&publishedAfter={start_date}T00:00:00Z&publishedBefore={end_date}T23:59:59Z"
    response = pd.read_json(url)
    video_ids = response['items'].apply(lambda x:x['id']['videoId'])
    video_data = pd.DataFrame([get_video_data(i) for i in video_ids], columns=['VideoID', 'Transcript', 'Sentiment'])
    video_data.dropna(inplace=True)
    video_data.sort_values('Sentiment', ascending=False, inplace=True)
    video_data.reset_index(inplace=True, drop=True)
    return video_data

# Define a function to calculate the weighted average sentiment score
def get_weighted_sentiment(video_data):
    weights = [1/(i+1) for i in range(len(video_data))]
    total_weight = sum(weights)
    weighted_scores = [score*weight for score, weight in zip(video_data['Sentiment'], weights)]
    weighted_average = sum(weighted_scores)/total_weight
    return weighted_average

# Define a function to write the video data to a CSV file
def write_csv(video_data, filename):
    video_data.to_csv(filename, index=False)

# Define the main function
def main():
    query = input("Enter a search query: ")
    start_date = input("Enter a start date (YYYY-MM-DD): ")
    end_date = input("Enter an end date (YYYY-MM-DD): ")
    video_data = get_top_videos(query, start_date, end_date)
    print("Top videos:")
    print(video_data.head())
    weighted_sentiment = get_weighted_sentiment(video_data)
    print(f"Weighted average sentiment score: {weighted_sentiment:.2f}")
    filename = f"{query}_{start_date}_{end_date}.csv"
    write_csv(video_data, filename)
    print(f"Video data written to {filename}")

if __name__ == '__main__':
    main()
