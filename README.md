# 📊 Sentiment Analysis Web App

A Flask-based web application that analyzes text sentiment (Positive, Negative, Neutral) using Hugging Face Transformers.  
The app stores reviews in **MongoDB** and generates a sentiment distribution chart with **Matplotlib**.

---

## 🚀 Features
- ✅ Input a review and get sentiment prediction (Positive / Negative / Neutral)  
- ✅ Save results in MongoDB automatically  
- ✅ Generate a sentiment distribution pie chart  
- ✅ Clear stored reviews from the database  

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)  
- **NLP Model:** Hugging Face `cardiffnlp/twitter-roberta-base-sentiment`  
- **Database:** MongoDB  
- **Visualization:** Matplotlib  
- **Frontend:** HTML, CSS (templates + static folder)  

---

## 📂 Project Structure
SENTIMENT ANALYSIS
├── 📁 static/ # CSS, images
├── 📁 templates/ # HTML files (index.html, result.html, report.html, clear.html)
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── .gitignore # Ignore venv, cache files
└── README.md # Project documentation
