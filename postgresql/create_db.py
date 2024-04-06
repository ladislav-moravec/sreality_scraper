import psycopg2

def create_database():
    # Připojení k defaultní databázi PostgreSQL (template1)
    conn = psycopg2.connect(
        dbname="template1",
        user="your_username",
        password="your_password",
        host="your_host"
    )
    cur = conn.cursor()

    # Vytvoření nové databáze s názvem sreality
    cur.execute("CREATE DATABASE sreality")

    # Uzavření spojení s template1 databází
    cur.close()
    conn.close()

def create_table():
    # Připojení k nově vytvořené databázi sreality
    conn = psycopg2.connect(
        dbname="sreality",
        user="your_username",
        password="your_password",
        host="your_host"
    )
    cur = conn.cursor()

    # Vytvoření tabulky estates, pokud ještě neexistuje
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estates (
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
        create_table()
        print("Tabulka estates byla úspěšně vytvořena.")
    except psycopg2.Error as e:
        print("Chyba při vytváření tabulky:", e)