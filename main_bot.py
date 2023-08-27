import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import asyncio
#만든 함수
from functions import *
from user_check import *

token = 'MTEzODc0MTk2NjkyMjg0NjIzOA.GWpSql.yaWRnXRgzVWPZeNVjZHpohdIpaGWoeZEBgTMGg'
error_red = 0xf44336 
noerror_green = 0x388e3c
# guild=discord.Object(id=1110101899312631808)
guild = None

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

def error_maker(error_type: int = 0,*args):
    """
    0: 기본 에러
    1: 백준 아이디 존재 안함 , *args = (baekjoon_id,)
    2: 디스코드 식별번호에 대응하는 백준 아이디가 존재 하지 않음, *args = (interation.user,)
    3: exception error, *args = (e,)
    4: 올바르지 않은 티어 범위 *args = (잘못된 범위,)
    """
    if error_type == 0: 
        embed=discord.Embed(title=f"에러", description="에러가 발생했습니다.",color=error_red)
    elif error_type == 1:
        embed=discord.Embed(title=f"'{args[0]}' 은/는 존재하지 않는 백준 아이디입니다.", description=f"다시 입력해 주세요.",color=error_red)
    elif error_type == 2: 
        embed=discord.Embed(title=f"'{args[0]}' 님의 백준 아이디는 등록되어 있지 않습니다.", description="/등록 명령어를 사용하여 백준 아이디를 등록하여 주세요.",color=error_red)
    elif error_type == 3: 
        embed=discord.Embed(title=f"코드 오류", description=args[0],color=error_red)
    elif error_type == 4: 
        embed=discord.Embed(title=f"'{args[0]}' 은/는 올바른 범위가 아닙니다.", description="올바른 범위를 입력해 주세요.",color=error_red)
    
    return embed


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    await asyncio.gather(
        client.change_presence(activity = discord.Game(name = "너를 감시")),
        tree.sync(guild=guild),
    )


@tree.command(name="today", description="오늘 백준에서 푼 문제를 보여줍니다.",guild=guild)
@app_commands.describe( 
    baekjoon_id = "검색하고 싶은 백준 아이디를 입력합니다. /등록 기능을 이용하시면 매번 자신의 아이디를 입력할 필요가 없습니다.",
    틀린문제표기 = "성공하지 못한 문제 표기할지 말지 선택합니다. 기본값은 False입니다."
 )
async def today_command(interaction, baekjoon_id: str = None,틀린문제표기: bool = False):
    print(f"{interaction.guild}에서 {interaction.user}: {interaction.data}")
    try:
        if baekjoon_id == None: #id가 입력되지 않으면 저장된 데이터에서 찾아봄
            find = get_user_value(interaction.user.id)
            if find == None:
                await interaction.response.send_message(embed = error_maker(2,interaction.user))
                return
            else:
                baekjoon_id= find

        if check_baekjoon_id(baekjoon_id) == False:
            await interaction.response.send_message(embed = error_maker(1,baekjoon_id))
            return
        embed = today_baekjoon(baekjoon_id,틀린문제표기) 
        await interaction.response.send_message(embed=embed)
        return
    except Exception as e:
        await interaction.response.send_message(embed = error_maker(3,e))
        return


@tree.command(name="출석", description="현재 연속 출석 일수와 최대 연속 출석 일수를 보여줍니다.",guild=guild)
@app_commands.describe( 
    baekjoon_id = "검색하고 싶은 백준 아이디를 입력합니다. /등록 기능을 이용하시면 매번 자신의 아이디를 입력할 필요가 없습니다.",
 )
async def today_command(interaction, baekjoon_id: str = None):
    print(f"{interaction.guild}에서 {interaction.user}: {interaction.data}")
    try:
        if baekjoon_id == None: #id가 입력되지 않으면 저장된 데이터에서 찾아봄
            find = get_user_value(interaction.user.id)
            if find == None:
                await interaction.response.send_message(embed = error_maker(2,interaction.user))
                return
            else:
                baekjoon_id= find

        if check_baekjoon_id(baekjoon_id) == False:
            await interaction.response.send_message(embed = error_maker(1,baekjoon_id))
            return
        link = f"https://solved.ac/profile/{baekjoon_id}"
        response = requests.get(link)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            temp1 = soup.find_all("div","css-18g9mtb")[0]
            temp2 = temp1.find_all("b")
            current_strike = temp2[0].text
            max_strike = temp2[1].text
            print(temp1.find_all("rect"))
            embed=discord.Embed(title=f"현재 {current_strike}일 연속 문제 풀이중!", description=f"아이디 : {baekjoon_id}",color=discord.Color.random())

            await interaction.response.send_message(embed = embed)
            return
        elif response.status_code == 404:
            await interaction.response.send_message(embed = error_maker(1,baekjoon_id))
            return
        
    except Exception as e:
        await interaction.response.send_message(embed = error_maker(3,e))
        return



@tree.command(name="등록", description="백준 아이디를 등록합니다. 이미 등록되어 있을 경우 새로운 값으로 업데이트됩니다.",guild=guild)
async def baekjoon_id_register(interaction, baekjoon_id: str):
    print(f"{interaction.guild}에서 {interaction.user}: {interaction.data}")
    try:
        if update_user_value(interaction.user.id,baekjoon_id) == None:
                await interaction.response.send_message(embed = error_maker(1,baekjoon_id))
                return
        else:
            embed=discord.Embed(title=f"{interaction.user}님의 백준 아이디가 성공적으로 등록되었습니다!", description=f"아이디 : {baekjoon_id}",color=noerror_green)
            await interaction.response.send_message(embed=embed)
            return
    except Exception as e:
            await interaction.response.send_message(embed = error_maker(3,e))
            return


