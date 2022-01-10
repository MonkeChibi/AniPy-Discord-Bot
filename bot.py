
print(f"Starting bot...")



import time
startTime = time.time()



print(f"Importing modules...")

import discord
from discord.ext import commands
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
from googlesearch import search
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
from discord.utils import get
from dotenv import load_dotenv
from discord import Member



print(f"Importing .env configuration...")



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#can cahnge the prefix to anything you like
#delete 'help_command=None' if you want default help command
bot = commands.Bot(command_prefix=';', help_command=None)
slash = SlashCommand(bot, sync_commands=True)


print(f"Startup complete!\t[ {(time.time()-startTime):.2f}s ]")


#custom help command
@slash.slash(name="help", description="Help Command")
async def help(ctx: SlashContext):
    embed=discord.Embed(title="Chibi Bot Help", description = "Use prefix '/' before <command>", color=discord.Color.blue())
    embed.set_author(name='Help')
    embed.add_field(name=";ping", value = " Check you pingu\n", inline=False)
    embed.add_field(name=";info", value = "Server stats\n", inline=False)
    embed.add_field(name=";pfp <@user>", value = "Embeds your profile picture\n", inline=False)
    embed.add_field(name=";youtube <query>", value ="Search youtube for a video", inline=False)
    embed.add_field(name=";google <query>", value = "Search Google", inline=False)
    embed.add_field(name=';anime <title>', value="Search anime by title or ID.", inline=False)
    embed.add_field(name=';manga <title>', value="Search manga by title or ID.", inline=False)
    embed.add_field(name=';user <username>', value="Search up a user by their username.", inline=False)
    embed.add_field(name=';reverse <image link>', value="Search an anime by a link to an image.", inline=False)
    embed.add_field(name=';studio <studio name>', value="Search a studio by their name.", inline=False)
    embed.add_field(name=';staff <staff name>', value="Search an actor by their name.", inline=False)
    embed.add_field(name=';char <character name>', value="Search a character by their name.", inline=False)
    embed.add_field(name=';add <url> <name>', value="Add an emote", inline=False)
    embed.add_field(name=';delete <name>', value="Delete an emote", inline=False)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)


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

@slash.slash(name="ban",
            description="ban members (if you have permission)",
            guild_ids=[],
            options=[create_option(name="member", description="name of the member", required=True, option_type=6),
                    create_option(name="reason", description="Reason for ban", required=False, option_type=3)]
            )
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    embed = discord.Embed(title='Chibi Bot', description='Moderation', color=discord.Color.red())
    embed.add_field(name=f'User {member} has been banned',value=f'Reason : {reason}', inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="unban",
            description="unban member",
            guild_ids=[],
            options=[create_option(name="member", description="name of the member", required=True, option_type=3)])
@commands.has_permissions(administrator = True)
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


#youtube search command
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
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

#Google search command
@slash.slash(name="google",
            description="Google search",
            options=[create_option(name="query", description="Term to be googled", required=True, option_type=3)])
async def google(ctx:SlashContext, query):
    await ctx.defer()
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):          #can loop to show multiple results
	       await ctx.send(f"{j}")

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
