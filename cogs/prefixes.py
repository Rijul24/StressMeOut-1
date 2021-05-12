from discord.ext import commands
import json


class Prefixes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

    @commands.command(aliases=["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def changepref(self, ctx, pref=None):
        if pref is None:
            ctx.send("Prefix is a required argument which is missing")
            return
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = pref
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
        await ctx.send(f"new prefix is {pref}")


def setup(client):
    client.add_cog(Prefixes(client))
