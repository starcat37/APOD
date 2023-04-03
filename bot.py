import discord
import requests
from bs4 import BeautifulSoup

f = open('token.txt', 'r')
bot_token = f.read()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

url = "https://apod.nasa.gov/"
response = requests.get(url)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #~apod
    if message.content == '~apod':
        #~apod today
        response.encoding = 'utf-8' #인코딩 설정
        response_html = response.text #html 파일 추출
        response_soup = BeautifulSoup(response_html, features='lxml') #soup 객체로 변환

        apod_date = response_soup.body.center.p.next_sibling.get_text().replace("\n", "")
        apod_title = response_soup.select_one('center > b').get_text()
        apod_explanation = response_soup.select_one('body > p').get_text().replace("\n", " ")[14:]
        apod_image = response_soup.select_one('body center p a img')['src']

        apod_embed = discord.Embed(title="Astronomy Picture of the Day", url="https://apod.nasa.gov/", description=f"{apod_date}")
        apod_embed.set_image(url="https://apod.nasa.gov/apod/" + apod_image)
        apod_embed.add_field(name=apod_title, value=apod_explanation)

        await message.channel.send(embed = apod_embed)

    #~apod YY-MM-DD
    if message.content == "~apod 00-00-00":
        print()

    #~apod alarm
    if message.content == "~apod alarm":
        print()

    #~apod help
    if message.content == "~apod help":
        print()

client.run(bot_token)