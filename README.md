# Universal Web Scraper (eBay, Alibaba, OLX)

A simple and effective multi-platform Python web scraper built with Selenium. It extracts product data from major e-commerce sites like eBay, Alibaba, and OLX. It uses `undetected-chromedriver` to bypass bot protection and saves the results in clean CSV files.

## Features
- **Multi-Platform Support:** Choose which marketplace to scrape (eBay or Alibaba) directly from the terminal menu.
- **Anti-Bot Protection & Smart Safeguards:** Bypasses standard blocks. If a marketplace (like eBay) shows a block on the first page, the scraper automatically pauses for 15 seconds, giving you a chance to manually refresh the page and bypass the system!
- **Smart Pagination:** Automatically navigates through search result pages and stops smartly when the products run out.
- **Dynamic CSV Export:** Saves data dynamically based on the target website and your search query (e.g., `ebay_laptops_output.csv` or `alibaba_iphone_output.csv`).
- **Modular Configuration:** Uses separate JSON files (`ebay.json`, `alibaba.json`, `olx.json`) to store CSS/XPath selectors. You don't need to touch the Python code if a website layout changes.

## Installation

1. Clone this repository:
git clone https://github.com/prvlmir/eBay-WebScraper.git
cd eBay-WebScraper

2. Create a virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

## How to Use

1. Run the main script:
python main.py

2. Select the target marketplace from the terminal menu (1 for eBay, 2 for OLX, 3 for Alibaba).
3. Enter your search query (for example: `laptops` or `iphone`).
4. The browser will open automatically and start collecting data. (If you hit an Anti-Bot block on the first page, just hit F5 in the browser while the script waits).
5. Once finished, find your results in the `data/` folder.

## Configuration

If you need to change the selectors, update the website link, or increase the number of pages to scrape, just edit the corresponding file in the `config/` folder (e.g., `config/ebay.json`).

To use a proxy, open `main.py` and update the proxy settings:
browser_cfg = BrowserConfig(proxy="your_proxy_ip:port")
