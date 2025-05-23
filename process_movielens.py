import pandas as pd

# Load movie metadata
columns = [
    'movieId', 'title', 'release_date', 'video_release_date',
    'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
    'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
    'Thriller', 'War', 'Western'
]

# Load movies
movies = pd.read_csv('data/u.item', sep='|', names=columns, encoding='ISO-8859-1')
genre_columns = columns[5:]
movies['genres'] = movies[genre_columns].apply(
    lambda row: '|'.join([genre for genre, val in row.items() if val == 1]),
    axis=1
)
movies = movies[['movieId', 'title', 'genres']]

# Load ratings and compute avg_rating
ratings = pd.read_csv('data/u.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
avg_ratings.columns = ['movieId', 'avg_rating']

# Merge into movies
movies = movies.merge(avg_ratings, on='movieId', how='left')
movies['avg_rating'] = movies['avg_rating'].fillna(3.0)  # fallback

# Save final movies.csv
movies.to_csv('movies.csv', index=False)

print("✅ Processed and saved enhanced 'movies.csv' with avg_rating.")
