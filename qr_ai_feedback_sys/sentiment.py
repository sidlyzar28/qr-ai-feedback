from textblob import TextBlob

def get_sentiment(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)  # -1 to 1
