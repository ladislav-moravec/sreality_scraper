import psycopg2
import json

# Připojení k databázi
conn = psycopg2.connect(
    dbname="sreality",
    user="your_username",
    password="your_password",
    host="your_host"
)

# Vytvoření kurzoru pro provádění SQL příkazů
cur = conn.cursor()

# SQL příkaz pro vložení dat do tabulky
insert_query = """
INSERT INTO estates (name, price, image_urls) 
VALUES (%s, %s, %s);
"""

# JSON data
with open('data.json') as json_file:
    data = json.load(json_file)

# Procházení dat a vkládání do databáze
for estate in data['_embedded']['estates']:
    name = estate['name']
    price = estate['price']
    image_urls = json.dumps([img['href'] for img in estate['_links']['images']])
    cur.execute(insert_query, (name, price, image_urls))

# Potvrzení provedení změn v databázi
conn.commit()

# Uzavření spojení
cur.close()
conn.close()