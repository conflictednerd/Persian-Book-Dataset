import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PageParser():
    def __init__(self, driver: webdriver, debug=False, max_wait=5) -> None:
        self.driver = driver
        self.debug = debug
        self.max_wait = max_wait
        self.PROBLEM = False

    def parse(self, url: str = None):
        """
        Parses a book page and returns a dictionary of the book's information, along with a flag indicating whether there was a problem.
        """
        self.PROBLEM = False
        if url is not None:
            self.driver.get(url)
            time.sleep(2)

        return {
            'url': self.driver.current_url,
            'title': self.get_title(),
            'authors': self.get_authors(),
            'image_path': self.get_image_path(),
            'publisher': self.get_publisher(),
            'ISBN': self.get_ISBN(),
            'pages': self.get_pages(),
            'publication_count': self.get_publication_count(),
            'publication_date': self.get_publication_date(),
            'genres': self.get_genres(),
            'description': self.get_description(),
            'ratings': self.get_ratings(),
        }, self.PROBLEM

    def get_title(self, mode='a') -> str:
        """
        Returns the title of the book
        """
        title = ''
        try:
            title = WebDriverWait(self.driver, self.max_wait).until(EC.visibility_of_element_located(
                (By.XPATH,
                 f'/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/div/div[1]/{mode}'
                 )
            )).text
        except Exception as e:
            if mode == 'a':
                title = self.get_title(mode='h1')
                if title == '':
                    self.PROBLEM = True
            if title == '' and self.debug:
                print('Title not found')
                print(e)
        finally:
            return title

    def get_authors(self) -> List[str]:
        """
        Returns a list of authors
        If fails, returns an empty list
        """
        authors = []
        try:
            author_list_element = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/div/div[2]'
                 )
            ))
            authors = [
                author.text for author in author_list_element.find_elements_by_tag_name('span')]
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Authors not found')
                print(e)
        finally:
            return authors

    def get_image_path(self) -> str:
        """
        Returns the path to the image of the book
        """
        image_path = ''
        try:
            image_path = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-information/div/img'
                 )
            )).get_attribute('src')
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Image path not found')
                print(e)
        finally:
            return image_path

    def get_genres(self) -> List[str]:
        """
        Returns a list of genres
        If fails, returns an empty list
        """
        genres = []
        try:
            genre_list_element = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/app-book-genre-list/swiper/div/div[1]'
                 )
            ))
            time.sleep(0.5)
            genres = [
                genre.text for genre in genre_list_element.find_elements_by_tag_name('span')]
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Genres not found')
                print(e)
        finally:
            return genres

    def get_description(self) -> str:
        """
        Returns the description of the book
        """
        description = ''
        try:
            description = self.driver.find_elements(by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/pre') + self.driver.find_elements(
                by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/div[2]/pre') + self.driver.find_elements(by=By.XPATH, value='/html/body/app-root/layout/section/main/book-detail/section/div[2]/div/p')
            description = description[0].text
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Description not found')
                print(e)
        finally:
            return description

    def get_ratings(self) -> List[int]:
        """
        Returns a five-element list of ratings, where the i-th element is the number of people who rated the book with i stars.
        If fetching the  
        """
        ratings = []
        try:
            ratings = [
                int(
                    WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/app-root/layout/section/main/book-detail/section/app-book-detail-reviews/section/div[2]/div[2]/div[{i}]/div[2]/p'
                         )
                    )).text)
                for i in range(1, 6)
            ]

        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Ratings not found')
                print(e)
        finally:
            return ratings[::-1]

    def get_publisher(self) -> str:
        """
        Returns the publisher of the book
        """
        publisher = ''
        try:
            publisher = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[1]/div[2]/a/span'
                 )
            )).text
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Publisher not found')
                print(e)
        finally:
            return publisher

    def get_ISBN(self) -> str:
        """
        Returns the ISBN of the book
        """
        ISBN = ''
        try:
            ISBN = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[2]/div[2]/span'
                 )
            )).text
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('ISBN not found')
                print(e)
        finally:
            return ISBN

    def get_pages(self) -> int:
        """
        Returns the number of pages of the book
        """
        pages = 0
        try:
            pages = int(''.join(filter(str.isdigit, WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[3]/div[2]/span'
                 )
            )).text)))
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Pages not found')
                print(e)
        finally:
            return pages

    def get_publication_count(self) -> int:
        """
        Returns the number of times the book was published
        """
        publication_count = 0
        try:
            publication_count = int(WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[4]/div[2]/span'
                 )
            )).text)
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Publication count not found')
                print(e)
        finally:
            return publication_count

    def get_publication_date(self) -> str:
        """
        Returns the publication date of the book
        """
        publication_date = ''
        try:
            publication_date = WebDriverWait(self.driver, self.max_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/app-root/layout/section/main/book-detail/section/div[3]/div[2]/div[5]/div[2]/span'
                 )
            )).text
        except Exception as e:
            self.PROBLEM = True
            if self.debug:
                print('Publication date not found')
                print(e)
        finally:
            return publication_date
