import json
import csv
import os
import sys
from core.browser import BrowserConfig
from core.page_scraper import PageScraper
from core.product_scraper import ProductScraper

def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load config {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

def save_to_csv(data, filename):
    if not data:
        print("[WARNING] No data available to save.")
        return
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    keys = data[0].keys()
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys, quoting=csv.QUOTE_MINIMAL)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"\n[SUCCESS] Data successfully saved to file: {filename}")
    except Exception as e:
        print(f"[ERROR] Error saving CSV: {e}", file=sys.stderr)

def main():
    print("=== Starting Universal Web Scraper ===")
    
    # Вибір маркетплейсу перед запуском
    print("Select marketplace:")
    print("1 - eBay")
    print("2 - Alibaba")
    choice = input("Enter number (default is 1): ").strip()
    
    if choice == "2":
        config_path = os.path.join("config", "alibaba.json")
        print("[INFO] Alibaba configuration loaded.")
        site_prefix = "alibaba"
    else:
        config_path = os.path.join("config", "ebay.json")
        print("[INFO] eBay configuration loaded.")
        site_prefix = "ebay"
        
    config = load_config(config_path)
    
    # Proxy configuration
    browser_cfg = BrowserConfig(proxy=None) 
    driver = browser_cfg.get_driver()
    
    if not driver:
        print("[ERROR] Execution stopped due to browser initialization failure.", file=sys.stderr)
        return

    try:
        search_query = input("Enter search query (e.g., 'laptops' or 'iphone'): ")
        if not search_query.strip():
            search_query = "iphone"
            
        # Phase 1: Collect Links
        page_scraper = PageScraper(driver, config)
        product_links = page_scraper.get_product_links(search_query)
        
        if not product_links:
            print("[WARNING] No links found. Exiting.")
            return
            
        # Phase 2: Extract Data
        product_scraper = ProductScraper(driver, config)
        scraped_data = product_scraper.scrape_products(product_links)
        
        # Save results (використовуємо site_prefix)
        safe_query = search_query.strip().replace(" ", "_").lower()
        csv_filename = f"{site_prefix}_{safe_query}_output.csv"
        csv_path = os.path.join("data", csv_filename)

        save_to_csv(scraped_data, csv_path)
        
    finally:
        print("\n[INFO] Closing browser...")
        driver.quit()
        print("=== Execution Finished ===")
if __name__ == "__main__":
    main()