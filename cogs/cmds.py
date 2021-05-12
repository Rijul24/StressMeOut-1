"""
MIT License

Copyright (c) 2021 armaanbadhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

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
