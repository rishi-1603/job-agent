import os
import requests

api_key = os.getenv("RAPIDAPI_KEY")

url = "https://jsearch.p.rapidapi.com/search"

querystring = {
    "query": "Data Analyst Hyderabad",
    "page": "1",
    "num_pages": "1"
}

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    jobs = data.get("data", [])

    for job in jobs[:10]:
        print("=" * 50)
        print("Company:", job.get("employer_name"))
        print("Role:", job.get("job_title"))
        print("Location:", job.get("job_location"))
        print("Apply:", job.get("job_apply_link"))
