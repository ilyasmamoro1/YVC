import pandas as pd
import datetime
from pyth2 import extract_data
from clissy_comment import clissy
from ahp_calcT import perform_ahp
import nltk

nltk.download('vader_lexicon')

api_key ='AIzaSyB7BSYWW622KNiHRLbAy87y7WSNDUarP7o'

# Define search query
search_query = "best rap song"

# Extract video data from search query
videos = extract_data(search_query, api_key)

# Create an empty DataFrame to store the relevant video data
df = pd.DataFrame()
for i in range(len(videos)):
    video_data = {}
    video_data['video id'] = videos[i]['video_id']
    video_data['Number of views'] = videos[i]['views']
    video_data['Number of likes'] = videos[i]['likes']
    video_data['Number of subscribers'] = videos[i]['subscribers']
    video_data['Number of comments'] = len(videos[i]['comments'])
    positive_opinions, negative_opinions = clissy(videos[i]['comments'])
    video_data['Number of positive opinions'] = positive_opinions
    video_data['Number of negative opinions'] = -1 * negative_opinions
  # Calculate the number of days since the video was published
    publish_date = datetime.datetime.strptime(videos[i]['publish_date'], '%Y-%m-%dT%H:%M:%SZ')
    days_since_publish = (datetime.datetime.now() - publish_date).days
    video_data['Days since publish'] = -1 * days_since_publish

    df = df._append(video_data, ignore_index=True)



# Use AHP to rank videos
weights  = [    ['Number of views', 'Number of likes',  'Number of subscribers', 'Number of comments', 'Number of positive opinions', 'Number of negative opinions', 'Days since publish'],
                [   [1, 7, 7, 9, 4, 6, 6],
                    [1/7, 1, 3, 3, 1/7, 1, 1/4],
                    [1/7, 1/3, 1, 1, 1/7, 1/3, 1/4],
                    [1/9, 1/3, 1, 1, 1/8, 1/5, 1/7],
                    [1/4, 7, 7, 8, 1, 4, 6],
                    [1/6, 1, 3, 5, 1/4, 1, 1],
                    [1/6, 4, 4, 7, 1/6, 1, 1],
                ]
            ]



# Perform AHP analysis and assign ranks


feature_points = perform_ahp(weights, total_point=1)
rank_dict = {feature_points[i][0]: feature_points[i][1] for i in range(len(feature_points))}
df['Rank'] = df.apply(lambda row: sum([int(row[col]) * rank_dict.get(col) for col in df.columns if col in rank_dict]), axis=1)
df = df.sort_values(by='Rank', ascending=False)
# Set display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 0)
if len(df) > 10:
    print(df.head(10))
else:
    print(df)

