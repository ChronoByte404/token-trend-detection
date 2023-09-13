import json

from utils import *

inputs = input("You: ")
inputs = f"User said: '{inputs}' Jarvis replies:"

new_sentence = predict_sentence(inputs, 30)

print(new_sentence)
