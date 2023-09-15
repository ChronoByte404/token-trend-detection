import json
import numpy as np
import spacy
import torch
import torch.nn as nn
import torch.optim as optim
from Janex import *

nlp = spacy.load("en_core_web_md")

def open_file(file_path):
    with open(file_path, "r") as f:
        file_data = f.read()
    return file_data

def calculate_cosine_similarity(vector1, vector2):
    target_dim = 300
    vector1 = np.resize(vector1, target_dim)
    vector2 = np.resize(vector2, target_dim)

    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0

    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity

def calculate_similarity(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out = torch.relu(self.fc1(x))
        out = self.fc2(out)
        return out

def get_word_vector(word):
    return nlp(word).vector

def predict_sentence(inputs, max_tokens):

    for _ in range(max_tokens):
        with open("trends.json", "r") as f:
            trends_dictionary = json.load(f)

        context_window_size = 3
        context_vectors = np.array([get_word_vector(word) for word in inputs.split()[-context_window_size:]])

        target_dim = 300
        context_vectors = np.resize(context_vectors, target_dim)

        input_dim = 300
        hidden_dim = 128
        output_dim = len(trends_dictionary)
        model = SimpleNN(input_dim, hidden_dim, output_dim)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        context_tensor = torch.Tensor(context_vectors)

        output = model(context_tensor)
        _, predicted_idx = torch.max(output, 0)
        best_next_word = list(trends_dictionary.keys())[predicted_idx.item()]

        if best_next_word and output[predicted_idx.item()] > 0.1:
            inputs += ' ' + best_next_word
            inputs = inputs.replace("\n", " ")
            inputs = inputs.replace("  ", " ")
            print(inputs)
            context_vectors = np.roll(context_vectors, -1, axis=0)
            context_vectors = get_word_vector(best_next_word)
        else:
            break

    return inputs

if __name__ == "__main__":
    sentence = input("You: ")
#    sentence = f"User said: '{sentence}' Jarvis replies:"
    output = predict_sentence(sentence, 20)
    print("AI:", output)
