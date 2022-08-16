
print(f"Starting bot...")



import time
startTime = time.time()



print(f"Importing modules...")

import discord
import asyncio
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
import re
import os
import datetime
import pickle
import os.path
import aiohttp
from io import BytesIO
from urllib import parse, request
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from commands.searchAnime import animeSearch
from commands.searchManga import mangaSearch
from commands.searchStudio import studioSearch
from commands.searchStaff import staffSearch
from commands.searchCharacter import charSearch
from commands.searchUser import *
from discord import HTTPException
from discord.utils import get
from dotenv import load_dotenv
from discord import Member



print(f"Importing .env configuration...")



print(f"Importing .env configuration...")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=";", intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
api_key= ""
iqair_key = ""
iqair_base = "https://api.airvisual.com/v2/nearest_city?"
base_url="http://api.openweathermap.org/data/2.5/weather?"
geo_url_base = "http://api.openweathermap.org/geo/1.0/direct?"
icon_url_base = "http://openweathermap.org/img/wn/"
Guild_ID = []


print(f"Startup complete!\t[ {(time.time()-startTime):.2f}s ]")


#custom help command
@slash.slash(name="help", description="Help Command")
async def help(ctx: SlashContext):
    page1 = discord.Embed(title="Chibi Bot Help", description = "Use prefix '/' before commands", color=discord.Color.blue())
    page1.set_author(name='Help')
    page1.add_field(name="ping", value = " Check you pingu\n", inline=False)
    page1.add_field(name="info", value = "Server stats\n", inline=False)
    page1.add_field(name="pfp ", value = "Embeds your profile picture\n", inline=False)
    page1.add_field(name="youtube ", value ="Search youtube for a video", inline=False)
    page1.add_field(name="google ", value = "Search Google", inline=False)
    page1.set_thumbnail(url=bot.user.avatar_url)

    page2=discord.Embed(title="Chibi Bot Help", description = "Use prefix ';' before <command>", color=discord.Color.blue())
    page2.set_author(name='Help')
    page2.add_field(name='anime ', value="Search anime by title or ID.", inline=False)
    page2.add_field(name='manga ', value="Search manga by title or ID.", inline=False)
    page2.add_field(name='user ', value="Search up a user by their username.", inline=False)
    page2.add_field(name='reverse', value="Search an anime by a link to an image.", inline=False)
    page2.add_field(name='studio ', value="Search a studio by their name.", inline=False)
    page2.add_field(name='staff ', value="Search an actor by their name.", inline=False)
    page2.add_field(name='char ', value="Search a character by their name.", inline=False)
    page2.set_thumbnail(url=bot.user.avatar_url)

    page3=discord.Embed(title="Chibi Bot Help", description = "Use prefix ';' before <command>", color=discord.Color.blue())
    page3.set_author(name='Help')
    page3.add_field(name='add ', value="Add an emote", inline=False)
    page3.add_field(name='delete ', value="Delete an emote", inline=False)
    page3.add_field(name='weather', value="Search the weather and AQI of any place", inline=False)
    page3.set_thumbnail(url=bot.user.avatar_url)
    bot.help_pages = [page1, page2, page3]

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])


#Moderation commands : Kicking/Banning Members
@slash.slash(name="kick",
            description="kick members (if you have permission)",
            guild_ids=[],
            options=[create_option(name="member", description="name of the member", required=True, option_type=6),
            
                    create_option(name="reason", description="Reason for kick", required=False, option_type=3)]
            )
@bot.command(pass_context=True, name="kick")
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    embed = discord.Embed(title='Chibi Bot', description='Moderation', color=discord.Color.red())
    embed.add_field(name=f'User {member} has been kicked',value=f'Reason : {reason}', inline=False)
    await ctx.send(embed=embed)

