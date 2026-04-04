import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def check_relevance(article):
    prompt = f"""
You are an expert AI curator for a data science newsletter.

Given the following article:

Title: {article['title']}
Summary: {article['summary']}

Task:
1. Determine if it is relevant to:
   - Data Science
   - Machine Learning / AI
   - Big Data Analytics
   - Data Engineering

2. Reject:
   - Clickbait
   - Generic tech news
   - Business fluff
   - Non-technical content

Return STRICT JSON:
{{
  "relevant": true/false,
  "reason": "short reason",
  "relevance_score": 1-10
}}
"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        text = response.content[0].text.strip()

        # Try parsing JSON safely
        import json
        return json.loads(text)

    except Exception as e:
        print("Claude error:", e)
        return {
            "relevant": False,
            "reason": "error",
            "relevance_score": 0
        }


def filter_articles(articles):
    approved = []

    for article in articles:
        result = check_relevance(article)

        print("Checking:", article["title"])
        print("Result:", result)

        if result["relevance_score"] >= 7 and result["relevant"]:
            approved.append(article)

    return approved