# webscraping.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

def WebScraper(business, location, driver_path=r'.\chromedriver-win64\chromedriver.exe'):
    # Set up the Chrome WebDriver with options for headless browsing (no GUI)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(driver_path, options=options)

    # Navigate to Google's homepage
    driver.get("https://www.google.com")
    
    # Locate the search box and input the business and location search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{business} {location} reviews")
    search_box.send_keys(Keys.RETURN)  # Press Enter to search
    time.sleep(1.5)  # Wait for the results to load
    
    try:
        # Wait for the review button to be clickable, then extract the review count
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-async-trigger='reviewDialog']"))
        )
        
        review_text = review_button.text
        review_counts_str = review_text.split(" Google reviews")[0].replace(",", "")
        review_counts = int(review_counts_str)  # Convert the review count to an integer
        
        review_button.click()  # Click on the review button to open the review dialog
        time.sleep(1)  # Wait for the reviews to load
        
        # Extract the average rating from the page
        avg_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text.strip()
        
        # Click on the "Newest" reviews tab to sort reviews by newest first
        newest_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-checked='false']//span[text()='Newest']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", newest_button)  # Scroll to the button
        driver.execute_script("arguments[0].click();", newest_button)  # Click to sort reviews by newest
        time.sleep(2)  # Wait for the reviews to load
        
        review_limit = min(review_counts, 25)  # Limit the number of reviews to 25 or the total count
        review_count = 0  # Initialize the review count
        
        # Initialize lists to store the review text and dates
        reviews_list = []
        date_list = []
        
        # Loop through and scrape reviews until the limit is reached
        while review_count < review_limit:
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
                    # Parse the review container with BeautifulSoup
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
                        reviews_list.append(text)  # Add the review text to the list
                        date_list.append(date)  # Add the date to the list
                        review_count += 1  # Increment the review count

                    # Stop if the review limit is reached
                    if review_count >= review_limit:
                        break
                except Exception as e:
                    print(f"Error while processing review: {e}")  # Log any errors while processing a review

            # Stop if the review limit is reached
            if review_count >= review_limit:
                break

        driver.quit()  # Close the WebDriver once done scraping

        # Create a DataFrame to store the reviews and dates
        reviews_df = pd.DataFrame({
            "Review": reviews_list,
            "Date": date_list
        })
        
        return reviews_df, avg_rating  # Return the DataFrame and the average rating
    
    except Exception as e:
        driver.quit()  # Close the WebDriver in case of an error
        return None, None  # Return None if there was an error during scraping
