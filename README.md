# Python Discord Anilist Bot
**Basic Discord bot** written in Python (3.9.7), can be used as a template.
Uses the Anilist GraphOL API.
# Commands include : 
* server info 
* pfp 
* client ping 
* youtube search 
* google search
* Anilist commands : 
  * Search anime by title/ID
  * Search manga by title/ID
  * Search username ( also displays the user's favourites)
  * Search Character
  * Search Staff (also displays the studio's top 5 anime)
  * Search Studio
# Requirements :
 * Python 3.9.7+
 * A Discord Developer Account which you can make [here](https://discord.com/developers/docs/intro)
 * Stuff listed in [requirements.txt](https://github.com/saronik/PythonDiscordBot/blob/main/requirements.txt)
# **To run :**
  1. Clone this repo.
  2. Modify the discord token in [.env](https://github.com/saronik/PythonDiscordBot/blob/main/.env) after getting the token the Discord Developer Portal
  3. Get your credentials.json file from [here](https://console.cloud.google.com/apis/credentials) after creating a project first. (Be sure the .json is in the same directory as the python(.py) or it won't work).
  4. Go into the directory folder and execute command `pip install -r requirements.txt`.
  5. Execute the bot with `python bot.py` command
  6. (*Optional*) If to be deployed on Heroku Make a procfile with `<worker : python Your_Bot_Name.py>` inside and no extensions.
