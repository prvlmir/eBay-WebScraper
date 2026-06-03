# eBay Web Scraper

A simple and effective Python web scraper built with Selenium to extract product data from eBay. It uses `undetected-chromedriver` to bypass bot protection and saves the results in a clean CSV file.

## Features
- **Anti-Bot Protection:** Bypasses standard eBay blocks and captchas.
- **Pagination Support:** Automatically navigates through search result pages to collect more items.
- **CSV Export:** Saves data (Title, Price, Currency, Links, Images) dynamically based on your search query.
- **Easy Configuration:** Uses a JSON file to store selectors, so you don't need to change the Python code if the website layout changes.

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

2. Enter your search query (for example: `laptops` or `nike`).
3. The browser will open automatically and start collecting data.
4. Once finished, find your results in the `data/` folder (e.g., `data/laptops_output.csv`).

## Configuration

If you need to change the CSS/XPath selectors or the number of pages to scrape, just edit the `config/ebay.json` file. 

To use a proxy, open `main.py` and update the proxy settings:
browser_cfg = BrowserConfig(proxy="your_proxy_ip:port")
