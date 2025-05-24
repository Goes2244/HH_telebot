import requests
from bs4 import BeautifulSoup

def parse_hh_resume(link: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        full_name = soup.find("h1", {"class": "resume-block__title"}).text.strip()
        position = soup.find("span", {"class": "resume-block__specialization"}).text.strip()
        city = soup.find("span", {"data-qa": "resume-personal-address"}).text.strip()
        experience = soup.find("span", {"data-qa": "resume-experience"}).text.strip()
        
        return {
            "full_name": full_name,
            "position": position,
            "city": city,
            "experience": experience,
            "link": link
        }
    except Exception as e:
        return None