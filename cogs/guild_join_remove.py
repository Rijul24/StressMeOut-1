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
import json


class GuildJoinRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("_data.json", "r") as f:
            data = json.load(f)
        data[str(guild.id)] = [
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
