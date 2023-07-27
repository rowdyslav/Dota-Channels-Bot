from discord.ext import commands
# import discord
from setup import COLLECTION as DB_CHANNELS

from setup import SEARCH_CHANNEL_ID

from setup import get_error_info


class RemoveEmpty(commands.Cog):
    def __init__(self, client):
        self.search = None  # discord.TextChannel в on_ready()
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            voice = before.channel
            document = DB_CHANNELS.find_one({'ID войса': voice.id})
            if document and voice is not None and len(voice.members) == 0:
                await voice.delete()
                message = await self.search.fetch_message(document["ID серча"])
                await message.delete()  # Удаление сообщения от Seacrh.py
                DB_CHANNELS.delete_one({'ID войса': voice.id})
        except Exception as e:
            get_error_info(__file__, e)

    @commands.Cog.listener()
    async def on_ready(self):
        self.search = self.client.get_channel(SEARCH_CHANNEL_ID)


async def setup(client):
    await client.add_cog(RemoveEmpty(client))