#Moderation commands
@slash.slash(name="kick",
            description="kick members (if you have permission)",
            guild_ids=Guild_ID,
            options=[create_option(name="member", description="name of the member", required=True, option_type=6),
                    create_option(name="reason", description="Reason for kick", required=False, option_type=3)]
            )
@bot.command(pass_context=True, name="kick")
@has_permissions(ban_members = True, manage_roles=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    embed = discord.Embed(title='Chibi Bot', description='Moderation', color=discord.Color.red())
    embed.add_field(name=f'User {member} has been kicked',value=f'Reason : {reason}', inline=False)
    await ctx.send(embed=embed)
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry you do not have the perms"
        await bot.send_message(ctx.message.channel, text)


@slash.slash(name="ban",
            description="ban members (if you have permission)",
            guild_ids=Guild_ID,
            options=[create_option(name="member", description="name of the member", required=True, option_type=6),
                    create_option(name="reason", description="Reason for ban", required=False, option_type=3)]
            )
@has_permissions(ban_members = True, manage_roles=True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    embed = discord.Embed(title='Chibi Bot', description='Moderation', color=discord.Color.red())
    embed.add_field(name=f'User {member} has been banned',value=f'Reason : {reason}', inline=False)
    await ctx.send(embed=embed)



@slash.slash(name="unban",
            description="unban member",
            guild_ids=Guild_ID,
            options=[create_option(name="member", description="name of the member", required=True, option_type=3)])
@has_permissions(administrator = True, manage_roles=True)
async def unban(ctx:SlashContext, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title='Chibi Bot', description='Moderation', color=discord.Color.red())
            embed.add_field(name=f'Unbanned {user.mention}', value=f'User {member} has been unbanned', inline=False)
            await ctx.send(embed=embed)

            return



#ping command
@slash.slash(name="ping", description="Ping command")
async def ping(ctx: SlashContext):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)


#exit command, recommended to role or ID lock it
#@bot.command(name='exit')
#async def testCommand(ctx, *args):
#    await ctx.send("Closing the Bot now")
#    exit()

#Google Search Command
@slash.slash(name="google",
            description="Google search",
            options=[create_option(name="query", description="Term to be googled", required=True, option_type=3)])
async def google(ctx:SlashContext, query):
    await ctx.defer()

    def get_source(url):
        try :
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)
    
    def scrape_google(query):
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.in/search?q=" + query)

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')
        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
    results = scrape_google(query)
    print(results)

    Gpage1= results[0]
    Gpage2= results[1]
    Gpage3= results[2]
    bot.g_pages=[Gpage1, Gpage2, Gpage3]
    buttons=[u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current=0
    msg=await ctx.send(bot.g_pages[current])

    for button in buttons:
        await msg.add_reaction(button)
    
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.00)
        except asyncio.TimeoutError:
            return print("test")
        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
            elif reaction.emoji == u"\u2B05" :
                if current > 0:
                    current -=1
            elif reaction.emoji ==  u"\u27A1":
                if current < len(bot.g_pages)-1:
                    current +=1
            elif reaction.emoji == u"\u23E9":
                current = len(bot.g_pages)-1
            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            if current != previous_page:
                message = bot.g_pages[current]
                await msg.edit(content=message)


#Youtube search command
@slash.slash(name = "youtube",
            description="Youtube Search",
            options=[create_option(name="query", description="Term to be searched", required=True, option_type=3)])
