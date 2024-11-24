import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

def GetPolarity(review):
    analyser = SIA()
    analyser.lexicon.update({
        "thieves":-10,
        "owing":-10,
        "lie":-10,
        "1/5":-10,
        "2/5":-6,
        "5/5":10,
        "terrible":-10,
        "disgusting":-10,
        "hot":-10,
        "wet":-10
    })
    return analyser.polarity_scores(review)

def GetSentiment(polarity):
    if polarity['compound'] > 0.1:
        return "Positive"
    elif polarity['compound'] < -0.2 and polarity['neg'] > 0.2:
        return "Negative"
    else:
        return "Neutral"