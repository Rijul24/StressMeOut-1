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
import datetime


class Update(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check_any(commands.has_role("StressedOut"), commands.has_permissions(administrator=True))
    async def add(self, ctx, *, tada):
        tada = tada.split(";")
        
        #Addition latest
        check = tada[1]
        if check in ['Indefinite' , 'Coming Soon' ,'Soon', ' Indefinite',' Coming Soon']:
            with open("_data.json", "r") as f:
            _data = json.load(f)
            _data[str(ctx.guild.id)].append([tada[0].strip(), tada[1].strip()])
            #_data[str(ctx.guild.id)].sort(key=lambda val: datetime.datetime.strptime(val[1], '%Y %m %d %H %M'))
            with open("_data.json", "w") as f:
            json.dump(_data, f)
            await ctx.send("**successful**")
            
        if len(tada) - 2:
            await ctx.send("please provide 2 semicolon seperated arguments\n\
                      eg $add sample 1; 2021 05 10 23 59")
            return
        try:
            due = datetime.datetime.strptime(tada[1].strip(), '%Y %m %d %H %M')
        except ValueError:
            await ctx.send("format of date should be YYYY MM DD HH mm\n\
                      eg $add sample 1; 2021 05 10 23 59")
            return
        with open("_data.json", "r") as f:
            _data = json.load(f)
        _data[str(ctx.guild.id)].append([tada[0].strip(), tada[1].strip()])
        _data[str(ctx.guild.id)].sort(key=lambda val: datetime.datetime.strptime(val[1], '%Y %m %d %H %M'))
        with open("_data.json", "w") as f:
            json.dump(_data, f)
        await ctx.send("**successful**")

    @commands.command(aliases=["extend"])
    @commands.check_any(commands.has_role("StressedOut"), commands.has_permissions(administrator=True))
    async def update(self, ctx, *, tada):
        tada = tada.split(";")
        if len(tada) - 3:
            await ctx.send("please provide 3 semicolon seperated arguments\n\
                          eg $update 1; deadline; 2021 05 10 23 59\
                          eg $update 1; name; Sample assignment 3")
            return
        if tada[1].strip().lower() == "deadline":
            tada[1] = 2
        elif tada[1].strip().lower() == "name":
            tada[1] = 1
        else:
            await ctx.send("second argument should be name/deadline")
            return
        if tada[1] == 2:
            try:
                due = datetime.datetime.strptime(tada[2].strip(), '%Y %m %d %H %M')
            except ValueError:
                await ctx.send("format of date should be YYYY MM DD HH mm\n\
                          eg $update 1; deadline; 2021 05 10 23 59")
                return
        with open("_data.json", "r") as f:
            _data = json.load(f)
        idx = int(tada[0]) - 1
        leng = len(_data[str(ctx.guild.id)])
        if not (0 <= idx < leng):
            await ctx.send(f"first argument should be between 1 and {leng}(inclusive)")
            return
        _data[str(ctx.guild.id)][idx][tada[1] - 1] = tada[2].strip()
        _data[str(ctx.guild.id)].sort(key=lambda val: datetime.datetime.strptime(val[1], '%Y %m %d %H %M'))
        with open("_data.json", "w") as f:
            json.dump(_data, f)
        await ctx.send("**SUCCESSFUL**")

    @commands.command()
    @commands.check_any(commands.has_role("StressedOut"), commands.has_permissions(administrator=True))
    async def delete(self, ctx, pos):
        try:
            pos = int(pos)
        except ValueError:
            await ctx.send("enter valid int")
            return
        with open("_data.json", "r") as f:
            _data = json.load(f)
        if not 0 < pos <= len(_data[str(ctx.guild.id)]):
            await ctx.send(f"enter a int between 1 and {len(_data[str(ctx.guild.id)])}")
            return
        _data[str(ctx.guild.id)].pop(pos - 1)
        with open("_data.json", "w") as f:
            json.dump(_data, f)
        await ctx.send("**DELETED**")


def setup(client):
    client.add_cog(Update(client))
