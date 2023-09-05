from Janex import *
from utils import *
import json

file_path = input("Your file path: ")
data = open_file(file_path)

tokens = tokenize(data)
trends_dictionary = {}

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

        # Append the context words list to the dictionary
        trends_dictionary[token] = context_words

print(trends_dictionary)

with open("trends.json", "w") as file:
    # Dump the dictionary into the JSON file with line breaks
    json.dump(trends_dictionary, file, indent=4)

# Assuming you have a trends_dictionary with context_words
seed_word = input("You: ")

predict_sentence(seed_word, 20)
