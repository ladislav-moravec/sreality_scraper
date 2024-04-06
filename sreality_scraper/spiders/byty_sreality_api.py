import json
import requests
import requests

from sreality_scraper.sreality_scraper.postgresql.put_to_db import put_to_db


url = r"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=500"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    print("Počet nemovitostí:", data['result_size'])
else:
    print("Chyba při stahování dat:", response.status_code)


# Extract required information
for estate in data['_embedded']['estates']:
    title = estate['name']
    price = estate['price']
    image_urls = [img['href'] for img in estate['_links']['images']]

    print("Name:", title)
    print("Price:", price)
    print("Image URLs:", image_urls)
    print()

    put_to_db("sreality", title, price, image_urls)
