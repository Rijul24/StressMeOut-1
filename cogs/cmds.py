from discord.ext import commands
from asyncio import sleep
from myembeds import *


class Cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stressme", "stressmeout"])
    async def stress(self, ctx):
        async with ctx.typing():
            await sleep(0)
        await ctx.send(embed=e_stress(ctx.guild.id))

    @commands.command()
    async def help(self, ctx):
        async with ctx.typing():
            await sleep(0)
        await ctx.send(embed=e_help(ctx))

    @commands.command()
    async def prefix(self, ctx):
        async with ctx.typing():
            await sleep(0)
        await ctx.send(embed=e_whatpref(ctx))


def setup(client):
    client.add_cog(Cmds(client))
