from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
from pydantic import BaseModel

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ReviewRequest(BaseModel):
    business_name: str
    location_name: str

def WebScraper(business, location, driver_path=r'.\chromedriver-win64\chromedriver.exe'):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(driver_path, options=options)

    driver.get("https://www.google.com")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{business} {location} reviews")
    search_box.send_keys(Keys.RETURN)
    time.sleep(1.5)
    
    try:
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-async-trigger='reviewDialog']"))
        )
        
        review_text = review_button.text
        review_counts_str = review_text.split(" Google reviews")[0].replace(",", "")
        review_counts = int(review_counts_str)
        
        review_button.click()
        time.sleep(1)
        
        avg_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text.strip()
        
        newest_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-checked='false']//span[text()='Newest']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", newest_button)
        driver.execute_script("arguments[0].click();", newest_button)
        time.sleep(1.5)
        review_limit = min(review_counts, 25)  # Limit to 25 reviews
        review_count = 0

        reviews_list = []
        date_list = []
        
        while review_count < review_limit:
            # Wait for review containers to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "BgXiYe"))
            )
            
            # Re-fetch review containers after waiting for them to load
            review_containers = driver.find_elements(By.CLASS_NAME, "BgXiYe")
            
            # Scroll down to load new reviews
            scrollable_element = driver.find_element(By.CLASS_NAME, "review-dialog-list")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)

            # Wait for new reviews to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "BgXiYe"))
            )

            # Iterate through the review containers
            for container in review_containers:
                try:
                    container_soup = BeautifulSoup(container.get_attribute('outerHTML'), 'html.parser')

                    # Extract review date
                    date_span = container_soup.find('span', class_="dehysf lTi8oc")
                    date = date_span.get_text(strip=True) if date_span else None

                    # Extract review text
                    full_text_span = container_soup.find('span', class_='review-full-text')
                    if full_text_span and full_text_span.get_text(strip=True):
                        text = full_text_span.get_text(strip=True)
                    else:
                        alternative_text_span = container_soup.find('span', attrs={'data-expandable-section': True})
                        text = alternative_text_span.get_text(strip=True) if alternative_text_span else None

                    # Add the review if it's new and not already collected
                    if text and text.strip() and text not in reviews_list:
                        reviews_list.append(text)
                        date_list.append(date)
                        review_count += 1

                    # Stop once the review count limit is reached
                    if review_count >= review_limit:
                        break
                except Exception as e:
                    print(f"Error while processing review: {e}")

            # Check if the review count exceeds the limit
            if review_count >= review_limit:
                break

        driver.quit()


        reviews_df = pd.DataFrame({
            "Review": reviews_list,
            "Date": date_list
        })
        print('success',avg_rating)
        return reviews_df, avg_rating
    
    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        return None, None

def GetPolarity(review):
    analyser = SIA()
    return analyser.polarity_scores(review)['compound']

def GetSentiment(polarity):
    if polarity > 0.5:
        return "Positive"
    elif polarity < -0.3:
        return "Negative"
    else:
        return "Neutral"

@app.post("/")
async def scrape_reviews(request: ReviewRequest): 
    reviews_df, avg_rating = WebScraper(request.business_name, request.location_name) 
    if reviews_df is None or reviews_df.empty:
        return {"error" :"Location not found"}
    else:
        pass

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

# To run the FastAPI app, use Uvicorn as follows:
# uvicorn your_script_name:app --reload
