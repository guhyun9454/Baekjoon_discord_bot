import discord
from discord.ext import commands
import requests

from bs4 import BeautifulSoup
import time
import random

token = 'MTEzODc0MTk2NjkyMjg0NjIzOA.GWpSql.yaWRnXRgzVWPZeNVjZHpohdIpaGWoeZEBgTMGg'
channel_id = "1110101899878879273"



# client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id) # 위와 같은 클래스에서 id 프로퍼티 출력
    print('------')

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title='title', description='description', url='https://howbeautifulworld.tistory.com/', color=discord.Color.random())
    embed.set_thumbnail(url="https://d2gd6pc034wcta.cloudfront.net/tier/12.svg")
    await ctx.send(embed=embed)

bot.run(token)
