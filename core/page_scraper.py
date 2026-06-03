import time
import random
import sys
from selenium.webdriver.common.by import By

class PageScraper:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        
    def get_product_links(self, search_query):
        all_links = []
        base_url_template = self.config.get("search_url_template")
        limit = self.config.get("pagination_limit", 1)
        selector = self.config["selectors"]["listing_links"]
        print(f"\n[INFO] Starting link collection for query: '{search_query}'")
        
        for page in range(1, limit + 1):
            url = base_url_template.replace("{query}", search_query).replace("{page}", str(page))
            print(f"[INFO] Navigation to page {page}/{limit}: {url}")
            
            try:
                self.driver.get(url)
                
                #Anti-Blocking: Hard 5-secong wait + random delay
                time.sleep(5)
                time.sleep(random.uniform(3.0, 7.0))
                
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                page_links = []
                
                for el in elements:
                    link = el.get_attribute("href")
                    #Filter valid eBay items
                    if link and "/itm/" in link:
                        clean_link = link.split("?")[0]
                        page_links.append(clean_link)
                        
                    #remove duplicates
                    page_links = list(set(page_links))
                    all_links.extend(page_links)
                    
                    
                    print(f"[SUCCESS] Collected {len(page_links)} unique links from page {page}.")
            
            except Exception as e:
                print(f"[ERROR] Error on search page {url}: {type(e).__name__} - {e}", file=sys.stderr)
                continue
            
        final_links = list(set(all_links))
        print(f"\n[INFO] Phase 1 completed. Total unique product links found: {len(final_links)}")
        return final_links                
        