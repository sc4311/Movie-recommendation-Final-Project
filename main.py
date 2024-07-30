import logging
import pickle
import pandas as pd
from flask import Flask, request, jsonify, render_template
from imdb import IMDb
from functools import lru_cache

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the tfidf vectorizer and top-k similarity data from disk
with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

with open('top_k_cosine_similarities.pkl', 'rb') as sim_file:
    top_k_similarities = pickle.load(sim_file)

# Load the dataset
data = pd.read_csv('main_data.csv')
movie_titles = data['movie_title'].str.lower().tolist()

# Initialize IMDbPY cache
ia = IMDb()

# Cache for cover URLs to avoid repeated lookups
cover_url_cache = {}

@lru_cache(maxsize=1000)
def get_cover_url(movie_title):
    if movie_title in cover_url_cache:
        return cover_url_cache[movie_title]

    search_results = ia.search_movie(movie_title)
    if search_results:
        movie = search_results[0]
        ia.update(movie)
        cover_url = movie.get('cover url', '')
        cover_url_cache[movie_title] = cover_url
        return cover_url
    return ''

def rcmd(m):
    m = m.lower()
    if m not in movie_titles:
        return [{'title': 'Sorry! try another movie name', 'cover_url': ''}]
    else:
        i = movie_titles.index(m)
        similar_movies = next((item for item in top_k_similarities if item[0] == i), None)
        if similar_movies:
            top_k_indices = similar_movies[1]
            recommendations = [
                {
                    'title': data['movie_title'][index],
                    'cover_url': get_cover_url(data['movie_title'][index])
                }
                for index in top_k_indices
            ]
            return recommendations
        else:
            return [{'title': 'No recommendations found', 'cover_url': ''}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    app.logger.info(f"User searched for: {movie}")
    recommendations = rcmd(movie)
    return render_template('index.html', movie=movie, recommendations=recommendations)

@app.route('/suggestions', methods=['GET'])
def suggestions():
    search_term = request.args.get('q', '').lower()
    results = [title for title in movie_titles if search_term in title][:10]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
