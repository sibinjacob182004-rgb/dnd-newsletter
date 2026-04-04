import os
import time
import resend

from backend.utils.supabase_client import get_supabase_client
from backend.utils.logger import logger

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

resend.api_key = RESEND_API_KEY


def get_all_subscribers():
    supabase = get_supabase_client()

    response = supabase.table("subscribers") \
        .select("email") \
        .eq("subscribed", True) \
        .execute()

    return [row["email"] for row in response.data]


def send_bulk_emails(subject, html_template):
    subscribers = get_all_subscribers()

    success = 0
    failure = 0

    for email in subscribers:
        try:
            unsubscribe_link = f"https://dnd-newsletter.onrender.com/unsubscribe?email={email}"

            html = html_template.replace("{unsubscribe_link}", unsubscribe_link)

            logger.info(f"📤 Sending to: {email}")

            resend.Emails.send({
                "from": FROM_EMAIL,
                "to": email,
                "subject": subject,
                "html": html
            })

            logger.info(f"✅ Sent to {email}")
            success += 1

            time.sleep(1)

        except Exception as e:
            logger.error(f"❌ Failed for {email}: {e}")
            failure += 1

    logger.info(f"📊 SUMMARY | Success: {success} | Failed: {failure}")