
import pandas as pd
import pickle
import os
import requests
import numpy as np

# Load pre-trained model
model = pickle.load(open("svd_model.pkl", "rb"))

# Load movie data with avg_rating
movies = pd.read_csv("movies.csv")

# Optional fallback (if any rating is missing — unlikely now)
movies['avg_rating'] = movies['avg_rating'].fillna(3.0)


OMDB_API_KEY = "f4d2d01"  

def fetch_poster(title):
    try:
        if '(' in title:
            title = title.split('(')[0].strip()

        url = f"http://www.omdbapi.com/"
        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
    except Exception as e:
        print(f"OMDb error for {title}: {e}")

    return "https://dummyimage.com/150x220/cccccc/000000&text=No+Image"

def fetch_wikipedia_url(title):
    base = "https://en.wikipedia.org/wiki/"
    clean_title = title.replace(' ', '_').replace("(", "").replace(")", "")
    return base + clean_title

import numpy as np

def get_recommendations(user_id, n_recommendations=20):
    movie_ids = movies['movieId'].tolist()

    try:
        inner_uid = model.trainset.to_inner_uid(str(user_id))
        user_rated_movies = set(
            int(model.trainset.to_raw_iid(iid))
            for (iid, _) in model.trainset.ur[inner_uid]
        )
    except ValueError:
        user_rated_movies = set()

    predictions = []
    for movie_id in movie_ids:
        if movie_id not in user_rated_movies:
            pred = model.predict(user_id, movie_id)
            movie_avg = movies[movies['movieId'] == movie_id]['avg_rating'].values[0]
            score = pred.est - movie_avg
            predictions.append((movie_id, pred.est, score))

    predictions.sort(key=lambda x: (x[1], x[2]), reverse=True)

    top_predictions = predictions[:50]
    np.random.shuffle(top_predictions)
    top_predictions = sorted(top_predictions[:n_recommendations], key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie_id, est, _ in top_predictions:
        movie = movies[movies['movieId'] == movie_id].iloc[0]
        recommended_movies.append({
            'title': movie['title'],
            'avg_rating': round(movie['avg_rating'], 2),
            'genres': movie['genres'],
            'poster_url': fetch_poster(movie['title']),
            'wikipedia_url': fetch_wikipedia_url(movie['title'])
        })

    return recommended_movies
