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
        limit = self.config.get("pagination_limit", 10)
        selector = self.config["selectors"]["listing_links"]
        print(f"\n[INFO] Starting link collection for query: '{search_query}'")
        
        for page in range(1, limit + 1):
            url = base_url_template.replace("{query}", search_query).replace("{page}", str(page))
            print(f"[INFO] Navigation to page {page}/{limit}: {url}")
            
            try:
                time.sleep(3)
                self.driver.get(url)
                
                # Anti-Blocking: Hard 5-second wait + random delay
                time.sleep(5)
                time.sleep(random.uniform(3.0, 7.0))
                
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                page_links = []
                
                # Збираємо всі лінки з поточних елементів
                for el in elements:
                    link = el.get_attribute("href")
                    # Універсальний фільтр: просто перевіряємо, чи це валідне посилання
                    if link and link.startswith("http"):
                        clean_link = link.split("?")[0]
                        page_links.append(clean_link)
                        
                # Видаляємо дублікати для поточної сторінки
                page_links = list(set(page_links))
                all_links.extend(page_links)
                
                # РОЗУМНИЙ ЗАПОБІЖНИК ВІД АНТИБОТА
                if len(page_links) == 0:
                    if page == 1:
                        print(f"\n[🚨 WARNING] 0 links on page 1! Possible Anti-Bot block (eBay error page).")
                        print("Waiting 15 seconds... You can manually refresh the browser window to bypass it.")
                        time.sleep(15)
                        # Не зупиняємо цикл, даємо шанс парсеру піти на другу сторінку
                    else:
                        print(f"\n[INFO] No more products found on page {page}. Stopping pagination.")
                        break
                else:
                    print(f"[SUCCESS] Collected {len(page_links)} unique links from page {page}.")
        
            except Exception as e:
                print(f"[ERROR] Error on search page {url}: {type(e).__name__} - {e}", file=sys.stderr)
                continue
            
        final_links = list(set(all_links))
        print(f"\n[INFO] Phase 1 completed. Total unique product links found: {len(final_links)}")
        return final_links