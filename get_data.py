import requests
from bs4 import BeautifulSoup


def solvedac(link : str,): # 
    return

def baekjoon(link: str):
    try:
        page = requests.get(link , headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except:
        return None
