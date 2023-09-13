import json

with open("intents.json", "r") as f:
    intents = json.load(f)

patterns = []
responses = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
    for response in intent["responses"]:
        responses.append(response)

new_patterns = " \n".join(patterns)
print(new_patterns)
new_responses = " \n".join(responses)
print(new_responses)

with open("patterns.txt", "w") as f:
    f.write(new_patterns)

with open("responses.txt", "w") as f:
    f.write(new_responses)
