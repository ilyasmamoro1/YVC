from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def clissy(comments):
    """
    This function takes in a list of comments and returns the number of positive opinions and the number of negative
    opinions
    """
    positive_opinions = 0
    negative_opinions = 0
    for comment in comments:
        sentiment_scores = sia.polarity_scores(comment)
        if sentiment_scores['compound'] >= 0.05:
            positive_opinions += 1
        elif sentiment_scores['compound'] <= -0.05:
            negative_opinions += 1


    return positive_opinions, negative_opinions



