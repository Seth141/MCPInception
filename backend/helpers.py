#!/usr/bin/env python3

"""
uv run backend/template.py <url>
"""

import os
import sys
from dotenv import load_dotenv
import argparse
import psycopg2
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(ROOT)
# load environment variables like PG_USER and PG_PASSWORD
load_dotenv()


def print_roots():
    """ just for debug """
    print(f'{PROJECT_ROOT=}')
    print(f'{ROOT=}')


def parse_args() -> argparse.Namespace:
    """
    take the url to scrape a site
    """
    parser = argparse.ArgumentParser(description="Take the site url as argument.")
    parser.add_argument("url", metavar="N", type=str, nargs=1)
    return parser.parse_args()


def db_create(DB_NAME: str = os.getenv("DB_NAME", "mcp")) -> None:
    """
    create the database if it doesn't exist already
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database=DB_NAME,
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to create database: {e}")


def db_connect(
    db_name: str = os.getenv("DB_NAME", "mcp")
) -> psycopg2.extensions.connection | None:
    """
    postgres db connection
    create the db if it doesn't exist already, and connect to it
    otherwise connect to the existing db right away
    """
    # brew services start postgresql
    # psql -U ${whoami} -d postgres
    # psql -U sudo -d postgres
    # CREATE DATABASE mcp;

    # check if database exists
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        conn.close()

    except Exception as e:
        raise Exception(f"Failed to check database existence: {e}")

    if exists:
        # connect to existing db
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database=db_name,
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
    else:
        # create db and connect
        db_create(db_name)
        conn = db_connect(db_name)

    return conn


def fetch_url(url: str) -> BeautifulSoup:
    """
    fetch the url and return the soup object
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def parse_url(url: str) -> None:
    """
    parse the url and print the soup object
    """
    soup = fetch_url(url)
    print(soup.prettify())


if __name__ == "__main__":

    args = parse_args()
    url = args.url[0]

    # conn = db_connect()
    conn = db_connect("mcp")
    if conn is None:
        raise Exception("Database connection failed.")

    parse_url(url)

    conn.close()
    print("Database connection closed.")

