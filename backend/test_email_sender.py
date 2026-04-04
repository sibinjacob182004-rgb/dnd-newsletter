from backend.email_builder import build_email_html, build_subject
from backend.email_sender import send_bulk_emails

sample_articles = [
    {
        "title": "AI is transforming everything",
        "summary": "AI is rapidly changing industries worldwide.",
        "url": "https://example.com/ai",
        "source": "TechCrunch"
    }
]

html = build_email_html(
    sample_articles,
    "http://localhost:8000/unsubscribe?email=test@example.com"
)

subject = build_subject()

send_bulk_emails(subject, html)
