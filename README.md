# Python Job Alert Telegram Bot

A Python bot that checks the Djinni RSS feed for data analyst
vacancies, filters them by job title and keywords, and sends
matching jobs to Telegram.

The bot remembers previously sent job links to avoid duplicates
and repeats the check 15 minutes after each completed check.

AI-based job evaluation is planned for a future version.

## Features

- Fetches job listings from the Djinni RSS feed.
- Filters job titles for data analytics roles.
- Excludes titles containing Senior, Lead, or Principal.
- Matches keywords such as Python, SQL, Excel, and Power BI.
- Sends matching vacancies to Telegram.
- Saves sent job links locally to prevent duplicate alerts.
- Waits 15 minutes between checks.
- Retries failed downloads after 15 minutes.

## Current limitations

- Checks only the vacancies available in the RSS feed.
- Uses title and keyword matching; does not assess all job requirements.
- Requires the script to remain running and the computer to stay awake.
- Does not apply for jobs automatically.
- AI evaluation is not implemented yet.

## Setup and usage

1. Install Python. This project was developed with Python 3.14.

2. Open a terminal in the project folder and create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Copy the configuration template:

   ```bash
   cp .env.example .env
   ```

5. Open `.env` and enter your Telegram bot token and chat ID.
   Send a message to your bot in Telegram before running the script.

6. Start the bot:

   ```bash
   python check_feed.py
   ```

7. Press Control + C in the terminal to stop the bot.

These commands are for macOS and Linux.
Keep your `.env` file private.
