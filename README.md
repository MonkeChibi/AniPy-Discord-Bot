# Python Discord Anilist Bot
**Discord bot** written in Python (3.9.7+), can be used as a template, also has Anilist (through Anilit's GraphQL API), OpenWeather and IQAIR's APIs for weather forecast
# Commands include : 
* server info 
* pfp 
* client ping 
* youtube search 
* google search
* emoji add/delete
* kick members
* ban/unban members
* weather forecast command
* Anilist commands : 
  * Search anime by title/ID
  * Search manga by title/ID
  * Search username ( also displays the user's favourites)
  * Search Character
  * Search Staff 
  * Search Studio (also displays the studio's top 5 anime)
# Requirements :
 * Python 3.9.7+
 * A Discord Developer Account which you can make [here](https://discord.com/developers/docs/intro)
 * [OpenWeather's Current Weather Data API](https://openweathermap.org/current) for weather command 
 * [IQAIR's API](https://api-docs.iqair.com/) for Air Quality Index in the weather command
 * Stuff listed in [requirements.txt](https://github.com/saronik/PythonDiscordBot/blob/main/requirements.txt)
# **To run :**
  1. Clone this repo.
  2. Modify the discord token in [.env](https://github.com/saronik/PythonDiscordBot/blob/main/.env) after getting the token the Discord Developer Portal
  3. Get your credentials.json file from [here](https://console.cloud.google.com/apis/credentials) after creating a project first. (Be sure the .json is in the same directory as the python(.py) or it won't work).
  4. Remember to put all the required API keys in correct places.
  5. Go into the directory folder and execute command `pip install -r requirements.txt`.
  6. Execute the bot with `python bot.py` command
  7. (*Optional*) If to be deployed on Heroku Make a procfile with `<worker : python Your_Bot_Name.py>` inside and no extensions.
