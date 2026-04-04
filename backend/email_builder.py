from datetime import datetime
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "email_template.html"


def generate_article_block(article: dict) -> str:
    title = article.get("title", "No Title")
    summary = article.get("summary", "")[:200] + "..."
    url = article.get("url", "#")
    source = article.get("source", "Unknown")

    return f"""
    <div class="article">
        <div class="article-title">{title}</div>
        <div class="article-summary">{summary}</div>
        <p><strong>Source:</strong> {source}</p>
        <a href="{url}" class="read-more" target="_blank">
            Read More
        </a>
    </div>
    """


def build_email_html(articles: list, unsubscribe_link: str) -> str:
    if not articles:
        return "<p>No articles available today.</p>"

    article_blocks = "".join(
        generate_article_block(article) for article in articles
    )

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{articles}}", article_blocks)
    html = html.replace("{{unsubscribe_link}}", unsubscribe_link)

    return html


def build_subject() -> str:
    today = datetime.now().strftime("%b %d, %Y")
    return f"🧠 AI & Data Science Digest — {today}"