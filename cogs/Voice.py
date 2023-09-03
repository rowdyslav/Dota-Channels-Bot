from discord.ext import commands
import discord
# import asyncio
from setup import LIVE_CHANNELS
from setup import COLLECTION as DB_CHANNELS

from setup import get_error_info


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None or before.channel == after.channel:
            return
        try:
            channel_id = after.channel.id
            worked = list(filter(lambda x: x.lobby_id == channel_id, LIVE_CHANNELS))
            if worked:
                cfg = worked[0]
                categ = self.client.get_channel(cfg.categ_id)
                if isinstance(categ, discord.CategoryChannel):
                    voice_order = get_voice_order(categ.name, DB_CHANNELS)
                    new_channel = await categ.create_voice_channel(
                        name=cfg.voice_name.format(voice_order),
                        user_limit=cfg.user_limit
                    )
                    DB_CHANNELS.insert_one(
                        {"Категория": categ.name, "ID войса": new_channel.id, "Номер": voice_order}
                    )
                    await member.move_to(new_channel)
        except Exception as e:
            print(get_error_info(__file__, e))


def get_voice_order(categ_name, col):
    a = list(col.find({"Категория": categ_name}))
    b = list(sorted([x["Номер"] for x in a]))
    n = len(b)
    if n == 0 or b[0] != 1:
        return 1

    for i in range(1, n):
        if b[i] - b[i - 1] > 1:
            return b[i - 1] + 1

    return b[-1] + 1


async def setup(client):
    await client.add_cog(Voice(client))
