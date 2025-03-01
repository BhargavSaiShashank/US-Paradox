import pandas as pd
import sqlite3
from pathlib import Path

class MovieDatabase:
    def __init__(self):
        self.db_path = Path("data/movies.db")
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        # Create movies table if it doesn't exist
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT,
                genres TEXT,
                year INTEGER,
                rating REAL,
                description TEXT
            )
        """)
        self.conn.commit()

    def load_data(self, csv_path):
        # Load data from CSV and save to SQLite
        movies = pd.read_csv(csv_path)
        movies.to_sql("movies", self.conn, if_exists="replace", index=False)
        self.conn.execute("CREATE INDEX idx_title ON movies(title)")
        self.conn.execute("CREATE INDEX idx_genre ON movies(genres)")
        self.conn.execute("CREATE INDEX idx_year ON movies(year)")
        self.conn.commit()

    def search_movies(self, query=None, genre=None, year=None, limit=100):
        base_query = """
            SELECT title, year, genres, rating, description
            FROM movies
            WHERE 1=1
        """
        params = []
        
        if query:
            base_query += " AND title LIKE ?"
            params.append(f"%{query}%")
        if genre:
            base_query += " AND genres LIKE ?"
            params.append(f"%{genre}%")
        if year:
            base_query += " AND year = ?"
            params.append(year)
            
        base_query += f" LIMIT {limit}"
        
        return pd.read_sql(base_query, self.conn, params=params)