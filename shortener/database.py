import os

import psycopg  # PostgreSQL db driver v3


conn_params = {
    "dbname": "felixgao_url_shortener",
    "user": "felixgao",
    "password": os.environ['DB_PASSWORD'],
    "host": "hackclub.app",
    "port": "5432"
}

# Note to self, database table formats :D
"""
felixgao_url_shortener=> SELECT * FROM URLs;
 id | original_url | shortened_url | analytics_url 
----+--------------+---------------+---------------
(0 rows)

felixgao_url_shortener=> SELECT * FROM Analytics;
 id | url_id | created_at | referrer | user_agent | ip_address 
----+--------+------------+----------+------------+------------
(0 rows)
"""

def get_url(shortened_path: str) -> list:
    """
    Gets a database entry for a URL
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT * FROM URLs WHERE shortened_url = {shortened_path};")
        result = [item[0] for item in cur.fetchall()]
        conn.commit()
    return result


def add_url(original_url: str, shortened_url: str, analytics_url: str) -> None:
    """
    Creates a database entry for a new URL
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO URLs (original_url, shortened_url, analytics_url) 
        VALUES ({original_url}, {shortened_url}, {analytics_url});
        """)

        conn.commit()


def check_exists(table_item, table_value) -> bool:
    """
    Checks if a table item already exists
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        ...

if __name__ == "__main__":
    add_url("test123", "felixgao.dev", "test5")
