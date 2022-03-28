from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_options():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless") # Uncomment to run
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument('--disable-gpu') # Uncomment this line if running windows
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "--blink-settings=imagesEnabled=false"
    )
    return chrome_options



if __name__ == "__main__":
    chrome_options = get_options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com/")
    driver.quit()