from datetime import datetime


def build_subject():
    today = datetime.now().strftime("%B %d, %Y")
    return f"🧠 Data n Dreads | Top AI & Data Science News - {today}"


def build_email_html(articles, unsubscribe_base_url):
    html = f"""
    <html>
    <body style="font-family: Arial; background-color: #f4f4f4; padding: 20px;">
        <h2>🧠 Data n Dreads | DataForge Newsletter</h2>
        <p>Latest in AI, ML & Data Science:</p>
    """

    for article in articles[:10]:
        html += f"""
        <div style="background: white; padding: 10px; margin-bottom: 10px; border-radius: 8px;">
            <h3>{article['title']}</h3>
            <p>{article['summary']}</p>
            <p><b>Source:</b> {article['source']}</p>
            <a href="{article['url']}">Read more</a>
        </div>
        """

    html += """
        <hr>
        <p style="font-size: 12px; color: gray;">
            If you wish to unsubscribe, click below:
        </p>
        <p>
            <a href="{unsubscribe_link}">Unsubscribe</a>
        </p>
    </body>
    </html>
    """

    return html