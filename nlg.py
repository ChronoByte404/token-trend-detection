import json

from utils import *

inputs = input("You: ")

new_sentence = predict_sentence(inputs, 30)

print(new_sentence)
