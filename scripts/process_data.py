import pandas as pd
import sqlite3
from pathlib import Path

# Load IMDb datasets
basics = pd.read_csv("data/raw/title.basics.tsv", sep="\t", low_memory=False)
ratings = pd.read_csv("data/raw/title.ratings.tsv", sep="\t", low_memory=False)

# Filter movies
movies = basics[basics["titleType"] == "movie"]

# Merge with ratings
movies = pd.merge(movies, ratings, on="tconst", how="left")

# Clean data
movies = movies[[
    "tconst", "primaryTitle", "startYear", "genres", 
    "averageRating", "numVotes", "runtimeMinutes"
]].rename(columns={
    "tconst": "id",
    "primaryTitle": "title",
    "startYear": "year",
    "genres": "genres",
    "averageRating": "rating",
    "numVotes": "votes",
    "runtimeMinutes": "runtime"
})

# Add a placeholder description column
movies["description"] = "No description available."

# Save to SQLite
db_path = Path("data/movies.db")
conn = sqlite3.connect(db_path)
movies.to_sql("movies", conn, index=False, if_exists="replace")

# Create indexes
conn.executescript("""
    CREATE INDEX idx_title ON movies(title);
    CREATE INDEX idx_genre ON movies(genres);
    CREATE INDEX idx_year ON movies(year);
""")
conn.close()