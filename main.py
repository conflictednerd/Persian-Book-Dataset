import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from extractor import get_lists, parse_list
from page_parser import PageParser

EXTRACT_LINKS = False
NUM_WORKERS = 24


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


def func(parser, urls, ID):
    global start_time
    books, failed_urls = [], []
    batch_size = 20
    for i, url in enumerate(urls):
        if ID < 4 and i % batch_size == batch_size-1:
            print(f'(ID: {ID}) [{i+1}/{len(urls)}] Failures: {len(failed_urls)} Success rate: {100 - (len(failed_urls) / (i+1)) * 100:.2f}% time/iter: {(time() - start_time) / (i+1):.2f}s')
        try:
            book, problem_flag = parser.parse(url)
            books.append(book)
            if problem_flag:
                failed_urls.append(url)
        except:
            failed_urls.append(url)
    return books, failed_urls


def run_workers(urls, num_workers):
    chunk_size = len(urls) // num_workers + 1
    chunks = [urls[i:i+chunk_size] for i in range(0, len(urls), chunk_size)]
    drivers = [webdriver.Chrome(options=get_options())
               for _ in range(num_workers)]
    parsers = [PageParser(driver) for driver in drivers]
    all_books, all_failed_urls = [], []
    print(f'Running {num_workers} workers')
    global start_time
    start_time = time()
    try:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for future in as_completed([executor.submit(func, parser, chunk, ID) for ID, (parser, chunk) in enumerate(zip(parsers, chunks))]):
                books, failed_urls = future.result()
                all_books.extend(books)
                all_failed_urls.extend(failed_urls)
                print('Worker finished!')
    finally:
        [driver.quit() for driver in drivers]
    return all_books, all_failed_urls


if __name__ == "__main__":
    # Extraction of links
    if EXTRACT_LINKS:
        chrome_options = get_options()
        driver = webdriver.Chrome(options=chrome_options)
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
    # Run workers
    books, failed_urls = run_workers(book_urls, NUM_WORKERS)
    print('FINISHED\n')
    print('-'*100)
    print()
    print(f'Failures: {len(failed_urls)}')
    print(
        f'Success rate: {100 - (len(failed_urls) / len(book_urls)) * 100:.2f}%')

    with open('failed_urls.json', 'w', encoding='utf-8') as f:
        json.dump(failed_urls, f, indent=4, ensure_ascii=False)

    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=4, ensure_ascii=False)
