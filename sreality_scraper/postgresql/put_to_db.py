import psycopg2
import json


def put_to_db(table_name, title, price, image_urls):

    # connection
    conn = psycopg2.connect(
        dbname="master",
        user="postgres",
        password="asdf",
        host="localhost"
    )

    cur = conn.cursor()

    insert_query = f"""
    INSERT INTO {table_name} (title, price, image_urls) 
    VALUES (%s, %s, %s);
    """

    cur.execute(insert_query, (title, price, image_urls))

    # # JSON data
    # with open('data.json') as json_file:
    #     data = json.load(json_file)
    #
    # # Put in from json
    # for estate in data['_embedded']['estates']:
    #     title = estate['name']
    #     price = estate['price']
    #     image_urls = json.dumps([img['href'] for img in estate['_links']['images']])
    #     cur.execute(insert_query, (title, price, image_urls))

    conn.commit()

    cur.close()
    conn.close()

# test
# put_to_db("idnes_reality", "test_title", "price", "urls")