
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
from discord.utils import get
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from commands.searchAnime import animeSearch
from commands.searchManga import mangaSearch
from commands.searchStudio import studioSearch
from commands.searchStaff import staffSearch
from commands.searchCharacter import charSearch
from commands.searchUser import *
from discord import HTTPException
from io import BytesIO
import aiohttp
from dotenv import load_dotenv



print(f"Importing .env configuration...")



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE1 = os.getenv('SAMPLE_RANGE1')
SAMPLE_RANGE2 = os.getenv('SAMPLE_RANGE2')

#can cahnge the prefix to anything you like
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
    embed.set_author(name='Help')
    embed.add_field(name=";ping", value = " Check you pingu\n", inline=False)
    embed.add_field(name=";info", value = "Server stats\n", inline=False)
    embed.add_field(name=";pfp <@user>", value = "Embeds your profile picture\n", inline=False)
    embed.add_field(name=";youtube <query>", value ="Search youtube for a video", inline=False)
    embed.add_field(name=";google <query>", value = "Search Google", inline=False)
    embed.add_field(name=';anime <title>', value="Search anime by title or ID.", inline=False)
    embed.add_field(name=';manga <title>', value="Search manga by title or ID.", inline=False)
    embed.add_field(name=';user <username>', value="Search up a user by their username.", inline=False)
    embed.add_field(name=';studio <studio name>', value="Search a studio by their name.", inline=False)
    embed.add_field(name=';staff <staff name>', value="Search an actor by their name.", inline=False)
    embed.add_field(name=';char <character name>', value="Search a character by their name.", inline=False)
    embed.add_field(name=';add <url> <name>', value="Add an emote", inline=False)
    embed.add_field(name=';delete <name>', value="Delete an emote", inline=False)
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
		await ctx.channel.send(f"Here are your results {author}!")
		async with ctx.typing():	#makes the bot appear as typing
				for j in search(query, tld="co.in", num=1, stop=1, pause=2):	#can loop and show more results instead of just the first
						await ctx.send(f"\n:point_right: {j}")

#Pfp command, embeds it
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

#EMOJI ADDING/Removing
@bot.command()
async def add(ctx, url: str, *, name):
	guild = ctx.guild
	if ctx.author.guild_permissions.manage_emojis:
		async with aiohttp.ClientSession() as ses:
			async with ses.get(url) as r:

				try:
					img_or_gif = BytesIO(await r.read())
					b_value = img_or_gif.getvalue()
					if r.status in range(200, 299):
						emoji = await guild.create_custom_emoji(image=b_value, name=name)
						await ctx.send(f'Successfully created emoji: <:{name}:{emoji.id}>')
						await ses.close()
					else:
						await ctx.send(f'Error when making request | {r.status} response.')
						await ses.close()

				except discord.HTTPException:
					await ctx.send('File size is too big!')

@bot.command()
async def delete(ctx, emoji: discord.Emoji):
	guild = ctx.guild
	if ctx.author.guild_permissions.manage_emojis:
		await ctx.send(f'Successfully deleted (or not): {emoji}')
		await emoji.delete()
	
	
#ANILIST SECTION
@bot.command(aliases=["ANIME", "a"])
async def anime(ctx, *, title):
    embed = animeSearch(title)
    await ctx.send(embed=embed)

@bot.command(aliases=["MANGA", "m"])
async def manga(ctx, *, title):
    embed = mangaSearch(title)
    await ctx.send(embed=embed)

@bot.command(aliases=['STUDIO', 's'])
async def studio(ctx, *, studioName):
    embed = studioSearch(studioName)
    await ctx.send(embed=embed)


@bot.command(aliases=['STAFF', 'st'])
async def staff(ctx, *, staffName):
    embed = staffSearch(staffName)
    await ctx.send(embed=embed)


@bot.command(aliases=["CHARACTER", 'ch', 'char'])
async def character(ctx, *, charName):
    embed = charSearch(charName)
    await ctx.send(embed=embed)

@bot.command(aliases=['USER', 'u'])
async def user(ctx, *, userName):
    result = generateUserInfo(userName)
    if result:
        try:
            userEmbed = userSearch(result)
            await ctx.send(embed=userEmbed)

            userAnimeEmbed = userAnime(result)
            await ctx.send(embed=userAnimeEmbed)

            userMangaEmbed = userManga(result)
            await ctx.send(embed=userMangaEmbed)

        except HTTPException:
            pass
    else:
        await ctx.send(embed=userError(userName))

	
#making the bot react to strings
@bot.listen()
async def on_message(message):
    if "cool" in message.content.lower(): #Replace cool with preferred str
        if message.author==bot.user :
            return
        else:
            await message.channel.send('url goes here')
            await bot.process_commands(message)


#reacting to everyone/bot being pinged
@bot.listen('on_message')
async def on_message(message):
    if message.author==bot.user :
        return
    else:
        if message.mention_everyone:     #Reacts to @everyone pings
            await message.channel.send('url goes here')
        else:
            return

@bot.listen()
async def on_message(message):
    if 'cool' in message.content.lower():    #Replace cool with preferred str
        if message.author==bot.user:
            return
        else :
            emoji = 'Emote goes here'   #Put the wanted emote, for custom emotes it's <:EmojiName:EmojiID>
            await message.add_reaction(emoji)


#Events          
@bot.event
async def on_ready():
    #edit this to change it's rich presence 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=";help"))
    print('Up and Running!')



bot.run(TOKEN)
