import pandas as pd

# Define column names from MovieLens 100k u.item format
columns = [
    'movieId', 'title', 'release_date', 'video_release_date',
    'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
    'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
    'Thriller', 'War', 'Western'
]

# Load the raw u.item file (ISO-8859-1 encoding for special characters)
df = pd.read_csv('data/u.item', sep='|', names=columns, encoding='ISO-8859-1')

# Build genre string from flags
genre_columns = columns[5:]
df['genres'] = df[genre_columns].apply(lambda row: '|'.join([genre for genre, val in row.items() if val == 1]), axis=1)

# Keep only the essentials
movies_df = df[['movieId', 'title', 'genres']]

# Save to CSV
movies_df.to_csv('movies.csv', index=False)

print("✅ Processed and saved clean 'movies.csv'")
