import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="review_db",
                user="fastapi_user",
                password="securepassword",
                host="database",
                port=5432,
            )
            conn.close()
            break
        except OperationalError:
            print("Database not ready, retrying in 1 second...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()