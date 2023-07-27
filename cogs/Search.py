from discord.ext import commands
import discord
from setup import SEARCH_CHANNEL_ID
from setup import COLLECTION as DB_CHANNELS

from setup import get_error_info


class Search(commands.Cog):
    def __init__(self, client):
        self.search = None  # discord.TextChannel в on_ready()
        self.client: discord.Client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if before.channel == after.channel:
                return

            documents = [
                DB_CHANNELS.find_one({'ID войса': x.id})
                for x in (before.channel, after.channel)
                if x is not None
            ]

            for document in documents:
                if document and "ID серча" not in document:
                    emb = await self.create_embed(document)
                    message = await self.search.send(embed=emb)
                    DB_CHANNELS.update_one(
                        {"_id": document["_id"]},
                        {"$set": {"ID серча": message.id}}
                    )
                elif document and "ID серча" in document:
                    emb = await self.create_embed(document)
                    if not emb:  # Если create_embed() вернуло None, сообщение будет удалено, значит выйти из функции
                        return
                    message = await self.search.fetch_message(document["ID серча"])
                    await message.edit(embed=emb)
        except Exception as e:
            print(get_error_info(__file__, e))

    @commands.Cog.listener()
    async def on_ready(self):
        self.search = self.client.get_channel(SEARCH_CHANNEL_ID)

    async def create_embed(self, doc):
        voice = self.client.get_channel(doc["ID войса"])
        embed = discord.Embed()
        if not voice.members:  # Если участников нет то войс и сообщение будут удалены в RemoveEmpty.py
            return None
        embed.set_author(
            name=f"📢▸ Поиск +{voice.user_limit - len(voice.members)} игроков",
        )
        embed.set_thumbnail(url=voice.members[0].avatar)
        desc = []
        for vmember in voice.members:
            desc.append(f'- {vmember.mention}')
        desc.append(f"\n**✅ Присоединиться: {voice.mention}**")
        embed.description = '\n'.join(desc)
        return embed


async def setup(client):
    await client.add_cog(Search(client))
