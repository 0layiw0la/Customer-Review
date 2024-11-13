import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

def WebScraper(business, location, driver_path='./chromedriver-win64/chromedriver.exe'):
    # Initialize WebDriver with headless option
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox (required for some environments)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--remote-debugging-port=9222")  # Optional, useful for debugging

    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver.get("https://www.google.com")
    
    # Search for the business name and location
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{business} {location} reviews")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  
    
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
            
        # Wait for the "Newest" filter to be clickable and click it
        newest_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-checked='false']//span[text()='Newest']"))
            )
        driver.execute_script("arguments[0].scrollIntoView(true);", newest_button)  # Ensure the button is in view
            
        # Use JavaScript to click the element directly if it's still not clickable
        driver.execute_script("arguments[0].click();", newest_button)

        review_limit = min(review_counts, 100)  # Limit to 100 reviews
        review_count = 0

        # Scroll and scrape reviews
        reviews_list = []
        for _ in range(25):  # Adjust scroll limit as needed
            time.sleep(3)
            rmcqnd_divs = driver.find_elements(By.CLASS_NAME, "Jtu6Td")
            scrollable_element = driver.find_element(By.CLASS_NAME, "review-dialog-list")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            
            # Parse each review element
            for div in rmcqnd_divs:
                div_soup = BeautifulSoup(div.get_attribute('outerHTML'), 'html.parser')
                
                # Check for full review text
                full_text_span = div_soup.find('span', class_='review-full-text')
                if full_text_span and full_text_span.get_text(strip=True):
                    text = full_text_span.get_text(strip=True)
                else:
                    # Look for alternative span if full review text is not found
                    alternative_text_span = div_soup.find('span', attrs={'data-expandable-section': True})
                    text = alternative_text_span.get_text(strip=True) if alternative_text_span else None

                # Append to list if text exists
                if text and text.strip():
                    if text not in reviews_list:
                        reviews_list.append(text)
                        review_count += 1
                        if review_count >= review_limit:
                            break
            if review_count >= review_limit:
                break

        # Close the driver
        driver.quit()

        # Convert the list into a DataFrame
        reviews_df = pd.DataFrame(reviews_list, columns=["Review"])

        return reviews_df
    
    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        return pd.DataFrame()  # Return empty DataFrame on error

#Example Usage
#df = WebScraper("film house cinema",'surulere')