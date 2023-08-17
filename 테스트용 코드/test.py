import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import random
import os

id = "guhyun9454"

# tr: 문제 
# td: 문제 설명 
# 첫번째 td: 제출 번호
# 두번째 td: 유저 아이디
# 세번째 td: 문제 번호, 문제 이름, 문제 주소, 
# 네번째 td: 문제 번호

def today_baekjoon(id: str): #백준 아이디를 입력받으면 오늘 푼 문제를 return
    link = "https://www.acmicpc.net/status?user_id="+id
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
        print(start_boundary,end_boundary)
    else:
        start_boundary = datetime(today_year,today_month,today_day)+ timedelta(hours=6)
        end_boundary = datetime(today_year,today_month,today_day)+ timedelta(hours=30)
        print(start_boundary,end_boundary)
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
            print(time_str)
            datetime_prob = datetime.strptime(time_str,"%Y-%m-%d %H:%M:%S")
            if start_boundary <= datetime_prob and datetime_prob <= end_boundary:
                print(datetime_prob)
                if "result-ac" in str(prob_list[i].find_all("td")[3]):
                    sum += 1
                    prob_id = prob_list[i].find_all("td")[2].text
                    prob_title = prob_list[i].find_all("td")[2].find("a")["title"]
                    memory = prob_list[i].find_all("td")[4].text
                    ms = prob_list[i].find_all("td")[5].text
                    lang = prob_list[i].find_all("td")[6].text
                    length = prob_list[i].find_all("td")[7].text
                    solved_time = prob_list[i].find_all("td")[8].text
                    time_str = prob_list[i].find_all("td")[8].find("a")["title"]
                    print(time_str)
                
                    temp1 = prob_id + " - "+prob_title +" ("+solved_time+")"
                    temp2 = "메모리: " + memory + " KB, 시간: " + ms + " ms, 언어: " + lang 
                    embed.add_field(name = temp1, value = temp2 , inline = False)
            else:
                break
        if sum == 0:
            embed.add_field(name="정말로 한 문제도 안 푸셨네요" , value="문제 추천은 /랜덤 기능을 이용해 주세요" , inline=False)
        embed.set_footer(text="성공한 문제: "+str(sum) + ", 스트라이크: 연속 "+str(strike)+"일")
        return embed

print(today_baekjoon(id))