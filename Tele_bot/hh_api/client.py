import requests
from config import HH_CLIENT_ID, REDIRECT_URI

def search_candidates(query):
    response = requests.get("https://api.hh.ru/resumes", params={"text": query})
    return response.json()

def parse_resume_link(link):
    return link.split("/")[-1]
