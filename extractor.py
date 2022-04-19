import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_lists(driver: webdriver.Chrome, url: str = None):
    '''
    Extracts the URL of every genre list
    '''
    if url is not None:
        driver.get(url)
        time.sleep(7)

    links = [
        a.get_attribute('href') for a in driver.find_elements(By.XPATH, '//a[@href]')
    ]
    return [a for a in links if '/genre/' in a]


def parse_list(driver: webdriver.Chrome, list_url: str = None):
    '''
    Given the URL of a genre list, returns the URL of every book in that list.
    '''
    if list_url is not None:
        driver.get(list_url)

    # scroll down to load the list completely
    for _ in range(0, 240):
        driver.find_element(By.XPATH, '/html/body').send_keys(Keys.END)
        time.sleep(0.7)

    # extract book urls
    book_urls = []
    try:
        for i in range(1, 20_000):
            book_urls.append(
                driver.find_element(
                    By.XPATH, f'/html/body/app-root/layout/section/main/app-genre-books/section/main/div/div[{i}]/div[1]/a').get_attribute('href')
            )
    except:
        print(i)
    finally:
        return book_urls
