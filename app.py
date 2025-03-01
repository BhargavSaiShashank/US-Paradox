import streamlit as st
from utils.database import MovieDatabase

# Initialize the database
db = MovieDatabase()

# Streamlit app
st.title("Movie Database App")
st.write("Welcome to the Movie Database App!")

# Search functionality
search_query = st.text_input("Search for movies by title, genre, or year:")
if search_query:
    results = db.search_movies(search_query)
    if results:
        st.write("Search results:")
        for movie in results:
            st.write(f"Title: {movie[1]}, Year: {movie[2]}, Genre: {movie[3]}")
    else:
        st.write("No movies found.")

# Close the database connection
db.close()