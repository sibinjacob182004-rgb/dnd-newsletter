from email_builder import build_email_html, build_subject

sample_articles = [
    {
        "title": "AI beats humans in coding",
        "summary": "A new AI model has surpassed human benchmarks in competitive coding.",
        "url": "https://example.com/ai",
        "source": "TechCrunch"
    },
    {
        "title": "Top Data Science Trends",
        "summary": "Key trends shaping the future of AI and ML.",
        "url": "https://example.com/ds",
        "source": "KDnuggets"
    }
]

html = build_email_html(
    sample_articles,
    "http://localhost:8000/unsubscribe?email=test@example.com"
)

subject = build_subject()

with open("preview.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ preview.html generated")
print("📩 Subject:", subject)