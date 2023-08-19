import discord
from discord import app_commands
from discord.ext import commands
import requests

from bs4 import BeautifulSoup
import time
import random

token = 'MTEzODc0MTk2NjkyMjg0NjIzOA.GWpSql.yaWRnXRgzVWPZeNVjZHpohdIpaGWoeZEBgTMGg'


# client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity = discord.Game(name = "너를 감시"))


@bot.command(name="today", description="오늘 백준에서 푼 문제를 보여줍니다.", aliases=["정산", "hi"])
async def today_command(ctx, baekjoon_id: str = None):
    # Your command implementation
    print(1)
    pass

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title='title', description='description', url='https://howbeautifulworld.tistory.com/', color=discord.Color.random())
    embed.set_thumbnail(url="https://d2gd6pc034wcta.cloudfront.net/tier/12.svg")
    await ctx.send(embed=embed)

@bot.tree.command(name='hello', description='testing')  # 명령어 이름, 설명
@app_commands.describe(text1='쓸 내용', text2 = '번호') # 같이 쓸 내용들
async def hello(interaction: discord.Interaction, text1:str, text2:int):    # 출력
    await interaction.response.send_message(f'{interaction.user.mention} : {text1} : {text2}', ephemeral=True)

bot.run(token)
