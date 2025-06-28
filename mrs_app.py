#WORKING PERFECTLY

import streamlit as st
import pickle
import requests
import gzip


#loading movies dataset
movies = pickle.load(open('movies.pkl','rb'))
#getting titles from it 
movies_title = movies['title'].values
# #loading similarity(cosine similarity) 
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


def get_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        # Return a default or placeholder image
        return "https://via.placeholder.com/500x750?text=No+Image"



#function to recommend top 5 similar movies + posters
def recommend_top5(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    recommended_movies = sorted(list(enumerate(distance)),reverse=True,key = lambda x:x[1])[1:6]
    
    recommended_5_movies = []
    recommended_movies_poster = []

    for i in recommended_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_5_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_poster.append(get_poster(movie_id))

    return recommended_5_movies,recommended_movies_poster





st.title(" 🎥 MOVIE RECOMMENDATION SYSTEM")

selected_movie = st.selectbox(
    "Search for a movie :  ",
    movies_title
)

if st.button("Search"):
    names , posters = recommend_top5(selected_movie)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.subheader(names[0])
        st.image(posters[0])
    with col2:
        st.subheader(names[1])
        st.image(posters[1])
    with col3:
        st.subheader(names[2])
        st.image(posters[2])
    with col4:
        st.subheader(names[3])
        st.image(posters[3])
    with col5:
        st.subheader(names[4])
        st.image(posters[4])














