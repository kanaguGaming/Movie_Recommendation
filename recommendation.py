# recommendation.py

import pandas as pd
import numpy as np
import pickle
import requests
import os

# Load model and data
model = pickle.load(open("svd_model.pkl", "rb"))
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("data/u.data", sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
users = pd.read_csv('users.csv')

# Calculate average movie ratings
avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
avg_ratings.columns = ['movieId', 'avg_rating']

# Merge with movies
movies = movies.merge(avg_ratings, on='movieId', how='left')
movies['avg_rating'] = movies['avg_rating'].fillna(3.0)

# TMDB API Key (replace with your actual key if needed)
TMDB_API_KEY = "0e8ff8159b37fa456aa8cb274b45c89e"

def fetch_poster(title):
    try:
        clean_title = title.split('(')[0].strip() if '(' in title else title
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": clean_title}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")

    return "https://via.placeholder.com/300x450?text=No+Image"

def fetch_wikipedia_url(title):
    clean_title = title.replace(' ', '_').replace('(', '').replace(')', '')
    return f"https://en.wikipedia.org/wiki/{clean_title}"

def get_user_info(user_id):
    user = users[users['userId'] == user_id]
    if not user.empty:
        user_data = user.iloc[0]
        return {
            'Age': user_data['age'],
            'Gender': user_data['gender'],
            'Occupation': user_data['occupation'],
            'Zip Code': user_data['zip_code']
        }
    return None

def get_recommendations(user_id, n_recommendations=20):
    movie_ids = movies['movieId'].tolist()
    rated_movies = set(ratings[ratings['userId'] == user_id]['movieId'])

    predictions = []
    for movie_id in movie_ids:
        if movie_id not in rated_movies:
            pred = model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_predictions = predictions[:n_recommendations]

    recommended_movies = []
    for movie_id, _ in top_predictions:
        movie = movies[movies['movieId'] == movie_id].iloc[0]
        recommended_movies.append({
            'title': movie['title'],
            'avg_rating': round(movie['avg_rating'], 2),
            'genres': movie['genres'],
            'poster_url': fetch_poster(movie['title']),
            'wikipedia_url': fetch_wikipedia_url(movie['title'])
        })

    return recommended_movies
