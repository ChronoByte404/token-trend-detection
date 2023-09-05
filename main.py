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

# Choose a seed word that exists in your trends_dictionary
if seed_word in trends_dictionary:
    context_words = trends_dictionary[seed_word]

    # Use a template-based approach
    if context_words:
        sentence_template = f"The word '{seed_word}' is often associated with '{', '.join(context_words)}' in recent trends."
        print(sentence_template)
    else:
        print(f"No context words found for '{seed_word}'.")
else:
    print(f"'{seed_word}' not found in trends_dictionary.")
