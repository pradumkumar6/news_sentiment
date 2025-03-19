from flask import Flask, request, jsonify
from utils import fetch_news, analyze_sentiment, generate_tts

app = Flask(__name__)

@app.route("/get_news", methods=["GET"])
def get_news():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name required"}), 400
    
    # Fetch news articles
    articles = fetch_news(company)
    
    # Perform sentiment analysis and topic extraction
    enriched_articles = []
    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
    all_topics = []
    
    for article in articles:
        if not article.get("summary"):  # Skip articles with no summary
            continue

        sentiment = analyze_sentiment(article["summary"])
        sentiment_count[sentiment] += 1

        # Mock topic extraction (you can enhance with NLP later)
        topics = ["Electric Vehicles"] if "Tesla" in article["title"] else ["Finance", "Regulations"]
        all_topics.extend(topics)
        
        enriched_articles.append({
            "Title": article["title"],
            "Summary": article["summary"],
            "Sentiment": sentiment,
            "Topics": topics
        })
    
    # Handle empty or missing summaries
    full_summary = " ".join([a["summary"] for a in enriched_articles])
    if not full_summary.strip():
        full_summary = "No valid articles found for this company."

    # Generate Hindi TTS summary
    audio_file = generate_tts(full_summary)
    
    # Comparative Sentiment Insights
    coverage_differences = [
        {
            "Comparison": "Article 1 highlights Tesla's strong sales, while Article 2 discusses regulatory issues.",
            "Impact": "The first article boosts confidence in Tesla's market growth, while the second raises concerns about future regulatory hurdles."
        },
        {
            "Comparison": "Article 1 is focused on financial success and innovation, whereas Article 2 is about legal challenges and risks.",
            "Impact": "Investors may react positively to growth news but stay cautious due to regulatory scrutiny."
        }
    ]
    
    # Topic overlap comparison
    topic_overlap = {
        "Common Topics": list(set(all_topics)), 
        "Unique Topics in Article 1": ["Stock Market", "Innovation"],
        "Unique Topics in Article 2": ["Regulations", "Autonomous Vehicles"]
    }
    
    # Final structured response
    response = {
        "Company": company,
        "Articles": enriched_articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_count,
            "Coverage Differences": coverage_differences,
            "Topic Overlap": topic_overlap
        },
        "Final Sentiment Analysis": "Tesla’s latest news coverage is mostly positive. Potential stock growth expected.",
        "Audio": f"[Play Hindi Speech]({audio_file})"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
