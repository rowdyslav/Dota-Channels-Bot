import os
import asyncio
import discord
from discord.ext import commands

token = os.environ['Anything']
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Модуль {filename[:-3]} загружен!')


async def main():
    async with client:
        await load()
        await client.start(token)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(''))
    print('бот робит двк')


asyncio.run(main())

# https://discord.com/api/oauth2/authorize?client_id=1113526591339909281&permissions=8&scope=bot
