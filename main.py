from Janex import *
from utils import *
import json
import spacy
import numpy as np

nlp = spacy.load("en_core_web_md")

file_path = input("Your file path: ")
data = open_file(file_path)

tokens = tokenize(data)

with open("trends.json", "r") as f:
    trends_dictionary = json.load(f)

# Iterate through tokens with an index
for i, token in enumerate(tokens):
    if token not in trends_dictionary:
        # Get the previous and next tokens if they exist
        prev_token = tokens[i - 1] if i > 0 else None
        next_token = tokens[i + 1] if i < len(tokens) - 1 else None

        # Create a list to store the word before and word after
        context_words = []
        if prev_token:
            context_words.append(prev_token)
        if next_token:
            context_words.append(next_token)

        # Compute the vector arrays for context words using spaCy
        context_vectors = []
        for word in context_words:
            word_doc = nlp(word)
            context_vectors.append(word_doc.vector.tolist())

        # Append the context words and their vectors to the dictionary
        trends_dictionary[token] = {
            "context_words": context_words,
            "context_vectors": context_vectors
        }
        print(trends_dictionary[token])
    else:
        # If the token already exists, add the previous and next words
        if prev_token:
            trends_dictionary[token]["context_words"].append(prev_token)
        if next_token:
            trends_dictionary[token]["context_words"].append(next_token)

# Save the trends_dictionary to a JSON file with the desired structure
output_dictionary = {}
for token, context_info in trends_dictionary.items():
    output_dictionary[token] = context_info

with open("trends.json", "w") as file:
    # Dump the dictionary into the JSON file with line breaks
    json.dump(output_dictionary, file, indent=4)

if __name__ == "__main__":
    # Assuming you have a trends_dictionary with context_words
    seed_word = input("You: ")

    predict_sentence(seed_word, 20)
