#
# Copyright (C) 2020 vExo307. All rights reserved.
#
# For use with the Xbox 360 Hub Discord server
#
# Any other use is prohibited without express permission of vExo307
#
# This document may not be reproduced or transmitted in any form, in whole or in part, without
# the express written permission of vExo307.
#
import discord
import time
import datetime
import json
import os
import os.path
import secrets
import requests
import asyncio
from discord.ext import commands
from bs4 import BeautifulSoup

currentdirectory = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(currentdirectory, 'config.json')

with open(config, 'r+') as f:
  data = json.load(f)
client = commands.Bot(command_prefix = data['prefix'])

def getUser(gamertag):
    r = requests.get(url=f"https://xbl.io/api/v2/friends/search?gt={gamertag}", headers={"X-Authorization": data["xapikey"]})
    return r.text

def colorResolve(color):
    r = requests.get(url=color)
    color = json.loads(r.text)
    return color["primaryColor"]

@client.event
async def on_message(message):
    if(message.channel.id in data["allowedchannels"]):
        await client.process_commands(message)

@client.command()
async def gamertag(ctx, *, gamertag: str):
    user = json.loads(getUser(gamertag))
    if("code" in user):
        await ctx.channel.send("No user with that gamertag could be found, please ensure that you have spelt it correctly")
        return
    gamerpic = str(user["profileUsers"][0]["settings"][0]["value"])
    gamerscore = str(user["profileUsers"][0]["settings"][1]["value"])
    gamertag = str(user["profileUsers"][0]["settings"][2]["value"])
    subscription = str(user["profileUsers"][0]["settings"][3]["value"])
    rep = str(user["profileUsers"][0]["settings"][4]["value"])
    color = str(user["profileUsers"][0]["settings"][5]["value"])
    bio = str(user["profileUsers"][0]["settings"][7]["value"])
    tenure = str(user["profileUsers"][0]["settings"][8]["value"])
    if not bio:
        bio = "No Bio"
    if rep == "GoodPlayer":
        rep = "Good Player"
    if rep == "NeedsWork":
        rep = "Needs Work"
    if rep == "AvoidMe":
        rep = "Avoid Me"
    
    embed = discord.Embed(title="Gamertag Lookup", color=int(colorResolve(color), 16))
    embed.add_field(name="Gamertag", value=gamertag, inline="true")
    embed.add_field(name="Gamerscore", value=gamerscore, inline="true")
    embed.add_field(name="Subscription", value=subscription, inline="true")
    embed.add_field(name="Reputation", value=rep, inline="true")
    embed.add_field(name="Tenure", value=tenure, inline="true")
    embed.add_field(name="Bio", value=bio, inline="true")
    embed.set_footer(text="Xbox Bot", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=gamerpic)
    await ctx.channel.send(embed=embed)
    


client.run(data['token'])