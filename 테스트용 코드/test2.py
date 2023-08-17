
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import time
import random

# prob_id = "3266"
# url = 'https://solved.ac/api/v3/problem/show?problemId='+prob_id
# headers = {'Accept': 'application/json'}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
    
#     data = response.json()
#     print(data["titleKo"])
#     algo_list = []
#     for i in data["tags"]:
#         algo_list.append(i["displayNames"][0]["short"])
#     print(algo_list)
# else:
#     print(f"Request failed with status code: {response.status_code}")
tier_list = ["1","2","3","4","5"]
def rand_problem(tier_list):
    link = "https://www.acmicpc.net/problemset?sort=no_asc&tier="+",".join(tier_list)
    page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    pages = soup.find("ul",class_ = "pagination").find_all("li").__len__()
    rand_page = str(random.randint(1,pages))
    # print(rand_page)
    link = "https://www.acmicpc.net/problemset?sort=no_asc&tier="+",".join(tier_list) +"&page="+rand_page

    page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    number_of_problems = soup.find_all("tr").__len__()
    # print(number_of_problems)

    rand_problem = random.randint(1,number_of_problems)
    # print(rand_problem)
    print("page: ",rand_page," problem_no: ",rand_problem)
    print(soup.find_all("tr")[rand_problem-1].find("td","list_problem_id").text)
    return
for i in range(100):
    rand_problem(tier_list)