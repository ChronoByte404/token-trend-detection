import json
import numpy as np
import spacy
from Janex import *

nlp = spacy.load("en_core_web_sm")

def open_file(file_path):
    with open(file_path, "r") as f:
        file_data = f.read()
    return file_data

def calculate_cosine_similarity(vector1, vector2):
    # Resize vectors to a common dimension
    target_dim = 300
    vector1 = np.resize(vector1, target_dim)
    vector2 = np.resize(vector2, target_dim)

    # Calculate cosine similarity between two vectors
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0  # Handle zero division case

    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity

def predict_sentence(inputs, max_tokens):
    with open("trends.json", "r") as f:
        trends_dictionary = json.load(f)

    tokens = tokenize(inputs)

    context_window_size = 3  # Adjust the window size as needed

    for _ in range(max_tokens):
        highest_similarity = -1.0
        best_next_word = None

        # Calculate the vector representation of the input sentence context
        context = " ".join(tokens[-context_window_size:])
        input_sentence_vector = nlp(context).vector

        for word, data in trends_dictionary.items():
            if word not in tokens:
                context_vectors = data.get("context_vectors")

                if context_vectors:
                    # Calculate the cosine similarity between input_sentence_vector and context_vectors
                    similarities = [
                        calculate_cosine_similarity(input_sentence_vector, np.array(v))
                        for v in context_vectors
                        ]

                    max_similarity = max(similarities)

                    if max_similarity > highest_similarity:
                        highest_similarity = max_similarity
                        best_next_word = word

        if best_next_word and highest_similarity > 0.5:
            if best_next_word not in tokens:  # Adjust the threshold as needed
                tokens.append(best_next_word)
        else:
            break

    return " ".join(tokens)

if __name__ == "__main__":
    sentence = input("You: ")
    sentence = f"The user said: '{sentence}'"
    output = predict_sentence(sentence, 20)
    output = output.replace("\n", " ")
    output = output.replace("  ", " ")
    print("AI:", output)
