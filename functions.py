import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import random
import os
from get_data import *

tier_data = {0: ['Unrated'], 1: ['Bronze', 'V'], 2: ['Bronze', 'IV'], 3: ['Bronze', 'III'], 4: ['Bronze', 'II'], 
             5: ['Bronze', 'I'], 6: ['Silver', 'V'], 7: ['Silver', 'IV'], 8: ['Silver', 'III'], 9: ['Silver', 'II'], 
             10: ['Silver', 'I'], 11: ['Gold', 'V'], 12: ['Gold', 'IV'], 13: ['Gold', 'III'], 14: ['Gold', 'II'], 
             15: ['Gold', 'I'], 16: ['Platinum', 'V'], 17: ['Platinum', 'IV'], 18: ['Platinum', 'III'], 19: ['Platinum', 'II'], 
             20: ['Platinum', 'I'], 21: ['Diamond', 'V'], 22: ['Diamond', 'IV'], 23: ['Diamond', 'III'], 24: ['Diamond', 'II'], 
             25: ['Diamond', 'I'], 26: ['Ruby', 'V'], 27: ['Ruby', 'IV'], 28: ['Ruby', 'III'], 29: ['Ruby', 'II'], 
             30: ['Ruby', 'I']}

def today_baekjoon(id: str,틀린문제표기): #백준 아이디를 입력받으면 오늘 푼 문제를 return
    if 틀린문제표기:
        link = "https://www.acmicpc.net/status?user_id="+id
    else:
        link = "https://www.acmicpc.net/status?user_id="+id+"&result_id=4"
    sum = 0
    page = requests.get(link , headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    embed=discord.Embed(title="오늘의 정산", url=link,color=discord.Color.random())
    #솔브닥 오전 6시 초기화 기준으로 바운더리 설정
    today_datetime = datetime.today()
    today_year = today_datetime.year
    today_month = today_datetime.month
    today_day = today_datetime.day
    today_hour = today_datetime.hour
    if today_hour < 6:
        start_boundary = datetime(today_year,today_month,today_day)- timedelta(hours=18)
        end_boundary = datetime(today_year,today_month,today_day)+ timedelta(hours=6)
        # print(start_boundary,end_boundary)
    else:
        start_boundary = datetime(today_year,today_month,today_day)+ timedelta(hours=6)
        end_boundary = datetime(today_year,today_month,today_day)+ timedelta(hours=30)
        # print(start_boundary,end_boundary)
    #오늘 푼 문제를 고름
    if len(soup.find_all("tr")) == 1: #데이터 없음
        embed.add_field(name= "사용자를 찾을 수 없습니다", value= "제대로 입력하세요", inline=False)
    else:
        url = "https://solved.ac/api/v3/user/show"

        querystring = {"handle":id}

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers, params=querystring)

        strike = response.json()["maxStreak"]
        
        embed.set_author(name=id, url="https://solved.ac/profile/"+id, icon_url=response.json()["profileImageUrl"])
        prob_list = soup.find_all("tr")
        for i in range(1,len(prob_list)):
            time_str = prob_list[i].find_all("td")[8].find("a")["title"]
            datetime_prob = datetime.strptime(time_str,"%Y-%m-%d %H:%M:%S")
            if start_boundary <= datetime_prob and datetime_prob <= end_boundary:
                if "result-ac" in str(prob_list[i].find_all("td")[3]):
                    sum += 1
                submit_id = prob_list[i].find_all("td")[0].text
                prob_id = prob_list[i].find_all("td")[2].text
                prob_title = prob_list[i].find_all("td")[2].find("a")["title"]
                memory = prob_list[i].find_all("td")[4].text
                ms = prob_list[i].find_all("td")[5].text
                lang = prob_list[i].find_all("td")[6].text
                length = prob_list[i].find_all("td")[7].text
                solved_time = prob_list[i].find_all("td")[8].text
                temp1 = prob_id + " - "+prob_title +" ("+solved_time+")"
                temp2 = "메모리: " + memory + " KB, 시간: " + ms + " ms, 언어: " + lang + " [문제](https://www.acmicpc.net/problem/"+prob_id+")" +" / "+ " [코드](https://www.acmicpc.net/source/"+submit_id+")"
                embed.add_field(name = temp1, value = temp2, inline = False)
            else:
                break
        if sum == 0 and 틀린문제표기 == False:
            embed.add_field(name="정말로 한 문제도 안 푸셨네요" , value="문제 추천은 /랜덤 기능을 이용해 주세요" , inline=False)
        embed.set_footer(text="성공한 문제: "+str(sum) + ", 스트라이크: 연속 "+str(strike)+"일")
        return embed
    
def find_prob_by_id(prob_id,tier=False,algorithm=False): #솔브닥 api 이용
    try:
        url = 'https://solved.ac/api/v3/problem/show?problemId='+prob_id
        link = "https://www.acmicpc.net/problem/"+prob_id
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        data = response.json()
        description = "\n"
        if tier:
            tier_id = data["level"]
            tier_name = "".join(tier_data[tier_id])
            file_path = "./tier/"+tier_name+".png"
            file_name = tier_name+".png"
            description += "\n티어: "+ " ".join(tier_data[tier_id])
            pass
        else:
            file_path = "./tier/UK.png"
            file_name = "UK.png"

        if algorithm:
            description+="\n알고리즘 분류: "
            algo_list = []
            for i in data["tags"]:
                algo_list.append(i["displayNames"][0]["short"])
            description += ", ".join(algo_list)
        
        embed = discord.Embed(title=prob_id+" - "+data["titleKo"], description=description, url=link, color=discord.Color.random())
        file = discord.File(file_path, filename=file_name)
        embed.set_thumbnail(url="attachment://"+file_name)
    except Exception as e: #데이터 가져오는데 에러생기면 
        print(str(e))
        file_path = "./tier/notfound.png"
        file_name = "notfound.png"
        embed = discord.Embed(title="Not Found", description=prob_id+" 번은 존재하지 않는 문제입니다.", url="", color=discord.Color.random())
        embed.set_thumbnail(url="attachment://"+file_name) #404 사진 넣기
        file = discord.File(file_path, filename=file_name)
    finally:
        return file,embed

