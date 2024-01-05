#scrape link/picture/name/price

from ScraperClass import Scraper
from bs4 import BeautifulSoup
from selenium import webdriver #remove later / current use: testing
"""
scraper = Scraper()

should_scrape = True

counter = 0

while should_scrape:

    html = scraper.scrape_cycle(page=counter)

    soup = BeautifulSoup(html, "html.parser")

    all_lis = soup.find_all("li", {"class": "grid-tile"})

    count = 0

    for li in all_lis:

        links = li.find_all("a", {"class": "name-link"})

        if len(links) > 0:

            count += 1

            for link in links:
                print(link)

    if count > 0:

        counter += 25

    else:

        should_scrape = False
    """

scraper = Scraper()
html = scraper.scrape_cycle(page=1)
soup = BeautifulSoup(html, "html.parser")
all_lis = soup.find_all("li", {"class": "grid-tile"})  #####
driver = webdriver.Chrome()
item_links = []
image_classes = []
item_names = []
item_prices = []

for li in all_lis:
    links = li.find_all("a", {"class": "name-link"})

    for link in links:
        item_link = link["href"]
        item_links.append(item_link)

        print(item_links)

        break

        driver.get(item_link)

        image_class = soup.find("img", {"class": "primary-image"})
        image_classes.append(image_class)

        item_name = soup.find("h2", {"class": "product-name"})
        item_names.append(item_name)

        item_price = soup.find("span", {"class": "product-sales-price sales-price"})
        item_prices.append(item_price)

        break

print(item_links)
print(image_classes)
print(item_names)
print(item_prices)
print("done")