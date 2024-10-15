"""
Database for handling random things which need to be stored

WIP, borrowed from my url shortener, will modify but don't know whats gonna be stored yet
"""

from typing import Optional

import psycopg  # PostgreSQL db driver v3
from psycopg import sql


class Database:
    def __init__(self, conn_params):
        print("Database opened")
        self.conn = psycopg.connect(**conn_params)
        self.cur = self.conn.cursor()


    def close(self):
        """
        Close the database connection

        :return: Nothing
        """
        print("Database closed")
        if self.cur is not None:
            self.cur.close()

        if self.conn is not None:
            self.conn.close()


    def get_analytics(self, analytics_url: str) -> Optional[list]:
        """
        Fetch analytics data from the database
        """
        self.cur.execute("SELECT * FROM URLs WHERE analytics_url = %s", (analytics_url,))
        url_table = self.cur.fetchall()
        if not url_table:
            return None
        url_id = url_table[0][0] # Get url_id so search with on Analytics table

        self.cur.execute("SELECT * FROM Analytics WHERE url_id = %s", (url_id,))
        return self.cur.fetchall()


    def add_analytics(self, url_id: int, referrer: str, user_agent: str) -> None:
        """
        Creates a database entry for analytics
        """
        self.cur.execute("""
        INSERT INTO Analytics (url_id, referrer, user_agent)
        VALUES  (%s, %s, %s)
        """, (url_id, referrer, user_agent))
        self.conn.commit()


if __name__ == "__main__":
    ...