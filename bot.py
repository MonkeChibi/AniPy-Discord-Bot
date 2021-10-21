
print(f"Starting bot...")



import time
startTime = time.time()



print(f"Importing modules...")



import os
import datetime
import re
from urllib import parse, request
from googlesearch import search
import re
import discord
from discord import Member
from discord.ext import commands
from dotenv import load_dotenv

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



print(f"Importing .env configuration...")



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE1 = os.getenv('SAMPLE_RANGE1')
SAMPLE_RANGE2 = os.getenv('SAMPLE_RANGE2')


#delete 'help_command=None' if you want default help command
bot = commands.Bot(command_prefix=';', help_command=None)



print("Initializing Google Authentication...")


creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()



print(f"Startup complete!\t[ {(time.time()-startTime):.2f}s ]")


#custom help command
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Chibi Bot Help", description = "Use prefix ';' before <command>", color=discord.Color.blue())
    embed.add_field(name="ping", value = " Check you pingu\n")
    embed.add_field(name="info", value = "server stats\n")
    embed.add_field(name="pfp", value = "embeds your profile picture\n")
    embed.add_field(name="youtube", value =";youtube <query>\n")
    embed.add_field(name="google", value = ";google <query>\n")
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)


#Google sheets search command
#@bot.command(name='find')
#async def testCommand(ctx, *args):
#    if(len(args)==0):
#        await ctx.send("Can't search for nothing retard")
#    else:
#        print('{0} rows retrieved.'.format(len(rows)))


#ping command
@bot.command()
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)


#exit command
#@bot.command(name='exit')
#async def testCommand(ctx, *args):
#    await ctx.send("Closing the Bot now")
#    exit()


#youtube search command
@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    async with ctx.typing():
        search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
        print(search_results)
        # You can loop to show more results
        await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

#Google search command
@bot.command()
async def google(ctx,*, query):
		author = ctx.author.mention
		await ctx.channel.send(f"Gibing results wait <:CollegeWale:895336406833070170> {author}")
		async with ctx.typing():
				for j in search(query, tld="co.in", num=1, stop=1, pause=2):
						await ctx.send(f"\n:point_right: {j}")

#Grabs the Pfp and embeds it
@bot.command()
async def pfp(ctx, member: Member = None):
 if not member:
     member = ctx.author
 embed = discord.Embed(title=f"{member}",color=0x40cc88, timestamp=ctx.message.created_at)
 embed.set_image(url=member.avatar_url)
 embed.set_footer(text=f"Requested by {ctx.author}")
 embed.set_thumbnail(url=bot.user.avatar_url)
 await ctx.send(embed=embed)


#Server Info command
@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="test bot", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{custom url}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=embed)

@bot.listen()
async def on_message(message):
    if "retard" in message.content.lower():
        if message.author==bot.user :
            return
        else:
            await message.channel.send('https://cdn.discordapp.com/emojis/899366731896737793.png?size=128')
            await bot.process_commands(message)


#reacting to everyone/bot being pinged
@bot.listen('on_message')
async def on_message(message):
    if message.author==bot.user :
        return
    else:
        if message.mention_everyone:
            await message.channel.send('https://cdn.discordapp.com/attachments/894206029745778721/900628932712349736/unknown.png')
        else:
            return

#Events          
@bot.event
async def on_ready():
    #edit this to change it's rich presence 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=";help"))
    print('Up and Running!')



bot.run(TOKEN)
