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

def get_url(shortened_url: str) -> list:
    """
    Fetch URL data from the database
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT * FROM URLs WHERE shortened_url = '{shortened_url}';")
        return cur.fetchall()


def get_analytics(analytics_url: str) -> list:
    """
    Fetch analytics data from the database
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT * FROM URLs WHERE analytics_url = '{analytics_url}';")
        # TODO: Take item from that result and grab analytics with matching ID
        return cur.fetchall()


def add_url(original_url: str, shortened_url: str, analytics_url: str) -> None:
    """
    Creates a database entry for a new URL
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO URLs (orininal_url, shortened_url, analytics_url) 
        VALUES ('{original_url}', '{shortened_url}', '{analytics_url}');
        """)

        conn.commit()


def add_analytics(url_id: int, referrer: str, user_agent: str, ip_addr: str) -> None:
    """
    Creates a database entry for analytics
    """
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO Analytics (url_id, referrer, user_agent, ip_address)
        VALUES ('{url_id}', '{referrer}', '{user_agent}', '{ip_addr}');
        """)

        conn.commit()


def check_exists(table_item, table_value) -> bool:
    """
    Checks if a table item already exists
    """
    raise NotImplemented("Not quite there yet, don't blow up the db!")
    with psycopg.connect(**conn_params) as conn, conn.cursor() as cur:
        ...

if __name__ == "__main__":
    add_url("test123", "felixgao.dev", "test5")