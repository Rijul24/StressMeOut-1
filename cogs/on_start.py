import discord
from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            # status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='you $stress out'
            )
        )
        print(f"Logged in as {self.client.user}")
        print("-----------------------------")


def setup(client):
    client.add_cog(Ready(client))
