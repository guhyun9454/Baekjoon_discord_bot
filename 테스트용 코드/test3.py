import requests
from bs4 import BeautifulSoup

import requests

def algo_id_search(find):

    url = "https://solved.ac/api/v3/search/tag"
    find_algo = "수학"
    querystring = {"query":find_algo}

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, params=querystring)

    algo_list = response.json()["items"]
    for algo in algo_list:
        print(algo["displayNames"][0]["short"])
        print("id: ",algo["bojTagId"])


