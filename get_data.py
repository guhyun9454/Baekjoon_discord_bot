import requests
from bs4 import BeautifulSoup


def solvedac_api(link : str,): # 
    return

def request(link: str):
    try:
        page = requests.get(link , headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except:
        return None


