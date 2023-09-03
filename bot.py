from dotenv import load_dotenv
import os
import asyncio
import discord
from discord.ext import commands

from setup import COLLECTION

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CLIENT = commands.Bot(command_prefix='!', intents=discord.Intents.all())

COLLECTION.delete_many({})


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await CLIENT.load_extension(f'cogs.{filename[:-3]}')
            print(f'Модуль {filename[:-3]} загружен!')


async def main():
    async with CLIENT:
        await load()
        await CLIENT.start(TOKEN)


@CLIENT.event
async def on_ready():
    await CLIENT.change_presence(activity=discord.Game(''))
    print('бот робит двк')


asyncio.run(main())

# https://discord.com/api/oauth2/authorize?client_id=1113526591339909281&permissions=8&scope=bot
