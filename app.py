import streamlit as st
from recommendation import get_recommendations

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommender System")
st.markdown("Enter your **User ID** (1–943) to get personalized movie recommendations.")

user_id = st.text_input("User ID")

if st.button("Get Recommendations"):
    if user_id.isdigit():
        user_id = int(user_id)
        with st.spinner("Generating recommendations..."):
            recommendations = get_recommendations(user_id)
        st.success("Here are your top picks:")
        def render_stars(rating):
            full_stars = int(rating)  # number of full stars
            half_star = rating - full_stars >= 0.5
            empty_stars = 5 - full_stars - int(half_star)

            stars_html = '⭐' * full_stars
            if half_star:
                stars_html += '🌓'  # optional half-star emoji
            stars_html += '☆' * empty_stars
            return stars_html

        for i in range(0, len(recommendations), 3):
            cols = st.columns(3)
            for col, movie in zip(cols, recommendations[i:i+3]):
                with col:
                    st.image(movie['poster_url'], width=150)
                    st.markdown(f"**{movie['title']}**")
                    st.markdown(f"Genres: {movie['genres']}")
                    st.markdown(render_stars(movie['avg_rating']))
                    st.markdown(f"({movie['avg_rating']}/5)")
                    st.markdown(f"[🔗 Wikipedia]({movie['wikipedia_url']})", unsafe_allow_html=True)
    else:
        st.error("Please enter a valid numeric User ID.")

