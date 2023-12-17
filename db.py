import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env.local")
load_dotenv(dotenv_path)


def connect():
    try:
        con = psycopg2.connect(
            host=os.environ.get("DATABASE_HOSTNAME"),
            dbname=os.environ.get("DATABASE_NAME"),
            user=os.environ.get("DATABASE_USERNAME"),
            password=os.environ.get("DATABASE_PASSWORD"),
            port=os.environ.get("DATABASE_PORT"),
        )
        return con, con.cursor()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
        return None, None


def create_inventory_table():
    query = """
    CREATE TABLE IF NOT EXISTS inventory (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        product_price INTEGER NOT NULL,
        product_qty INTEGER NOT NULL
    );
    """
    execute_query(query)


def close_connection(con, cur):
    if cur is not None:
        cur.close()
    if con is not None:
        con.close()


def execute_query(query, params=None):
    con, cur = connect()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        con.commit()
    except Exception as error:
        print(f"Error executing query: {query}", error)
    finally:
        close_connection(con, cur)
