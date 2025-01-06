import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

DATABASE_PROMPT = "Enter db url or leave empty to use .env:"
db_url = input(DATABASE_PROMPT)
if not db_url:
    load_dotenv()
    db_url = os.environ['DATABASE_URL']

pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=db_url)


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)