async def youtube(ctx:SlashContext, query):
    await ctx.defer()
    query_string = parse.urlencode({'search_query': query})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    yt_page1 = ('https://www.youtube.com/watch?v=' + search_results[0])
    yt_page2 = ('https://www.youtube.com/watch?v=' + search_results[1])
    yt_page3 = ('https://www.youtube.com/watch?v=' + search_results[2])
    yt_page4 = ('https://www.youtube.com/watch?v=' + search_results[3])
    yt_page5 = ('https://www.youtube.com/watch?v=' + search_results[4])
    bot.yt_pages = [yt_page1, yt_page2, yt_page3, yt_page4, yt_page5]
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await ctx.send(bot.yt_pages[current])

    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(bot.yt_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.yt_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                message = bot.yt_pages[current]
                await msg.edit(content=message)


#Pfp command, embeds it
@slash.slash(name="pfp",
            description="Embeds your pfp",
            guild_ids=[],
            options=[create_option(name="member", description="can leave blank if you just want yours", required=False, option_type=6)])
async def pfp(ctx:SlashContext, member: Member = None):
    if not member:
            member = ctx.author
    embed = discord.Embed(title=f"{member}",color=0x40cc88)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


#Server Info command
@slash.slash(name="info",
            description="Server Info",
            guild_ids=[])
async def info(ctx:SlashContext):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Chibi's bot", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{custom url}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=embed))

#EMOJI ADDING/Removing
@slash.slash(name="add",
            description="add an emote",
            guild_ids=[],
            options=[create_option(name="url", description="Emote link/png", required=True, option_type=3),
                    create_option(name="name", description="Emote Name", required=True, option_type=3)])
async def add(ctx:SlashContext, url: str, name):
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
#Command to delete emotes is still using the old command prefix
@bot.command()
async def delete(ctx, emoji: discord.Emoji):
	guild = ctx.guild
	if ctx.author.guild_permissions.manage_emojis:
		await ctx.send(f'Successfully deleted (or not): {emoji}')
		await guild.delete_custom_emoji(emoji)
	
	
#ANILIST SECTION
@slash.slash(name="anime",
            description="Search for anime on Anilist",
            guild_ids=[],
            options=[create_option(name="title", description="Title of anime", required=True, option_type=3)])
async def anime(ctx:SlashContext, title):
    embed = animeSearch(title)
    await ctx.send(embed=embed)

@slash.slash(name="manga",
            description="Search for manga on Anilist",
            guild_ids=[],
            options=[create_option(name="title", description="Title of manga", required=True, option_type=3)])
async def manga(ctx:SlashContext, title):
    embed = mangaSearch(title)
    await ctx.send(embed=embed)

@slash.slash(name="studio",
            description="Search for studio on Anilist",
            guild_ids=[],
            options=[create_option(name="studioname", description="studio name", required=True, option_type=3)])
async def studio(ctx:SlashContext , studioname):
    embed = studioSearch(studioname)
    await ctx.send(embed=embed)

@slash.slash(name="staff",
            description="Search for staff on Anilist",
            guild_ids=],
            options=[create_option(name="staffname", description="staff name", required=True, option_type=3)])
async def staff(ctx:SlashContext, staffname):
    embed = staffSearch(staffname)
    await ctx.send(embed=embed)

@slash.slash(name="char",
            description="Search for character on Anilist",
            guild_ids=[],
            options=[create_option(name="charname", description="name of the character", required=True, option_type=3)])
async def character(ctx:SlashContext, charname):
    embed = charSearch(charname)
    await ctx.send(embed=embed)


@slash.slash(name="user",
            description="Search for user on Anilist",
            guild_ids=[],
            options=[create_option(name="username", description="username of anilist", required=True, option_type=3)])
async def user(ctx:SlashContext, username):
    result = generateUserInfo(username)
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
        await ctx.send(embed=userError(username))


	
#making the bot react to strings
@bot.listen()
async def on_message(message):
    if "cool" in message.content.lower(): #Replace cool with preferred keyword(s)
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
    if 'cool' in message.content.lower():    #Replace cool with preferred keyword(s)
        if message.author==bot.user:
            return
        else :
            emoji = 'Emote goes here'   #Put the wanted emote, for custom emotes it's <:EmojiName:EmojiID>
            await message.add_reaction(emoji)


#Events          
@bot.event
async def on_ready():
    #edit this to change it's rich presence 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    print('Up and Running!')



bot.run(TOKEN)