@tree.command(name="문제",description="백준 문제를 찾아보는 명령어입니다. 티어와 알고리즘을 표기할 수 있습니다. ",guild=guild)
@app_commands.describe( 
    id='백준 문제번호입니다.',
    tier='티어를 표시할지 말지 선택합니다. 기본값은 False입니다.',
    algorithm='알고리즘을 표시할지 말지 선택합니다. 기본값은 False입니다.'
 )
async def 문제(interaction, id: str, tier: bool = False, algorithm: bool = False):
    print(f"{interaction.guild}에서 {interaction.user}: {interaction.data}")
    try:
        file, embed = find_prob_by_id(id, tier, algorithm)
        await interaction.response.send_message(file=file, embed=embed)
        return
    except Exception as e:
        await interaction.response.send_message(embed = error_maker(3,e))
        return


@tree.command(name = "랜덤",description="랜덤으로 문제를 추천해 줍니다. 티어 범위를 설정할 수 있습니다.",guild=guild)
@app_commands.describe(
    범위 = "영문 첫 글자 + 숫자 (e.g. s4, g1) 혹은 영문 첫 글자 (e.g. b, s, g, p, d, r)를 쉼표로 구분하여 입력하여 주세요. (e.g. s, g4)",
    tier='티어를 표시할지 말지 선택합니다. 기본값은 False입니다.',
    algorithm='알고리즘을 표시할지 말지 선택합니다. 기본값은 False입니다.',
    한국어 = "한국어 문제만 추천할지 선택합니다. 기본값은 True입니다."
 )
async def 랜덤(interaction,범위: str,tier: bool = False, algorithm: bool = False,한국어: bool = True):
    print(f"{interaction.guild}에서 {interaction.user}: {interaction.data}")
    try:
        범위 = 범위.replace(" ","")
        범위 = 범위.split(",")
        범위 = tier_to_id(범위) #티어에 대응하는 id로 바꿈
        prob_id = rand_problem(범위) #범위 내에서 문제를 랜덤으로 뽑아옴
        file,embed = find_prob_by_id(prob_id,tier=tier,algorithm=algorithm) #문제를 출력함
        await interaction.response.send_message(file=file, embed=embed)
        return
    except Exception as e: 
        await interaction.response.send_message(embed = error_maker(4,str(e)))
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if message.content.startswith('/today'): #/today 명령어
    #     print(message.author,", 명령어: today")
    #     # try:
        #     cmd = message.content.split()
        #     if len(cmd) == 1: #user id가 입력되지 않으면
        #         if message.author.id in user_data: #미리 저장된 디스코드 사용자 id 가 있는지 확인
        #             baekjoon_id = user_data[message.author.id]
        #         else: #데이터베이스에 없을 시 에러 출력
        #             await message.channel.send("유저 id를 입력하세요!")
        #     else:
        #         baekjoon_id = cmd[1]
        #     embed = today_baekjoon(baekjoon_id)
        #     await message.channel.send(embed = embed)
        # except Exception as e:
        #     print(e)
        #     await message.channel.send("사용자를 찾을 수 없습니다.")

    # elif message.content.startswith("/문제"):
    #     if message.content.split().__len__() == 1:
    #         await message.channel.send("문제 번호를 입력하세요.")
    #     else:
    #         tier = False
    #         algorithm = False
    #         prob_num = message.content.replace("/문제","")
    #         prob_num = prob_num.replace(" ","")
    #         if "티어" in message.content:
    #             tier = True
    #             prob_num = prob_num.replace("티어","")
    #         if "알고리즘" in message.content:
    #             algorithm = True      
    #             prob_num = prob_num.replace("알고리즘","")
    #         file,embed = find_prob_by_id(prob_num,tier,algorithm)
    #         await message.channel.send(file = file,embed=embed)

    # elif message.content.startswith("/랜덤"):
    #     try:
    #         tier_list = message.content.replace("/랜덤","")
    #         tier_list = tier_list.replace(" ","")
    #         tier_list = tier_list.split(",")
    #         tier_list = tier_to_id(tier_list)
    #         file,embed = rand_problem(tier_list)
    #         await message.channel.send(file = file,embed=embed)
    #     except Exception as e:
    #         await message.channel.send(str(e))
    
    elif message.content.startswith("마법소녀GH99님"):
        await message.channel.send(":emoji_1:")
    
    elif message.content.startswith("/언어"):
        try:
            id = message.content.replace("/언어","")
            id = id.replace(" ","")
            top3 = baekjoon_top3_language(id)
            embed=discord.Embed(title="사용 언어",color=discord.Color.random())
            for i in top3:
                embed.add_field(name=i[0], value=i[1], inline=True)
            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send(str(e))
    

    elif message.content.startswith("//"):
        embed=discord.Embed(title=" ")
        embed.set_author(name="guhyun9454", icon_url="https://static.solved.ac/tier_small/11.svg")
        embed.set_thumbnail(url="https://static.solved.ac/misc/360x360/default_profile.png")
        embed.add_field(name="문제 해결", value="204", inline=False)
        embed.add_field(name="티어: Gold V", value="진척도: 0.0067%", inline=False)
        embed.add_field(name="사용 언어", value="Python 3 : 47%, C++17 : 49.3%, C99 : 3.2%", inline=False)
        embed.add_field(name="스트라이크", value="연속 23일", inline=True)
        await message.channel.send(embed = embed)


client.run(token)
