from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def get_recommendations(self, query, movies, top_k=5):
        # Ensure all columns are strings and not empty
        movies["title"] = movies["title"].fillna("").astype(str)
        movies["genres"] = movies["genres"].fillna("").astype(str)
        movies["description"] = movies["description"].fillna("").astype(str)

        # Combine title, genres, and description for better recommendations
        movies["features"] = (
            movies["title"] + " " + 
            movies["genres"] + " " + 
            movies["description"]
        )

        # Debug: Check if features are non-empty
        if movies["features"].str.strip().eq("").all():
            raise ValueError("All feature strings are empty. Check your data.")

        # Fit and transform the data
        tfidf_matrix = self.vectorizer.fit_transform(movies["features"])

        # Transform the query
        query_vector = self.vectorizer.transform([query])

        # Compute similarity
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]

        # Return top recommendations
        return movies.iloc[top_indices]