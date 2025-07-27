from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def debug_no_results_detection():
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
        
        print("Checking no results detection...")
        
        # Method 1: Check page source for specific text
        page_text = driver.page_source.lower()
        print(f"Page contains 'no results found for search term': {'no results found for search term' in page_text}")
        
        # Method 2: Look for specific elements with XPath
        try:
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'No results found for search term')]")
            print(f"Found {len(elements)} elements with 'No results found for search term' text")
            for i, elem in enumerate(elements):
                print(f"Element {i+1}: {elem.text}")
                print(f"  Displayed: {elem.is_displayed()}")
                print(f"  Style: {elem.get_attribute('style')}")
        except Exception as e:
            print(f"Error finding elements: {e}")
        
        # Method 3: Look for elements with specific classes
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, ".no-results, .empty-results, [class*='no-results'], #noResults")
            print(f"Found {len(elements)} elements with no-results classes")
            for i, elem in enumerate(elements):
                print(f"Element {i+1}: {elem.text}")
                print(f"  Displayed: {elem.is_displayed()}")
                print(f"  Style: {elem.get_attribute('style')}")
        except Exception as e:
            print(f"Error finding CSS elements: {e}")
        
        # Method 4: Look for the specific noResults div
        try:
            no_results_div = driver.find_element(By.ID, "noResults")
            print(f"Found noResults div:")
            print(f"  Text: {no_results_div.text}")
            print(f"  Displayed: {no_results_div.is_displayed()}")
            print(f"  Style: {no_results_div.get_attribute('style')}")
            
            # Check if it should be considered
            is_displayed = no_results_div.is_displayed()
            style = no_results_div.get_attribute("style")
            should_consider = is_displayed and style != "display: none"
            print(f"  Should consider: {should_consider}")
            
            if should_consider:
                div_text = no_results_div.text.lower()
                contains_text = "no results found for search term" in div_text
                print(f"  Contains 'no results found for search term': {contains_text}")
        except Exception as e:
            print(f"No noResults div found: {e}")
        
        # Check for results div
        try:
            results_div = driver.find_element(By.ID, "results")
            print(f"Found results div:")
            print(f"  Displayed: {results_div.is_displayed()}")
            print(f"  Style: {results_div.get_attribute('style')}")
            print(f"  Text preview: {results_div.text[:200]}...")
        except Exception as e:
            print(f"No results div found: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_no_results_detection() 