from backend.news_fetcher import fetch_all_news
from backend.email_builder import build_email_html, build_subject
from backend.email_sender import send_bulk_emails
from backend.utils.logger import logger


def run_pipeline():
    logger.info("🚀 Starting newsletter pipeline...")

    try:
        # 1. Fetch articles
        articles = fetch_all_news()
        logger.info(f"📰 Articles fetched: {len(articles)}")

        if not articles:
            logger.warning("⚠️ No articles found. Skipping email.")
            return

        # 2. Build email
        html = build_email_html(
            articles,
            "http://localhost:8000/unsubscribe"
        )
        subject = build_subject()

        # 3. Send emails
        send_bulk_emails(subject, html)

        logger.info("✅ Pipeline completed successfully")

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}", exc_info=True)


if __name__ == "__main__":
    run_pipeline()