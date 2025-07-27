from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_page_content():
    # Set up browser
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        print("Navigating to GWAS database...")
        driver.get("https://www.ebi.ac.uk/gwas")
        time.sleep(2)
        
        print("Searching for 'diabetes'...")
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-box")))
        search_box.clear()
        search_box.send_keys("diabetes")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for page to load
        
        print("Checking page content...")
        page_source = driver.page_source
        page_text = page_source.lower()
        
        print(f"Page contains 'no results found': {'no results found' in page_text}")
        print(f"Page contains 'no results found for search term': {'no results found for search term' in page_text}")
        
        # Look for specific elements
        try:
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'No results found')]")
            print(f"Found {len(elements)} elements with 'No results found' text")
            for elem in elements:
                print(f"Element text: {elem.text}")
        except Exception as e:
            print(f"Error finding elements: {e}")
        
        # Check for the noResults div
        try:
            no_results_div = driver.find_element(By.ID, "noResults")
            print(f"Found noResults div, displayed: {no_results_div.is_displayed()}")
            print(f"noResults div text: {no_results_div.text}")
        except Exception as e:
            print(f"No noResults div found: {e}")
        
        # Check for results div
        try:
            results_div = driver.find_element(By.ID, "results")
            print(f"Found results div, displayed: {results_div.is_displayed()}")
            print(f"Results div text: {results_div.text[:200]}...")
        except Exception as e:
            print(f"No results div found: {e}")
        
        # Save page source for inspection
        with open("diabetes_page_content.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("Page source saved to diabetes_page_content.html")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_page_content() 