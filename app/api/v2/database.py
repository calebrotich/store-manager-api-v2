"""Module creates a connection to the database

Creates tables for the application
"""

import sys
import os

import psycopg2
import psycopg2.extras
from instance.config import config

def init_db(db_url=None):
    """Initialize db connection
        
    Run queries that set up tables
    """        
    try:
        if os.getenv('FLASK_ENV') == 'testing':
            conn, cursor = query_database()
            queries = drop_table_if_exists() + create_tables()
            
        else:
            conn, cursor = query_database()
            queries = create_tables()

        i = 0
        while i != len(queries):
            query = queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        conn.close()

    except Exception as error:
        print("DB Error : {} \n".format(error))


def create_tables():
    """Queries for setting up the database tables"""

    users_table_query = """
    CREATE TABLE IF NOT EXISTS users  (
        user_id SERIAL PRIMARY KEY,
        email VARCHAR (30) NOT NULL UNIQUE,
        password VARCHAR (128) NOT NULL,
        role VARCHAR (10) NOT NULL
    )"""

    category_query = """
    CREATE TABLE IF NOT EXISTS category (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR (24) NOT NULL UNIQUE,
        date_added TIMESTAMP DEFAULT NOW()
    )"""

    products_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR (24) NOT NULL UNIQUE,
        product_price INTEGER NOT NULL,
        min_quantity INTEGER NOT NULL,
        inventory INTEGER NOT NULL,
        added_by INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
        category INTEGER NOT NULL REFERENCES category(category_id) ON DELETE CASCADE
    )"""

    sales_order_query = """
    CREATE TABLE IF NOT EXISTS saleorders (
        saleorder_id SERIAL PRIMARY KEY,
        date_ordered TIMESTAMP DEFAULT NOW(),
        amount INTEGER NOT NULL,
        made_by INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
    )"""

    sale_items_query = """
    CREATE TABLE IF NOT EXISTS saleitems (
        saleorder_id INTEGER NOT NULL REFERENCES saleorders(saleorder_id) ON DELETE CASCADE,
        product INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
        quantity INTEGER NOT NULL
    )"""

    blacklist_query = """
    CREATE TABLE IF NOT EXISTS blacklist (
        token VARCHAR (240) NOT NULL
    )
    """

    return [users_table_query, category_query, products_table_query,
            sales_order_query, sale_items_query, blacklist_query]


def drop_table_if_exists():
    """Drop tables before recreating them"""

    drop_products_table = """
    DROP TABLE IF EXISTS products CASCADE"""

    drop_sales_table = """
    DROP TABLE IF EXISTS saleorders CASCADE"""

    drop_users_table = """
    DROP TABLE IF EXISTS users CASCADE"""

    drop_category_table = """
    DROP TABLE IF EXISTS category CASCADE"""

    drop_saleitems_table = """
    DROP TABLE IF EXISTS saleitems CASCADE"""

    drop_blacklist_table = """
    DROP TABLE IF EXISTS blacklist CASCADE"""

    return [drop_products_table, drop_sales_table,
     drop_users_table, drop_category_table, drop_blacklist_table, drop_saleitems_table]


def query_database(query=None, db_url=None):
    """Creates a connection to the db
        
    Executes a query
    """
    conn = None
    if db_url is None:
        db_url = config[os.getenv("FLASK_ENV")].DB_URL
    try:
        # connect to db
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory= psycopg2.extras.RealDictCursor)

        if query:
            cursor.execute(query)
            conn.commit()

    except(Exception,
            psycopg2.DatabaseError,
            psycopg2.ProgrammingError) as error:
        print(error)
        return None

    return conn, cursor


def insert_to_db(query):
    """Handles INSERT queries"""
        
    try:
        conn = query_database(query)[0]
        conn.close()
    except psycopg2.Error as error:
        print("Insertion error: {}".format(error))
        sys.exit(1)


def select_from_db(query):
    """Handles SELECT queries"""
    
    fetched_content = None
    conn, cursor = query_database(query)
    if conn:
        fetched_content = cursor.fetchall()
        conn.close()

    return fetched_content


if __name__ == '__main__':
    init_db()
    query_database()
