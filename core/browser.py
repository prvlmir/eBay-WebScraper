from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

class BrowserConfig:
    def __init__(self, proxy=None):
        self.proxy = proxy
    
    
    def get_driver(self):
        chrome_options = Options()
        
        #Anti-Blocking basic settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        #Set default Window Size
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.page_load_strategy = 'eager' # Не чекаємо повного завантаження всіх скриптів
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        
        #Proxy support
        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
            print(f"[INFO] Launching browser with proxy: {self.proxy}")
        else:
            print("[INFO] Launching browser without proxy (local IP)")
            
        try:
            driver = webdriver.Chrome(options=chrome_options)
            
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                """
            })
            
            driver.maximize_window()
            return driver
        
        except Exception as e:
            print(f"[ERROR] Failed to launch browser {e}", file=sys.stderr)
            return None