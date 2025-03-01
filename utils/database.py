import sqlite3

class MovieDatabase:
    def __init__(self, db_path="data/movies.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            genre TEXT NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def search_movies(self, search_query):
        """
        Search for movies in the database based on a query.
        :param search_query: A string to search for in movie titles, genres, or years.
        :return: A list of matching movies.
        """
        query = """
        SELECT * FROM movies
        WHERE title LIKE ? OR genre LIKE ? OR year LIKE ?;
        """
        search_term = f"%{search_query}%"
        results = self.conn.execute(query, (search_term, search_term, search_term)).fetchall()
        return results
     

    def close(self):
        self.conn.close()