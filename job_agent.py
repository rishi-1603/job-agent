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
print(response.text[:500])
