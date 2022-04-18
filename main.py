import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm.auto import tqdm
from tqdm.contrib import tenumerate

from extractor import get_lists, parse_list
from page_parser import parse_book_page

EXTRACT_LINKS = False


def get_options():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")  # Uncomment to run
    chrome_options.add_argument("--no-sandbox")
    # Uncomment this line if running windows
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "--blink-settings=imagesEnabled=false"
    )
    chrome_options.add_argument('log-level=3')
    return chrome_options


if __name__ == "__main__":
    chrome_options = get_options()
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Extraction of links
        if EXTRACT_LINKS:
            lists = get_lists(driver, 'https://behkhaan.ir/genre')
            book_urls = []
            for list_url in lists:
                book_urls.extend(parse_list(driver, list_url))
            book_urls = list(set(book_urls))
            print(f'extracted the urls for {len(book_urls)} unique books')
            with open('book_urls.json', 'w') as f:
                json.dump(book_urls, f, indent=4, ensure_ascii=False)
        else:
            with open('book_urls.json', 'r') as f:
                book_urls = json.load(f)

        books = []
        failed_urls = []
        # for i, url in enumerate(tqdm(book_urls, position=0, leave=True)):
        for i, url in enumerate(book_urls):
            if i % 100 == 99:
                print(f'{i+1}/{len(book_urls)}')
                print(f'Failures: {len(failed_urls)}')
                print(
                    f'Success rate: {100 - (len(failed_urls) / (i+1)) * 100:.2f}%')
                with open('books.json', 'w', encoding='utf-8') as f:
                    json.dump(books, f, indent=4, ensure_ascii=False)
            try:
                book, problem_flag = parse_book_page(driver, url)
                books.append(book)
                if problem_flag:
                    failed_urls.append(url)
            except:
                failed_urls.append(url)

        with open('failed_urls.json', 'w', encoding='utf-8') as f:
            json.dump(failed_urls, f, indent=4, ensure_ascii=False)

        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(books, f, indent=4, ensure_ascii=False)
    finally:
        driver.quit()

# load books
# multi processing
