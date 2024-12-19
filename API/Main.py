import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from WebScraping import WebScraper  
from DataTransformation import GetPolarity, GetSentiment 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://getcustomerreviews.netlify.app"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],  
    allow_headers=["*"],  
)

class ReviewRequest(BaseModel):
    business_name: str
    location_name: str

@app.get("/")
async def test():
    return {"message":"cors works"}

@app.post("/get_reviews")
async def scrape_reviews(request: ReviewRequest): 
    reviews_df, avg_rating = WebScraper(request.business_name, request.location_name)
    if reviews_df is None or reviews_df.empty:
        return {"error" :"Location not found"}
    
    reviews_df['polarity'] = reviews_df["Review"].apply(GetPolarity)  
    reviews_df['sentiment'] = reviews_df['polarity'].apply(GetSentiment)

    positive_dict = {}
    negative_dict = {}

    if (reviews_df['sentiment'] == 'Positive').sum() > 0:
        limit = min(5, (reviews_df['sentiment'] == 'Positive').sum())
        top_positive = reviews_df[reviews_df['sentiment'] == 'Positive'].head(limit)[['Review', 'Date']]
        positive_dict = dict(zip(top_positive['Review'], top_positive['Date']))
    else:
        top_positive = "No positive comments from past 30 reviewers!"

    if (reviews_df['sentiment'] == 'Negative').sum() > 0:
        limit = min(5, (reviews_df['sentiment'] == 'Negative').sum())
        top_negative = reviews_df[reviews_df['sentiment'] == 'Negative'].head(limit)[['Review', 'Date']]
        negative_dict = dict(zip(top_negative['Review'], top_negative['Date']))
    else:
        top_negative = "No Negative comments from past 30 reviewers!"
        
    return {"positive_reviews": positive_dict, "negative_reviews": negative_dict, "avg_rating": avg_rating}
