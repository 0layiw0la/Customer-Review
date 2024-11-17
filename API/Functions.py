from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

def WebScraper(business, location, driver_path=r'.\chromedriver-win64\chromedriver.exe'):
    # Initialize WebDriver with headless option
    options = webdriver.ChromeOptions()
    
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Necessary for some environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
    driver = webdriver.Chrome(r'API\chromedriver-win64\chromedriver.exe', options=options)

    driver.get("https://www.google.com")
    
    # Search for the business name and location
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{business} {location} reviews")
    search_box.send_keys(Keys.RETURN)
    time.sleep(1.5)
    
    # Wait for the review button to be clickable
    try:
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-async-trigger='reviewDialog']"))
        )
        
        # Get the number of reviews
        review_text = review_button.text
        review_counts_str = review_text.split(" Google reviews")[0].replace(",", "")
        review_counts = int(review_counts_str)
        
        # Open the reviews modal
        review_button.click()
        time.sleep(1)  # Allow modal to open
        
        avg_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text.strip()
        
        # Wait for the "Newest" filter to be clickable and click it
        newest_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-checked='false']//span[text()='Newest']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", newest_button)
        driver.execute_script("arguments[0].click();", newest_button)

        review_limit = min(review_counts, 25)  # Limit to 100 reviews
        review_count = 0

        # Scroll and scrape reviews
        reviews_list = []
        date_list = []
        
        for _ in range(25):  # Adjust scroll limit as needed
            time.sleep(1.5)
            review_containers = driver.find_elements(By.CLASS_NAME, "BgXiYe")
            scrollable_element = driver.find_element(By.CLASS_NAME, "review-dialog-list")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            
            # Parse each review element
            for container in review_containers:
                container_soup = BeautifulSoup(container.get_attribute('outerHTML'), 'html.parser')
                
                # Extract date
                date_span = container_soup.find('span', class_="dehysf lTi8oc")
                date = date_span.get_text(strip=True) if date_span else None
                
                # Extract review text
                full_text_span = container_soup.find('span', class_='review-full-text')
                if full_text_span and full_text_span.get_text(strip=True):
                    text = full_text_span.get_text(strip=True)
                else:
                    # Look for alternative span if full review text is not found
                    alternative_text_span = container_soup.find('span', attrs={'data-expandable-section': True})
                    text = alternative_text_span.get_text(strip=True) if alternative_text_span else None

                # Append to list if text exists
                if text and text.strip():
                    if text not in reviews_list:
                        reviews_list.append(text)
                        date_list.append(date)
                        review_count += 1
                        if review_count >= review_limit:
                            break
            if review_count >= review_limit:
                break

        # Close the driver
        driver.quit()

        # Convert the lists into a DataFrame
        reviews_df = pd.DataFrame({
            "Review": reviews_list,
            "Date": date_list
        })

        return reviews_df, avg_rating
    
    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        return pd.DataFrame()  # Return empty DataFrame on error

def GetPolarity(review):
    analyser = SIA()
    return analyser.polarity_scores(review)['compound']

def GetSentiment(polarity):
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.65:
        return "Negative"
    else:
        return "Neutral"

def App(business_name, location_name):
    reviews_df, avg_rating = WebScraper(business_name, location_name) 
    
    # Apply sentiment analysis to each review
    reviews_df['polarity'] = reviews_df["Review"].apply(GetPolarity)  
    reviews_df['sentiment'] = reviews_df['polarity'].apply(GetSentiment)
    positive_dict = {}
    negative_dict = {}

    if (reviews_df['sentiment'] == 'Positive').sum() > 0:
        limit = min(5, (reviews_df['sentiment'] == 'Positive').sum())
        top_positive = reviews_df[reviews_df['sentiment'] == 'Positive'].nlargest(limit, 'polarity')[['Review', 'Date']]
        positive_dict = dict(zip(top_positive['Review'], top_positive['Date']))
    else:
        top_positive = "No positive comments from past 30 reviewers!"

    if (reviews_df['sentiment'] == 'Negative').sum() > 0:
        limit = min(5, (reviews_df['sentiment'] == 'Negative').sum())
        top_negative = reviews_df[reviews_df['sentiment'] == 'Negative'].nsmallest(limit, 'polarity')[['Review', 'Date']]
        negative_dict = dict(zip(top_negative['Review'], top_negative['Date']))
    else:
        top_negative = "No Negative comments from past 30 reviewers!"
        
    return positive_dict, negative_dict

# Example Usage
a = time.time()
positive_reviews, negative_reviews = App("debonairs", "surulere")
print("Positive Reviews: ", positive_reviews)
print("Negative Reviews: ", negative_reviews)
b = time.time()
print(b - a)
