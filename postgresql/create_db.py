import psycopg2

def create_database():
    # Připojení k defaultní databázi PostgreSQL (template1)
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="asdf",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Vytvoření nové databáze s názvem sreality
    cur.execute("CREATE DATABASE master")

    # Uzavření spojení s template1 databází
    cur.close()
    conn.close()

def create_table(name_table):
    # Připojení k nově vytvořené databázi sreality
    conn = psycopg2.connect(
        dbname="master",
        user="postgres",
        password="asdf",
        host="localhost"
    )
    cur = conn.cursor()

    # Vytvoření tabulky estates, pokud ještě neexistuje
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {name_table} (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        price INTEGER,
        image_urls JSONB
    );
    """)

    # Potvrzení provedení změn v databázi
    conn.commit()

    # Uzavření spojení
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
        print("Databáze sreality byla úspěšně vytvořena.")
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
