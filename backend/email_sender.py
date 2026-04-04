import os
import time
from resend import Resend

from backend.utils.supabase_client import get_supabase_client
from backend.utils.logger import logger

# Load env variables
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

resend = Resend(api_key=RESEND_API_KEY)


def get_all_subscribers():
    supabase = get_supabase_client()

    response = supabase.table("subscribers").select("email").eq("subscribed", True).execute()

    emails = [row["email"] for row in response.data]
    return emails


def send_bulk_emails(subject, html):
    subscribers = get_all_subscribers()

    success = 0
    failure = 0

    for email in subscribers:
        try:
            logger.info(f"📤 Sending to: {email}")

            resend.emails.send({
                "from": FROM_EMAIL,
                "to": email,
                "subject": subject,
                "html": html
            })

            logger.info(f"✅ Sent to {email}")
            success += 1

            # Rate limiting (avoid spam issues)
            time.sleep(1)

        except Exception as e:
            logger.error(f"❌ Failed for {email}: {e}")
            failure += 1

    logger.info(f"📊 SUMMARY | Success: {success} | Failed: {failure}")