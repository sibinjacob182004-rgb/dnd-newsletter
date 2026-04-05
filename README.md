# AI Newsletter Automation System

A fully automated, cloud-native newsletter pipeline that fetches trending AI and Data Science articles, builds clean HTML emails, and delivers them to subscribers every day — no manual effort required.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-2088FF?style=flat&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com)

---

## Project Overview

This system is a production-grade, end-to-end pipeline that automatically curates and delivers a daily newsletter focused on Artificial Intelligence, Machine Learning, and Data Science.

Every morning, the pipeline wakes up, pulls the latest articles from multiple sources, filters them for relevance, composes a clean HTML email, and sends it to all subscribers — without any human involvement. It is fully cloud-hosted, meaning there is no dependency on a local machine to keep it running.

---

## Features

- Pulls articles from both the GNews API and curated RSS feeds for broad coverage
- Filters content using keyword logic so only relevant AI/ML/DS articles reach subscribers
- Builds a clean, responsive HTML email from a reusable template
- Stores and retrieves subscriber data from a Supabase PostgreSQL database
- Sends emails reliably through the Resend API
- Runs automatically every day at 8:00 AM IST via a GitHub Actions cron job
- Manages all credentials securely through GitHub Actions secrets — nothing sensitive is hardcoded

---

## Architecture

The pipeline follows a straightforward linear flow:

```
News Sources (GNews + RSS)
        |
        v
  Filter Engine (Keyword Matching)
        |
        v
  Email Builder (HTML Template)
        |
        v
  Supabase (Fetch Subscribers)
        |
        v
  Resend API (Send Emails)
        ^
        |
  GitHub Actions (Daily Trigger)
```

---

## Tech Stack

| Layer          | Technology              | Purpose                          |
|----------------|-------------------------|----------------------------------|
| Backend        | Python 3.11 + FastAPI   | Core pipeline logic and API      |
| Database       | Supabase (PostgreSQL)   | Subscriber storage               |
| Email Service  | Resend API              | Transactional email delivery     |
| Automation     | GitHub Actions          | Scheduled daily execution        |
| News Sources   | GNews API + RSS         | Article fetching                 |
| Deployment     | Render                  | Cloud hosting                    |

---

## Project Structure

```
dnd-newsletter/
│
├── backend/
│   ├── main.py                   # FastAPI app entry point
│   ├── news_fetcher.py           # Fetches articles from GNews and RSS feeds
│   ├── email_builder.py          # Builds the HTML email from fetched articles
│   ├── email_sender.py           # Sends emails to subscribers via Resend
│   ├── scheduler.py              # Optional local scheduler config
│   ├── orchestrator.py           # Master pipeline — ties all steps together
│   │
│   ├── utils/
│   │   └── supabase_client.py    # Supabase client initialisation
│   │
│   ├── templates/
│   │   └── email_template.html   # HTML email layout template
│   │
│   └── requirements.txt          # Python dependencies
│
├── .github/
│   └── workflows/
│       └── newsletter.yml        # GitHub Actions cron workflow
│
├── .env                          # Local environment variables (not committed)
└── README.md
```

---

## How It Works

1. **Trigger** — GitHub Actions fires the pipeline every day at 8:00 AM IST using a cron schedule.
2. **Fetch** — `news_fetcher.py` calls the GNews API and parses multiple RSS feeds to collect recent articles.
3. **Filter** — Articles are matched against a keyword list (AI, Machine Learning, Data Science, LLM, etc.) and only relevant ones move forward.
4. **Build** — `email_builder.py` injects the filtered articles into `email_template.html` to produce a styled HTML email.
5. **Fetch Subscribers** — `email_sender.py` queries Supabase to retrieve the current list of active subscribers.
6. **Send** — The email is dispatched to every subscriber via the Resend API.
7. **Done** — The entire pipeline completes in under 30 seconds with no manual input.

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- A [Supabase](https://supabase.com) project with a `subscribers` table
- A [Resend](https://resend.com) account and API key
- A [GNews](https://gnews.io) API key

### Steps

```bash
# Clone the repository
git clone https://github.com/sibinjacob182004-rgb/dnd-newsletter.git
cd dnd-newsletter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create your .env file and fill in your credentials
cp .env.example .env

# Run the pipeline manually
python -m backend.orchestrator
```

---

## Environment Variables

Create a `.env` file in the root directory with the following:

```env
# Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-key

# Resend
RESEND_API_KEY=re_your_resend_api_key
FROM_EMAIL=onboarding@resend.dev

# GNews
GNEWS_API_KEY=your_gnews_api_key
```

> Never commit your `.env` file. It is already listed in `.gitignore`. In production, all secrets are stored in GitHub Actions and injected at runtime — nothing sensitive lives in the codebase.

---

## Deployment

### Render

1. Connect your GitHub repository to [Render](https://render.com)
2. Create a new Web Service
3. Set the build command: `pip install -r backend/requirements.txt`
4. Set the start command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
5. Add your environment variables in the Render dashboard under Environment

### GitHub Actions

The newsletter runs automatically via `.github/workflows/newsletter.yml`. Before the first run, add these secrets under **Settings > Secrets and variables > Actions**:

| Secret Name      | Description                  |
|------------------|------------------------------|
| `SUPABASE_URL`   | Your Supabase project URL    |
| `SUPABASE_KEY`   | Your Supabase API key        |
| `RESEND_API_KEY` | Your Resend email API key    |
| `FROM_EMAIL`     | Sender email address         |
| `GNEWS_API_KEY`  | Your GNews API key           |

---

## Automation

The pipeline runs on a cron schedule defined in the workflow file:

```yaml
schedule:
  - cron: "30 2 * * *"   # 8:00 AM IST (UTC+5:30)
```

GitHub Actions runs on UTC, so `02:30 UTC` maps to `08:00 AM IST`. You can also trigger a manual run at any time from the Actions tab using `workflow_dispatch`.

---

## Example Output

Each subscriber receives a clean HTML email that includes a newsletter header with the current date, four to ten curated articles with their title, source, and a short summary, direct links to the original articles, and a footer with contact information.

The email is fully responsive and renders correctly across desktop and mobile clients.

---

## Limitations

- **Resend free tier** limits delivery to 100 emails per day and 3,000 per month. This is sufficient for a small audience but an upgrade is needed at scale.
- **GNews free tier** has a daily API call cap. RSS feeds act as a fallback to maintain article volume when the limit is reached.
- There is currently no self-serve unsubscribe flow. Removals are handled manually.
- The pipeline is single-topic and focuses exclusively on AI, ML, and Data Science content.

---

## Future Improvements

- Self-serve subscribe and unsubscribe API endpoints
- AI-generated article summaries using an LLM
- Web-based admin dashboard for subscriber management
- Multi-topic newsletter support
- Open rate and click tracking
- Configurable delivery frequency (daily or weekly)
- Email preview before sending

---

## Author

**Sibin Jacob**
- GitHub: [@sibinjacob182004-rgb](https://github.com/sibinjacob182004-rgb)
- Project: [dnd-newsletter](https://github.com/sibinjacob182004-rgb/dnd-newsletter)
