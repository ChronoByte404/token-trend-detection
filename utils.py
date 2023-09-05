import json
from Janex import *

def open_file(file_path):
    with open(file_path, "r") as f:
        file_data = f.read()
    return file_data

def predict_sentence(inputs, max_tokens):
    with open("trends.json", "r") as f:
        trends_dictionary = json.load(f)

    tokens = tokenize(inputs)

    for seed_word in tokens:
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

    for i in range(max_tokens):
        last_element = tokens[-1]
        if last_element in trends_dictionary:
            context_words = trends_dictionary[last_element]
            if context_words:
                tokens.append(context_words[-1])
            else:
                break
        else:
            break

    return tokens
