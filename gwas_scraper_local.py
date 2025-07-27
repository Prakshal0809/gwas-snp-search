import time
import csv
import re
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from datetime import datetime

complement = {"A": "T", "T": "A", "C": "G", "G": "C"}

def parse_p_value(p_text):
    p_text = p_text.translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-"))
    p_text = p_text.lower().replace("x", "e").replace("×", "e").replace("−", "-").replace("–", "-").replace(" ", "")
    try:
        return float(p_text)
    except:
        match = re.search(r"(\d+(?:\.\d+)?)[^\d]*(10)[^\d\-]*(-?\d+)", p_text)
        if match:
            base, _, exponent = match.groups()
            return float(base) * 10**int(exponent)
    return None

def safe_click(driver, element, wait_time=10):
    """Safely click an element with multiple fallback methods"""
    try:
        # Wait for element to be clickable
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(element))
        
        # Try regular click first
        element.click()
        return True
    except ElementClickInterceptedException:
        try:
            # Try JavaScript click
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            try:
                # Try scrolling to element and clicking
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                element.click()
                return True
            except:
                try:
                    # Try clicking with offset
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    return True
                except:
                    return False
    except:
        return False

def run_gwas_scrape(search_term, progress_callback=None, max_pages=None):
    """
    Run GWAS scraping with progress updates - LOCAL VERSION
    
    Args:
        search_term (str): The search term to look for
        progress_callback (function): Callback function to update progress
        max_pages (int): Maximum number of pages to scrape (None for all pages)
    
    Returns:
        dict: Result with success status, count, filename, and error info
    """
    driver = None
    try:
        # Set up browser - optimized for local development
        options = Options()
        options.add_argument("--headless=new")  # Enable headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values": {
                "images": 2,
                "plugins": 2,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "media_stream": 2,
            }
        })
        
        # Use local ChromeDriver
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        wait = WebDriverWait(driver, 20)
        
        if progress_callback:
            progress_callback(10, f"Initializing browser...")
        
        if progress_callback:
            progress_callback(15, f"Navigating to GWAS database...")
        
        driver.get("https://www.ebi.ac.uk/gwas")
        time.sleep(1)  # Reduced wait time
        
        if progress_callback:
            progress_callback(20, f"Searching for '{search_term}'...")
        
        # Use original working search method
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-box")))
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for search to complete
        
        if progress_callback:
            progress_callback(25, "Checking search results...")
        
        # Check if there are no results found immediately after search
        try:
            # Wait a bit for the page to load after search
            time.sleep(3)  # Increased wait time
            
            if progress_callback:
                progress_callback(30, "Analyzing search results...")
            
            # Check for "No results found" message using multiple methods
            no_results_found = False
            
            # Method 1: Check page source for specific text - REMOVED because it's too broad
            # The page source contains hidden divs with "no results" text even when results exist
            # page_text = driver.page_source.lower()
            # if "no results found for search term" in page_text:
            #     no_results_found = True
            
            # Method 2: Look for specific elements with XPath - more precise
            if not no_results_found:
                try:
                    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'No results found for search term')]")
                    # Only consider visible elements
                    visible_elements = [elem for elem in elements if elem.is_displayed() and elem.get_attribute("style") != "display: none"]
                    if visible_elements:
                        no_results_found = True
                except:
                    pass
            
            # Method 3: Look for elements with specific classes
            if not no_results_found:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, ".no-results, .empty-results, [class*='no-results'], #noResults")
                    # Only consider visible elements
                    visible_elements = [elem for elem in elements if elem.is_displayed() and elem.get_attribute("style") != "display: none"]
                    if visible_elements:
                        no_results_found = True
                except:
                    pass
            
            # Method 4: Look for the specific noResults div - more precise
            if not no_results_found:
                try:
                    no_results_div = driver.find_element(By.ID, "noResults")
                    # Only consider it if it's actually displayed (not hidden)
                    if no_results_div.is_displayed() and no_results_div.get_attribute("style") != "display: none":
                        # Double-check that it contains the specific text
                        div_text = no_results_div.text.lower()
                        if "no results found for search term" in div_text:
                            no_results_found = True
                except:
                    pass
            
            if no_results_found:
                if progress_callback:
                    progress_callback(100, f"No results found for search term '{search_term}'")
                return {
                    'success': True,
                    'count': 0,
                    'filename': '',
                    'skipped_count': 0,
                    'pages_scraped': 0,
                    'error': None,
                    'no_results': True
                }
        
        except Exception as e:
            # If we can't check for no results, continue with normal flow
            pass
        
        # Wait for results and try to find clickable links
        try:
            # Wait for any results to appear, but with a shorter timeout
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr td a, .results a, a[href*='study']")))
                time.sleep(0.5)
            except TimeoutException:
                raise Exception("Search results did not load within expected time")
            
            # Try multiple selectors to find the right link
            selectors = [
                "table tbody tr td a",
                ".results a",
                "a[href*='study']",
                "a[href*='efotraits']"
            ]
            
            link_found = False
            for selector in selectors:
                try:
                    results = driver.find_elements(By.CSS_SELECTOR, selector)
                    for result in results:
                        if search_term.lower() in result.text.lower():
                            # Try to click the link safely
                            if safe_click(driver, result):
                                link_found = True
                                break
                    if link_found:
                        break
                except:
                    continue
            
            # If no specific match found, try clicking the first available link
            if not link_found:
                for selector in selectors:
                    try:
                        first_result = driver.find_element(By.CSS_SELECTOR, selector)
                        if safe_click(driver, first_result):
                            link_found = True
                            break
                    except:
                        continue
            
            if not link_found:
                raise Exception("Could not find or click on any search results")
                
        except TimeoutException:
            raise Exception("Search results did not load within expected time")
        
        time.sleep(1)  # Reduced wait time
        
        # Check pagination info to see if there are multiple pages
        try:
            pagination_info = driver.find_element(By.CSS_SELECTOR, ".dataTables_info, .pagination-info")
            if progress_callback:
                progress_callback(25, f"Pagination info: {pagination_info.text}")
        except:
            if progress_callback:
                progress_callback(25, "No pagination info found")
        
        snp_data = []
        skipped_studies = []
        page = 1
        
        while True:
            if progress_callback:
                if max_pages:
                    progress = 25 + (page / max_pages) * 60
                else:
                    progress = 25 + min((page / 50) * 60, 85)  # Assume max 50 pages for progress
                progress_callback(progress, f"Scraping page {page}...")
            
            # Use original working table method
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.dataTable tbody tr")))
            rows = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tbody tr")
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 10:
                    continue
                
                full_snp = cols[0].text.strip()
                p_text = cols[1].text.strip()
                beta = cols[5].text.strip()
                trait = cols[9].text.strip()
                
                if "?" in full_snp or "-" not in full_snp:
                    continue
                
                p_val = parse_p_value(p_text)
                if not p_val or p_val >= 5e-8:
                    continue
                
                try:
                    snp_id, risk = full_snp.split("-")
                    risk = risk.upper()
                    non_risk = complement.get(risk, "")
                    if not non_risk:
                        continue
                    
                    study_elem = cols[-2].find_element(By.TAG_NAME, "a")
                    ebi_link = study_elem.get_attribute("href")
                    
                    # Initialize default values
                    pubmed_link = "N/A"
                    doi = "N/A"
                    
                    # Try to extract PubMed ID and DOI
                    try:
                        driver.execute_script(f"window.open('{ebi_link}', '_blank');")
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)
                        
                        # Extract PubMed ID
                        try:
                            pubmed_id_elem = driver.find_element(By.CSS_SELECTOR, "#study-pubmedid a")
                            pubmed_id = pubmed_id_elem.text.strip()
                            pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}"
                        except:
                            # If PubMed ID not found, still continue but mark as N/A
                            pass
                        
                        # Navigate to PubMed and extract DOI using original method
                        if pubmed_link != "N/A":
                            try:
                                driver.get(pubmed_link)
                                time.sleep(2)  # Reduced wait time
                                
                                # Try multiple DOI selectors for better compatibility
                                doi_selectors = [
                                    "a[href*='doi.org']",
                                    "a[href*='doi.org/']",
                                    ".doi a",
                                    "[data-doi]",
                                    "a[title*='DOI']"
                                ]
                                
                                doi_found = False
                                for selector in doi_selectors:
                                    try:
                                        doi_elem = driver.find_element(By.CSS_SELECTOR, selector)
                                        doi = doi_elem.get_attribute("href")
                                        if doi and "doi.org" in doi:
                                            doi_found = True
                                            break
                                    except:
                                        continue
                                
                                if not doi_found:
                                    # Try with explicit wait as fallback
                                    try:
                                        doi_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='doi.org']")))
                                        doi = doi_elem.get_attribute("href")
                                    except:
                                        pass
                                        
                            except Exception as e:
                                # DOI not found, but that's okay
                                pass
                        
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                    except Exception as e:
                        # If there's any error with the study page, just continue with N/A values
                        if len(driver.window_handles) > 1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                    
                    # Always add the SNP data, even if PubMed/DOI extraction failed
                    snp_data.append({
                        "Primary SNP": full_snp,
                        "Risk Allele": risk,
                        "Non-risk Allele": non_risk,
                        "P-value": p_text,
                        "Beta": beta,
                        "Trait": trait,
                        "EBI Study Link": ebi_link,
                        "PubMed Link": pubmed_link,
                        "DOI": doi
                    })
                    
                    time.sleep(random.uniform(1.0, 2.0))
                    
                except Exception as e:
                    # Only add to skipped if there's a fundamental error with the SNP
                    skipped_studies.append(full_snp)
                    continue
            
            # Try clicking next using original method
            try:
                # Try multiple selectors for the Next button based on the actual HTML structure
                next_selectors = [
                    "#association-table-v2_next a",  # Click the anchor tag inside the li
                    "#association-table-v2_next",    # Click the li element itself
                    ".paginate_button.next a",       # Click anchor by class
                    ".paginate_button.next",         # Click li by class
                    "a[data-dt-idx='next']",         # Click by data attribute
                    "a[aria-controls='association-table-v2']",  # Click by aria attribute
                    ".next a",                       # Generic next anchor
                    ".next"                          # Generic next element
                ]
                
                next_btn = None
                for selector in next_selectors:
                    try:
                        next_btn = driver.find_element(By.CSS_SELECTOR, selector)
                        if progress_callback:
                            progress_callback(progress, f"Found Next button with selector: {selector}")
                        break
                    except:
                        continue
                
                if not next_btn:
                    if progress_callback:
                        progress_callback(90, "Could not find Next button - no more pages")
                    break
                
                next_btn_class = next_btn.get_attribute("class")
                if progress_callback:
                    progress_callback(progress, f"Next button class: {next_btn_class}")
                
                # Check if button is disabled (look for 'disabled' in class or aria-disabled attribute)
                is_disabled = "disabled" in next_btn_class or next_btn.get_attribute("aria-disabled") == "true"
                if is_disabled:
                    if progress_callback:
                        progress_callback(90, "Reached last page, no more SNPs to scrape")
                    break
                
                # Try to click the Next button
                if not safe_click(driver, next_btn):
                    if progress_callback:
                        progress_callback(90, "Could not click Next button")
                    break
                
                time.sleep(2)  # Wait for page to load
                page += 1
                if progress_callback:
                    progress_callback(progress, f"Successfully moved to page {page}")
                
                # Check if we've reached the max_pages limit
                if max_pages and page > max_pages:
                    if progress_callback:
                        progress_callback(90, f"Reached maximum page limit ({max_pages})")
                    break
                    
            except Exception as e:
                if progress_callback:
                    progress_callback(90, f"Pagination error: {str(e)}")
                break
        
        if progress_callback:
            progress_callback(90, "Saving results...")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{search_term.replace(' ', '_')}_snps_{timestamp}.csv"
        
        # Save to downloads folder
        downloads_dir = "downloads"
        os.makedirs(downloads_dir, exist_ok=True)
        filepath = os.path.join(downloads_dir, filename)
        
        # Write CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Primary SNP", "Risk Allele", "Non-risk Allele", "P-value", "Beta", "Trait", "EBI Study Link", "PubMed Link", "DOI"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in snp_data:
                writer.writerow(row)
        
        # Save skipped studies if any
        if skipped_studies:
            skipped_filename = f"skipped_snps_{timestamp}.csv"
            skipped_filepath = os.path.join(downloads_dir, skipped_filename)
            with open(skipped_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Skipped SNPs"])
                for snp in skipped_studies:
                    writer.writerow([snp])
        
        if progress_callback:
            progress_callback(100, f"Completed! Found {len(snp_data)} SNPs across {page} pages.")
        
        return {
            'success': True,
            'count': len(snp_data),
            'filename': filename,
            'skipped_count': len(skipped_studies),
            'pages_scraped': page,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'count': 0,
            'filename': '',
            'error': str(e)
        }
    finally:
        if driver:
            driver.quit()

# Legacy function for backward compatibility
def main():
    search_term = "facial wrinkling"
    result = run_gwas_scrape(search_term)
    if result['success']:
        print(f"✅ Done. Saved {result['count']} SNPs to '{result['filename']}'")
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main() 