from flask import Flask, render_template, request
from transformers import pipeline
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Load Hugging Face sentiment model (3-class)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

# Mapping for labels -> readable sentiments
label_map = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sentimentDB"]
collection = db["reviews"]

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Analyze sentiment and save to DB
@app.route("/analyze", methods=["POST"])
def analyze():
    review = request.form["review"]
    result = sentiment_pipeline(review)[0]

    raw_label = result["label"]  # LABEL_0 / LABEL_1 / LABEL_2
    sentiment = label_map.get(raw_label, raw_label)  # Map to NEGATIVE/NEUTRAL/POSITIVE
    score = float(result["score"])

    # Save in MongoDB
    collection.insert_one({
        "review": review,
        "sentiment": sentiment,
        "score": score
    })

    return render_template("result.html", review=review, sentiment=sentiment, score=score)

# Generate sentiment distribution report

@app.route("/report")
def report():
    data = list(collection.find({}))

    sentiments = [d["sentiment"].upper() for d in data]  # normalize to uppercase

    pos_count = sentiments.count("POSITIVE")
    neg_count = sentiments.count("NEGATIVE")
    neu_count = sentiments.count("NEUTRAL")

    counts = [pos_count, neg_count, neu_count]
    labels = ["Positive", "Negative", "Neutral"]

    plt.figure(figsize=(6,6))
    plt.pie(
        counts, 
        labels=labels, 
        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',  # hide 0%
        colors=["#ff4d4d", "#4da6ff", "#77dd77"],  # red, blue, green
        startangle=90
    )
    plt.title("Sentiment Distribution")
    plt.axis("equal")  # keep it circular

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    return render_template("report.html", chart=img_base64)

# Clear all reviews
@app.route("/clear", methods=["POST"])
def clear():
    collection.delete_many({})  # delete all documents
    return render_template("clear.html")


if __name__ == "__main__":
    app.run(debug=True)
