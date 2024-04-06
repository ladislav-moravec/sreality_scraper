import psycopg2
import json


def put_to_db(title, price, image_urls):
    # Připojení k databázi
    conn = psycopg2.connect(
        dbname="master",
        user="postgres",
        password="asdf",
        host="localhost"
    )

    # Vytvoření kurzoru pro provádění SQL příkazů
    cur = conn.cursor()

    # SQL příkaz pro vložení dat do tabulky
    insert_query = """
    INSERT INTO sreality (title, price, image_urls) 
    VALUES (%s, %s, %s);
    """

    # JSON data
    with open('data.json') as json_file:
        data = json.load(json_file)

    # Procházení dat a vkládání do databáze
    for estate in data['_embedded']['estates']:
        title = estate['name']
        price = estate['price']
        image_urls = json.dumps([img['href'] for img in estate['_links']['images']])
        cur.execute(insert_query, (title, price, image_urls))

    # Potvrzení provedení změn v databázi
    conn.commit()

    # Uzavření spojení
    cur.close()
    conn.close()
