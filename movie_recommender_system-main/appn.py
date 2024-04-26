from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/collection/{movie_id}/images"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

@app.route('/')
def home():
    return render_template('index.html', movies_list=movies_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append("")
    return render_template('recommendations.html', recommend_movie=recommend_movie)

if __name__ == '__main__':
    app.run(debug=True)

