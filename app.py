import streamlit as st
from utils.database import MovieDatabase
from utils.recommendations import MovieRecommender
from pathlib import Path

# Initialize database and recommender
db = MovieDatabase()
recommender = MovieRecommender()

# Load data (run only once)
if not Path("data/movies.db").exists():
    db.load_data("data/movies.csv")

# UI Configuration
st.set_page_config(layout="wide")
st.title("🎬 US Paradox - Find Your Next Favorite Movie")

# Search Filters
col1, col2, col3 = st.columns(3)
with col1:
    search_query = st.text_input("Search by title:")
with col2:
    selected_genre = st.selectbox("Filter by genre:", [
        "All", "Action", "Comedy", "Drama", "Horror", 
        "Sci-Fi", "Documentary", "Romance"
    ])
with col3:
    year_range = st.slider("Filter by year:", 1900, 2023, (2000, 2023))

# Search Execution
if st.button("Search Movies"):
    results = db.search_movies(
        query=search_query if search_query else None,
        genre=selected_genre if selected_genre != "All" else None,
        year=year_range[0],  # Search within range
        limit=50
    )
    
    # Display Results
    st.subheader("Search Results")
    cols = st.columns(4)
    for idx, movie in results.iterrows():
        with cols[idx % 4]:
            st.subheader(f"{movie['title']} ({movie['year']})")
            st.markdown(f"**Genre:** {movie['genres']}")
            st.markdown(f"**Rating:** ⭐ {movie['rating']}/10")
            st.markdown(f"**Description:** {movie['description']}")
            st.markdown("---")

# AI Recommendations
if st.button("Get AI Recommendations"):
    recommendations = recommender.get_recommendations(
        query=search_query if search_query else "action",  # Default query
        movies=db.search_movies(limit=1000),  # Use a larger dataset for recommendations
        top_k=5
    )
    
    st.subheader("AI Recommendations")
    for idx, movie in recommendations.iterrows():
        st.write(f"{idx + 1}. **{movie['title']}** ({movie['year']})")
        st.write(f"   Genre: {movie['genres']}")
        st.write(f"   Rating: ⭐ {movie['rating']}/10")
        st.write(f"   Description: {movie['description']}")
        st.write("---")