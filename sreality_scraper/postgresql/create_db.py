import psycopg2

def create_database():
    conn = psycopg2.connect(
        dbname="master",
        user="postgres",
        password="asdf",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("CREATE DATABASE master")

    cur.close()
    conn.close()

def create_table(name_table):
    conn = psycopg2.connect(
        dbname="master",
        user="postgres",
        password="asdf",
        host="localhost"
    )
    cur = conn.cursor()

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {name_table} (
        id SERIAL PRIMARY KEY,
        title VARCHAR,
        price VARCHAR,
        image_urls TEXT
    );
    """)

    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
        print("Databáze master byla úspěšně vytvořena.")
    except psycopg2.Error as e:
        print("Chyba při vytváření databáze:", e)

    try:
        create_table("sreality")
        print("Tabulka sreality byla úspěšně vytvořena nebo již existuje.")
    except psycopg2.Error as e:
        print("Chyba při vytváření tabulky:", e)

    try:
        create_table("idnes_reality")
        print("Tabulka idnes_reality byla úspěšně vytvořena nebo již existuje.")
    except psycopg2.Error as e:
        print("Chyba při vytváření tabulky:", e)
