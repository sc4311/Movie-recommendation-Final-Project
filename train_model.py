import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the data
data = pd.read_csv('main_data.csv')

# Create the TfidfVectorizer and fit it on the 'comb' column
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['comb'])

# Save the fitted vectorizer
with open('tfidf_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

# Function to save the top-k similarities
def save_top_k_similarities(tfidf_matrix, k=5):
    top_k_similarities = []

    for i in range(tfidf_matrix.shape[0]):
        cosine_sim = cosine_similarity(tfidf_matrix[i], tfidf_matrix).flatten()
        top_k_indices = cosine_sim.argsort()[-k-1:-1][::-1]  # Exclude the document itself
        top_k_similarities.append((i, top_k_indices, cosine_sim[top_k_indices]))

    with open('top_k_cosine_similarities.pkl', 'wb') as sim_file:
        pickle.dump(top_k_similarities, sim_file)

# Save the top-k similarities (k=5 in this example)
save_top_k_similarities(tfidf_matrix, k=5)

print("Vectorizer and top-k similarity matrix saved successfully.")
