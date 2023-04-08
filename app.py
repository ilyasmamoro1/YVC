from flask import Flask, render_template, request
import pandas as pd
import datetime
from pyth2 import extract_data
from clissy_comment import clissy
from ahp_calcT import perform_ahp
import nltk
from jinja2 import Environment

def abs_filter(value):
    return abs(value)

env = Environment()
env.filters['abs'] = abs_filter
nltk.download('vader_lexicon')

api_key ='AIzaSyB7BSYWW622KNiHRLbAy87y7WSNDUarP7o'

app = Flask(__name__)

@app.route('/YVC', methods=['GET', 'POST'])
def index():
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
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form['search_query']
        # Extract video data from search query
        videos = extract_data(search_query, api_key)
        # Perform AHP analysis and assign ranks
        feature_points = perform_ahp(weights, total_point=100)
        rank_dict = {feature_points[i][0]: feature_points[i][1] for i in range(len(feature_points))}
        # Create a list of dictionaries to store the video data
        data = []
        for i in range(len(videos)):
            # Extract relevant video data
            video_data = {}
            video_data['video_id'] =videos[i]['video_id']
            video_data['thumbnail'] = f"https://img.youtube.com/vi/{videos[i]['video_id']}/default.jpg"
            video_data['Number of views'] = float(videos[i]['views'])
            video_data['Number of likes'] = float(videos[i]['likes'])
            video_data['Number of subscribers'] = float(videos[i]['subscribers'])
            video_data['Number of comments'] = float(len(videos[i]['comments']))
            positive_opinions, negative_opinions = clissy(videos[i]['comments'])
            video_data['Number of positive opinions'] = float(positive_opinions)
            video_data['Number of negative opinions'] = -1 * float(negative_opinions)
            publish_date = datetime.datetime.strptime(videos[i]['publish_date'], '%Y-%m-%dT%H:%M:%SZ')
            days_since_publish = (datetime.datetime.now() - publish_date).days
            video_data['Days since publish'] = -1 * float(days_since_publish)
             # Calculate the score of each video
            score = sum([video_data[col[0]] * rank_dict.get(col[0], 0) for col in feature_points if col[0] != ('thumbnail' and 'video_id')])     
            video_data['score'] = score
            data.append(video_data)
        #Sort the list of videos according to their score
        ranked_data = sorted(data, key=lambda x: x['score'], reverse=True)
        # Render the results page with the ranked videos as a table
        return render_template('results.html', data=ranked_data)
    # Render the search page with the search form
    return render_template('index.html')