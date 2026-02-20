from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
import os

app = Flask(__name__)

nltk.download('punkt')

# Load NRC Lexicon
lexicon = defaultdict(list)

with open("emotion_lexicon.txt", "r", encoding="utf-8") as f:
    for line in f:
        word, emotion, value = line.strip().split('\t')
        if int(value) == 1:
            lexicon[word].append(emotion)

# Emotion Analyzer Function
def detect_emotion(text):
    tokens = word_tokenize(text.lower())
    emotions = defaultdict(int)

    # Count emotions
    ignore = ["positive", "negative"]

    for word in tokens:
        if word in lexicon:
            for emotion in lexicon[word]:
                if emotion not in ignore:
                    emotions[emotion] += 1

    # Total emotion count
    total = sum(emotions.values())

    if total == 0:
        return {}, ""

    # Convert to percentage
    percentages = {}
    for emotion, count in emotions.items():
        percentages[emotion] = round((count / total) * 100, 2)

    # Sort and take top 3
    top_emotions = dict(
        sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    )
    main_emotion = max(top_emotions, key=top_emotions.get)
    return top_emotions, main_emotion

# Homepage
@app.route("/", methods=["GET", "POST"])
def home():
    emotions = {}
    main_emotion = ""
    text = ""

    if request.method == "POST":
        text = request.form["text"]
        emotions, main_emotion = detect_emotion(text)

    return render_template(
        "index.html", 
        emotions=emotions,
        main_emotion=main_emotion, 
        text=text
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host = "0.0.0.0", port=port)