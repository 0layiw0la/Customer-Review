import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

# function to get the polarity of a review
def GetPolarity(review):
    analyser = SIA()  
    analyser.lexicon.update({  # Updating the lexicon with custom words and their sentiment scores
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

# function to get the sentiment based on the polarity scores
def GetSentiment(polarity):
    if polarity['compound'] > 0.1:  
        return "Positive"  
    elif polarity['compound'] < -0.2 and polarity['neg'] > 0.2:  
        return "Negative"  
    else:
        return "Neutral"  
