import logging
import pickle

import pandas as pd
from flask import Flask, request, jsonify, render_template

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

def rcmd(m):
    m = m.lower()
    if m not in data['movie_title'].str.lower().unique():
        return ['Sorry! try another movie name']
    else:
        i = data[data['movie_title'].str.lower() == m].index[0]
        # Get the top-k similar movies
        similar_movies = next((item for item in top_k_similarities if item[0] == i), None)
        if similar_movies:
            top_k_indices = similar_movies[1]
            l = [data['movie_title'][index] for index in top_k_indices]
            return l
        else:
            return ['No recommendations found']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    # Log the searched movie
    app.logger.info(f"User searched for: {movie}")
    recommendations = rcmd(movie)
    return render_template('index.html', movie=movie, recommendations=recommendations)

@app.route('/suggestions', methods=['GET'])
def suggestions():
    search_term = request.args.get('q', '')
    results = data[data['movie_title'].str.contains(search_term, case=False, na=False)]['movie_title'].head(10).tolist()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
