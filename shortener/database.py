import os

import psycopg  # Portgresql db driver v3


conn_params = {
    "dbname": "felixgao_url_shortener",
    "user": "felixgao",
    "password": os.environ['DB_PASSWORD'],
    "host": "hackclub.app",
    "port": "5432"
}

# Note to self, databse format
"""
 path | destination | analytics_url | analytics_data 
------+-------------+---------------+----------------
(0 rows)
"""

def get_url(shortened_path) -> list:
    """
    Gets a database entry for a URL
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT * FROM urls WHERE destination = {shortened_path};")
        result = [item[0] for item in cur.fetchall()]
        conn.commit()
    return result


def add_url(path, destination, analytics) -> None:
    """
    Creates a database entry for a new URL
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO urls (path, destination, analytics_url, analytics_data)
        VALUES ('{path}', '{destination}', '{analytics}', 'null');
        """)

        conn.commit()


def check_exists(table_item, table_value) -> bool:
    """
    Checks if a table item already exists
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        ...

if __name__ == "__main__":
    add_url("/test123", "felixgao.dev", "test5")
