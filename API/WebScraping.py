# webscraping.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import chromedriver_autoinstaller  

def WebScraper(business, location):
    # Automatically installing chromedriver and getting the path
    driver_path = chromedriver_autoinstaller.install()

    # Setting up headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(driver_path, options=options)
    wait = WebDriverWait(driver, 10)

    # Searching for business name and location on google
    driver.get("https://www.google.com")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{business} {location} reviews")
    search_box.send_keys(Keys.RETURN)  

    time.sleep(1.5)  # Waiting for the results to load incase of poor network
    
    try:
        # Wait for the review button to be clickable, then extracting the review count
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-async-trigger='reviewDialog']"))
        )
        
        review_text = review_button.text
        review_counts_str = review_text.split(" Google reviews")[0].replace(",", "")
        review_counts = int(review_counts_str) 
        
        review_button.click()  # Opening the review dialog
        time.sleep(1)  # Waiting incase of network
        
        # Extracting the average rating 
        avg_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text.strip()
        
        # Filter to newest tab to sort reviews by newest first
        newest_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-checked='false']//span[text()='Newest']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", newest_button)  
        driver.execute_script("arguments[0].click();", newest_button)  # Click to sort reviews by newest
        time.sleep(2)  # Wait for the reviews to load incase of network
        
        review_limit = min(review_counts, 25)  # Limit the number of reviews to 25 or the total count
        review_count = 0  # Initialize the review count to avoid infinite loop
        
        # lists to store the review text and dates
        reviews_list = []
        date_list = []
        
        max_scroll_attempts = 10  #maximum number of scroll attempts
        scroll_attempts = 0

        # Loop through and scrape reviews until the limit is reached
        while review_count < review_limit and scroll_attempts < max_scroll_attempts:
            # Wait for the reviews to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "BgXiYe"))
            )
            
            # Find all review containers on the page
            review_containers = driver.find_elements(By.CLASS_NAME, "BgXiYe")
            scrollable_element = driver.find_element(By.CLASS_NAME, "review-dialog-list")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)  # Scroll down to load more reviews

            # Wait again for the newly loaded reviews
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "BgXiYe"))
            )

            # Loop through the review containers and extract review data
            for container in review_containers:
                try:
                    
                    container_soup = BeautifulSoup(container.get_attribute('outerHTML'), 'html.parser')

                    # Extract the date of the review
                    date_span = container_soup.find('span', class_="dehysf lTi8oc")
                    date = date_span.get_text(strip=True) if date_span else None

                    # Extract the review text
                    full_text_span = container_soup.find('span', class_='review-full-text')
                    if full_text_span and full_text_span.get_text(strip=True):
                        text = full_text_span.get_text(strip=True)
                    else:
                        alternative_text_span = container_soup.find('span', attrs={'data-expandable-section': True})
                        text = alternative_text_span.get_text(strip=True) if alternative_text_span else None

                    # Ensure the review text is valid and hasn't been added already
                    if text and text.strip() and text not in reviews_list:
                        reviews_list.append(text)  
                        date_list.append(date)  
                        review_count += 1  

                    # Stop once review limit is reached
                    if review_count >= review_limit:
                        break
                except Exception as e:
                    print(f"Error while processing review: {e}")  # Logging any errors while processing a review

            # Stop if the review limit is reached
            if review_count >= review_limit:
                break

            scroll_attempts+=1

        driver.quit()  # Closing the WebDriver once done scraping

        # DataFrame to store the reviews and dates
        reviews_df = pd.DataFrame({
            "Review": reviews_list,
            "Date": date_list
        })
        
        return reviews_df, avg_rating  
    
    except Exception as e:
        driver.quit()  # Closing the WebDriver in case of an error
        return None, None  # Returning None if there was an error during scraping
