import pickle
import numpy as np

# Function to load chunks
def load_chunk(chunk_index):
    with open(f'cosine_similarity_chunk_{chunk_index}.pkl', 'rb') as sim_file:
        return pickle.load(sim_file)

# Example: Load all chunks into a single matrix (if memory allows)
def load_all_chunks(num_chunks):
    chunks = [load_chunk(i) for i in range(num_chunks)]
    return np.vstack(chunks)

# Number of chunks
num_chunks = 69  # Adjust based on the actual number of chunks

# Load all chunks (only if you have enough memory)
# cosine_sim_matrix = load_all_chunks(num_chunks)

# If you don't have enough memory, you can process chunks as needed
# For example, let's find the most similar documents to a given document in chunks

def find_most_similar(doc_index, num_chunks, top_n=5):
    similarities = []
    for i in range(num_chunks):
        chunk = load_chunk(i)
        similarities.extend(chunk[doc_index])
    similarities = np.array(similarities)
    most_similar_indices = similarities.argsort()[-top_n:][::-1]
    return most_similar_indices

# Example usage
doc_index = 0  # The index of the document you want to find similarities for
most_similar_docs = find_most_similar(doc_index, num_chunks)

print(f"Most similar documents to document {doc_index}: {most_similar_docs}")
