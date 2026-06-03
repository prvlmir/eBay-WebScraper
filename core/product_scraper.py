import time
import random
import sys
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class ProductScraper:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def scrape_products(self, urls):
        results = []
        selectors = self.config["selectors"]["product"]
        
        total_urls = len(urls)
        print(f"\n[INFO] Starting data extraction from product pages. Total URLs: {total_urls}")

        for index, url in enumerate(urls, 1):
            print(f"[INFO] ({index}/{total_urls}) Scraping: {url}")
            
            try:
                self.driver.get(url)
                
                # Anti-Blocking
                time.sleep(5)
                time.sleep(random.uniform(3.0, 7.0))

                item_data = {
                    "Title": "",
                    "Price": "",
                    "Currency": "",
                    "URL": url,
                    "Seller Name": "",
                    "Seller Link": "",
                    "Image URLs": ""
                }

                # 1. Title
                try:
                    title_el = self.driver.find_element(By.XPATH, selectors["title"])
                    item_data["Title"] = title_el.text.strip()
                except NoSuchElementException:
                    pass

                # 2. Price & Currency
                try:
                    price_el = self.driver.find_element(By.XPATH, selectors["price"])
                    raw_price = price_el.text.strip()
                    
                    price_match = re.search(r'([\d,\.]+)', raw_price)
                    if price_match:
                        item_data["Price"] = price_match.group(1)
                        item_data["Currency"] = raw_price.replace(item_data["Price"], "").strip()
                    else:
                        item_data["Price"] = raw_price
                except NoSuchElementException:
                    pass

                # 3. Seller Name
                try:
                    seller_name_el = self.driver.find_element(By.XPATH, selectors["seller_name"])
                    item_data["Seller Name"] = seller_name_el.text.strip()
                except NoSuchElementException:
                    pass

                # 4. Seller Link
                try:
                    seller_link_el = self.driver.find_element(By.XPATH, selectors["seller_link"])
                    item_data["Seller Link"] = seller_link_el.get_attribute("href")
                except NoSuchElementException:
                    pass

                # 5. Image URLs
                try:
                    image_els = self.driver.find_elements(By.XPATH, selectors["images"])
                    images = [img.get_attribute("src") for img in image_els if img.get_attribute("src")]
                    item_data["Image URLs"] = ", ".join(list(set(images)))
                except NoSuchElementException:
                    pass

                if item_data["Title"]:
                    results.append(item_data)
                    print(f"[SUCCESS] Scraped: {item_data['Title'][:40]}... | {item_data['Price']} {item_data['Currency']}")
                else:
                    print(f"[WARNING] Failed to find product title. Layout might have changed: {url}", file=sys.stderr)

            except Exception as e:
                print(f"[ERROR] Critical error on page {url}: {type(e).__name__} - {e}", file=sys.stderr)
                continue

        print(f"\n[INFO] Phase 2 completed. Successfully extracted data for {len(results)} items.")
        return results