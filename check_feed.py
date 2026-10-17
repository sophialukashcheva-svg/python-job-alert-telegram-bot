from urllib.request import urlopen
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from pathlib import Path
from urllib.error import URLError
from datetime import datetime

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if not token or not chat_id:
    print("У файлі .env потрібно вказати TELEGRAM_BOT_TOKEN і TELEGRAM_CHAT_ID.")
    raise SystemExit(1)

try:
    chat_id = int(chat_id)
except ValueError:
    print("TELEGRAM_CHAT_ID у файлі .env має бути цілим числом.")
    raise SystemExit(1)

rss_url = "https://djinni.co/jobs/rss/"

def fetch_jobs():
    try:
        with urlopen(rss_url, timeout=30) as response:
            rss_data = response.read()
    except (URLError, TimeoutError) as error:
        print("Не вдалося завантажити вакансії з Djinni:", error)
        return None

    root = ET.fromstring(rss_data)
    return root.findall("./channel/item")

keywords = [
    "python", "pandas", "excel", "sql", "power bi",
    "data analysis", "data cleaning", "automation", "api"
]

target_roles = [
    "data analyst",
    "bi analyst",
    "business intelligence",
    "reporting analyst",
    "power bi",
    "аналітик даних",
    "аналітика даних",
]

def filter_jobs(jobs):

    matched_jobs = []

    for job in jobs:
        title = job.findtext("title")

        if re.search(r"\b(senior|lead|principal)\b", title.lower()):
            continue

        has_target_role = False

        for role in target_roles:
            if role in title.lower():
                has_target_role = True

        if not has_target_role:
            continue

        link = job.findtext("link")
        description = job.findtext("description", default="")
        soup = BeautifulSoup(description, "html.parser")
        clean_description = soup.get_text(separator=" ", strip=True) 
        job_text = (title + " " + clean_description).lower()
        matched_keywords = []

        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", job_text):
                matched_keywords.append(keyword)

        if not matched_keywords:
            continue

        
        matched_jobs.append({
            "title": title,
            "link": link,
            "description": clean_description,
            "keywords": matched_keywords
        })

        print("Назва:", title)
        print("Посилання:", link)
        print("Опис:", clean_description[:500])
        print("Знайдені ключові слова:", matched_keywords)
        print()

    return matched_jobs

async def send_job(job, message_text):
    history_file = Path(__file__).with_name("sent_jobs.txt")
    sent_links = set()

    if history_file.exists():
        sent_links = set(history_file.read_text(encoding="utf-8").splitlines())

    if job["link"] in sent_links:
        print("Цю вакансію вже надсилали. Пропускаємо.")
        return

    async with Bot(token=token) as bot:
        await bot.send_message(
            chat_id=chat_id,
            text=message_text
        )

    with history_file.open("a", encoding="utf-8") as file:
        file.write(job["link"] + "\n")

    print("Вакансію надіслано, посилання збережено!")

async def send_jobs(matched_jobs):
    for job in matched_jobs:
        message_text = (
            f"💼 Вакансія з Djinni\n\n"
            f"{job['title']}\n\n"
            f"Ключові слова: {', '.join(job['keywords'])}\n\n"
            f"{job['link']}"
        )

        await send_job(job, message_text)
        await asyncio.sleep(1)

async def main():
    while True:
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"\n[{current_time}] Перевіряю вакансії...")

        jobs = fetch_jobs()
        if jobs is None:
            print("Спробую знову через 15 хвилин.")
            await asyncio.sleep(900)
            continue
        print("Отримано вакансій:", len(jobs))

        matched_jobs = filter_jobs(jobs)
        print("Відібрано вакансій:", len(matched_jobs))

        await send_jobs(matched_jobs)

        print("Наступна перевірка через 15 хвилин.")
        await asyncio.sleep(900)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nБота зупинено.")
