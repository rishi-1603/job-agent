import os
import json
import requests
import smtplib
from email.mime.text import MIMEText

# -----------------------------
# Load profile
# -----------------------------
with open("resume_profile.json", "r") as f:
    profile = json.load(f)

skills = [s.lower() for s in profile["skills"]]
preferred_locations = profile["preferred_locations"]
preferred_titles = profile["preferred_titles"]
exclude_titles = profile["exclude_titles"]

# -----------------------------
# API Setup
# -----------------------------
api_key = os.getenv("RAPIDAPI_KEY")

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

queries = [
    "Data Analyst Hyderabad",
    "Data Analyst Pune",
    "Associate Data Analyst Hyderabad",
    "Associate Data Analyst Pune",
    "Junior Data Analyst Hyderabad",
    "Junior Data Analyst Pune",
    "Business Analyst Hyderabad",
    "Business Analyst Pune",
    "Power BI Analyst Hyderabad",
    "Power BI Analyst Pune"
]

jobs_found = []

# -----------------------------
# Match Score
# -----------------------------
def calculate_score(job):

    score = 0

    title = (job.get("job_title") or "").lower()
    desc = (job.get("job_description") or "").lower()
    location = (job.get("job_location") or "").lower()

    # Title match
    if "data analyst" in title:
        score += 25

    if "associate" in title:
        score += 15

    if "junior" in title:
        score += 15

    if "business analyst" in title:
        score += 15

    if "power bi" in title:
        score += 20

    # Skills
    for skill in skills:
        if skill in desc:
            score += 5

    # Location
    if "hyderabad" in location:
        score += 10

    if "pune" in location:
        score += 10

    # Penalties
    if any(x.lower() in title for x in exclude_titles):
        score -= 50

    return max(score, 0)

# -----------------------------
# Fetch Jobs
# -----------------------------
for query in queries:

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        continue

    data = response.json().get("data", [])

    for job in data:

        title = job.get("job_title", "")

        if any(x.lower() in title.lower()
               for x in exclude_titles):
            continue

        score = calculate_score(job)

        jobs_found.append({
            "company": job.get("employer_name"),
            "title": title,
            "location": job.get("job_location"),
            "apply": job.get("job_apply_link"),
            "score": score
        })

# Remove duplicates
unique_jobs = {}

for job in jobs_found:
    unique_jobs[job["apply"]] = job

jobs_found = list(unique_jobs.values())

# Sort
jobs_found.sort(
    key=lambda x: x["score"],
    reverse=True
)

# -----------------------------
# Build Email
# -----------------------------
body = "Top Matching Data Analyst Jobs\n\n"

for i, job in enumerate(jobs_found, start=1):

    body += f"""
{i}. {job['title']}
Company: {job['company']}
Location: {job['location']}
Match Score: {job['score']}/100
Apply: {job['apply']}

--------------------------------------------------
"""

# -----------------------------
# Send Email
# -----------------------------
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

msg = MIMEText(body)

msg["Subject"] = "Data Analyst Jobs Report"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER

server = smtplib.SMTP(
    "smtp.gmail.com",
    587
)

server.starttls()

server.login(
    EMAIL_USER,
    EMAIL_PASSWORD
)

server.sendmail(
    EMAIL_USER,
    EMAIL_USER,
    msg.as_string()
)

server.quit()

print("Email Sent Successfully")
