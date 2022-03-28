import time
from pprint import pprint
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from main import get_options

MAX_ELEMENT_WAIT_TIME = 5
DEBUG = True


def parse_book_page(driver, url: str = None):
    """
    Parses a book page and returns a dictionary with the following keys:
    """
    if url is not None:
        driver.get(url)

    return {
        'url': driver.current_url,
        'title': get_title(driver),
        'image_path': get_image_path(driver),
        'publisher': get_publisher(driver),
        'ISBN': get_ISBN(driver),
        'pages': get_pages(driver),
        'publication_count': get_publication_count(driver),
        'publication_date': get_publication_date(driver),
        'authors': get_authors(driver),
        'genres': get_genres(driver),
        'description': get_description(driver),
        'ratings': get_ratings(driver),
    }


def get_title(driver) -> str:
    """
    Returns the title of the book
    """
    title = ''
    try:
        title = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.visibility_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/div/div[1]/a'
             )
        )).text
    except Exception as e:
        if DEBUG:
            print('Title not found')
            print(e)
    finally:
        return title


def get_authors(driver) -> List[str]:
    """
    Returns a list of authors
    If fails, returns an empty list
    """
    authors = []
    try:
        author_list_element = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/div/div[2]'
             )
        ))
        authors = [
            author.text for author in author_list_element.find_elements_by_tag_name('span')]
    except Exception as e:
        if DEBUG:
            print('Authors not found')
            print(e)
    finally:
        return authors


def get_image_path(driver) -> str:
    """
    Returns the path to the image of the book
    """
    image_path = ''
    try:
        image_path = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/img'
             )
        )).get_attribute('src')
    except Exception as e:
        if DEBUG:
            print('Image path not found')
            print(e)
    finally:
        return image_path


def get_genres(driver) -> List[str]:
    """
    Returns a list of genres
    If fails, returns an empty list
    """
    genres = []
    try:
        genre_list_element = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/app-book-genre-list/swiper/div/div[1]'
             )
        ))
        time.sleep(0.5)
        genres = [
            genre.text for genre in genre_list_element.find_elements_by_tag_name('span')]
    except Exception as e:
        if DEBUG:
            print('Genres not found')
            print(e)
    finally:
        return genres


def get_description(driver) -> str:
    """
    Returns the description of the book
    """
    description = ''
    try:
        description = driver.find_elements(by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/pre') + driver.find_elements(
            by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/div[2]/pre') + driver.find_elements(by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/p')
        description = description[0].text
    except Exception as e:
        if DEBUG:
            print('Description not found')
            print(e)
    finally:
        return description


def get_ratings(driver) -> List[int]:
    """
    Returns a five-element list of ratings, where the i-th element is the number of people who rated the book with i stars.
    If fetching the  
    """
    ratings = []
    try:
        ratings = [
            int(
                WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
                    (By.XPATH,
                     f'/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-reviews/section/div[2]/div[2]/div[{i}]/div[2]/p'
                     )
                )).text)
            for i in range(1, 6)
        ]

    except Exception as e:
        if DEBUG:
            print('Ratings not found')
            print(e)
    finally:
        return ratings[::-1]


def get_publisher(driver) -> str:
    """
    Returns the publisher of the book
    """
    publisher = ''
    try:
        publisher = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[1]/div[2]/a/span'
             )
        )).text
    except Exception as e:
        if DEBUG:
            print('Publisher not found')
            print(e)
    finally:
        return publisher


def get_ISBN(driver) -> str:
    """
    Returns the ISBN of the book
    """
    ISBN = ''
    try:
        ISBN = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[2]/div[2]/span'
             )
        )).text
    except Exception as e:
        if DEBUG:
            print('ISBN not found')
            print(e)
    finally:
        return ISBN


def get_pages(driver) -> int:
    """
    Returns the number of pages of the book
    """
    pages = 0
    try:
        pages = int(WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[3]/div[2]/span'
             )
        )).text)
    except Exception as e:
        if DEBUG:
            print('Pages not found')
            print(e)
    finally:
        return pages


def get_publication_count(driver) -> int:
    """
    Returns the number of times the book was published
    """
    publication_count = 0
    try:
        publication_count = int(WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[4]/div[2]/span'
             )
        )).text)
    except Exception as e:
        if DEBUG:
            print('Publication count not found')
            print(e)
    finally:
        return publication_count


def get_publication_date(driver) -> str:
    """
    Returns the publication date of the book
    """
    publication_date = ''
    try:
        publication_date = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[5]/div[2]/span'
             )
        )).text
    except Exception as e:
        if DEBUG:
            print('Publication date not found')
            print(e)
    finally:
        return publication_date


if __name__ == '__main__':
    urls = ['https://behkhaan.ir/book/023f6e23-a89c-465e-9503-883be354c181',  # Shazde
            'https://behkhaan.ir/book/2bf05adf-719d-4050-a05e-d58d43aa2ee8',  # Natoor
            'https://behkhaan.ir/book/3292dcca-3634-4ca7-8277-551fc3b2d5fe',  # Aghayed
            'https://behkhaan.ir/book/9df25320-e93e-4327-86bc-12f26ca89cb1',
            'https://behkhaan.ir/book/86494391-ee6b-4327-b1a5-b279fe2e5fb3',
            ]
    options = get_options()
    driver = webdriver.Chrome(options=options)
    try:
        for url in urls:
            pprint(parse_book_page(driver, url))
    finally:
        driver.quit()
