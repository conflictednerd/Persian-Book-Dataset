# Scraping book information from the Internet

Some time ago, I wanted to experiment a bit with book recommendation systems. I did not find any good Persian dataset of books, along with their information (title, authors, translators, ratings, etc.). There were some English ones, mainly scraped from GoodReads lists, but I didn't like them either. So I decided to create a Persian dataset of books and learn how to use selenium for web scraping along the way, which is something I wanted to learn for quite some time.

So, this is how this repository was born:)

So far I have written some code to extract an individual book's information from its webpage. In particular I extract:

+ URL
+ Title
+ Authors and Translators
+ ISBN
+ Genres
+ Publisher
+ Publication date
+ Publication count
+ Ratings
+ Number of pages
+ Description
+ Image URL

This code scraps data from [this website](https://behkhaan.ir/).

~~In the future, I should also add a crawler to automatically extract the URL of book pages and use it along with the current code to create a dataset.~~  
UPDATE: **Dataset creation is finished.** Using 24 threads of execution, it took ~4 hours to scrape 26,202 records. The dataset is stored in `books.json` and can also be downloaded from the zip file in the `data` directory.

Then perhaps a little bit of cleaning, removing duplicated and such, and that will be it.

I have some vague ideas of creating a graph from this dataset and run some GNNs on it, but there is no time for them now, so maybe in some distant future!

