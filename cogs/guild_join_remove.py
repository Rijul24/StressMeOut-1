from discord.ext import commands
import json


class GuildJoinRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("_data.json", "r") as f:
            data = json.load(f)
        data[str(guild.id)] =[
            ["sample assignment 1", "2022 06 10 10 00"],
            ["sample test 1", "2022 08 01 23 59"]
        ]
        with open("_data.json", "w") as f:
            json.dump(data, f)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("_data.json", "r") as f:
            data = json.load(f)
        data.pop(str(guild.id))
        with open("_data.json", "w") as f:
            json.dump(data, f)


def setup(client):
    client.add_cog(GuildJoinRemove(client))