possible_tier = {'b': ['1', '2', '3', '4', '5'], 'b5': ['1'], 'b4': ['2'], 'b3': ['3'], 'b2': ['4'], 'b1': ['5'], 
 's': ['6', '7', '8', '9', '10'], 's5': ['6'], 's4': ['7'], 's3': ['8'], 's2': ['9'], 's1': ['10'], 
 'g': ['11', '12', '13', '14', '15'], 'g5': ['11'], 'g4': ['12'], 'g3': ['13'], 'g2': ['14'], 'g1': ['15'], 
 'p': ['16', '17', '18', '19', '20'], 'p5': ['16'], 'p4': ['17'], 'p3': ['18'], 'p2': ['19'], 'p1': ['20'], 
 'd': ['21', '22', '23', '24', '25'], 'd5': ['21'], 'd4': ['22'], 'd3': ['23'], 'd2': ['24'], 'd1': ['25'], 
 'r': ['26', '27', '28', '29', '30'], 'r5': ['26'], 'r4': ['27'], 'r3': ['28'], 'r2': ['29'], 'r1': ['30']}

def tier_to_id(tier_list): #["s1","s2","g5","g4"] --> ["9","10","11","12"]
    new_list = []
    for i in tier_list:
        if i.lower() not in possible_tier:
            raise Exception(str(i))
        else:
            new_list.extend(possible_tier[i])
    return list(set(new_list))

    
def rand_problem(tier_list):
    link = "https://www.acmicpc.net/problemset?sort=no_asc&tier="+",".join(tier_list)
    page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    pages = soup.find("ul",class_ = "pagination").find_all("li").__len__()
    #해당 티어를 모아둔 문제에서 페이지 개수를 가져온다

    rand_page = str(random.randint(1,pages))
    #페이지를 렌덤으로 뽑는다

    link = "https://www.acmicpc.net/problemset?sort=no_asc&tier="+",".join(tier_list) +"&page="+rand_page
    page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    #페이지에 들어간다

    number_of_problems = soup.find_all("tr").__len__()
    #해당 페이지에서 문제수를 가져온다

    rand_problem = random.randint(1,number_of_problems)
    #해당 페이지에서 랜덤으로 문제를 뽑는다

    final_rand_problem = soup.find_all("tr")[rand_problem-1].find("td","list_problem_id").text
    return final_rand_problem #문제 번호

def baekjoon_top3_language(id: str):
    top3 = []
    sum = 0
    link = "https://www.acmicpc.net/user/language/"+id
    page = requests.get(link , headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    table_row = soup.find("tbody").find_all("tr")
    for i in range(3):
        temp_list = []
        temp_list.append(table_row[i].find("th").text)
        temp_list.append(table_row[i].find("td").text)
        sum += int(table_row[i].find("td").text)
        top3.append(temp_list)
    for i in top3:
        i[1] = str(round(int(i[1])/sum*100,1))+"%"
    return top3

def prob_compare(my_id,your_id):
    my_list = request("https://www.acmicpc.net/user/"+my_id).find("div","problem-list").find_all("a")
    your_list = request("https://www.acmicpc.net/user/"+your_id).find("div","problem-list").find_all("a")
    my_set = set([i.text for i in my_list])
    your_set = set([i.text for i in your_list])
    sub_set = your_set-my_set
    diff_count = len(sub_set)

    if diff_count > 100:
        temp1 = your_id + "님은 신입니다!"
        temp2 = your_id+"님은 " +my_id+"님이 풀지 못한 " +str(diff_count)+"개의 문제들을 더 풀었습니다.\n너무 차이가 많이 나서 차집합에서 랜덤으로 100개를 뽑은 후 정렬을 시도하겠습니다.\n"
        embed = discord.Embed(title = temp1, description = temp2, url="", color=discord.Color.random())
    else:
        temp = your_id+"님은 " +my_id+"님이 풀지 못한 " +str(diff_count)+"개의 문제들을 더 풀었습니다.\n"
        embed=discord.Embed(title = "저놈도 풀었는데 ㅋㅋ 얼른 풀어야겠지?", description = temp,color=discord.Color.random())

    id_string = ",".join(list(sub_set)[:100])

    url = "https://solved.ac/api/v3/problem/lookup"

    querystring = {"problemIds":id_string}

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    sorted_data = sorted(data, key=lambda x: x["level"],reverse=True)
    sorted_data = sorted_data[:10]     # level이 큰 순서대로 10개의 항목 추출

    for item in sorted_data:
        temp1 = str(item["problemId"]) +" - "+ item["titleKo"]
        temp2 = "["+temp1+"](https://www.acmicpc.net/problem/"+str(item["problemId"])+")"
        embed.add_field(name = " ".join(tier_data[item["level"]]), value = temp2, inline = False)
    
    return embed


    
