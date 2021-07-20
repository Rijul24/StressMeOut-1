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


import discord
from get_data import conv_list
from getpref import get_pref


invite = "https://github.com/armaanbadhan/StressMeOut/blob/main/help.md"
help_link = "https://github.com/armaanbadhan/StressMeOut/blob/main/help.md"


def e_stress():
    res = conv_list()
    embeded = discord.Embed(color=0x7289DA)
    if len(res) == 0:
        embeded.add_field(name="moj", value="no work to do huehuehue")
    else:
        for i in range(len(res)):
            embeded.add_field(
                value=format(res[i][1]),
                name="**" + str(res[i][0]) + "**",
                inline=False
                )
    return embeded


# not in use
def e_help(ctx):
    embeded = discord.Embed(
        colour=0x00FF00,
        title="HELP",
        description=f"full list of commands can be found [here]({help_link})"
    )


def e_miss_perm_admin():
    embeded = discord.Embed(
        color=0xFF0000,
        title="Missing Permissions",
        description="""You're missing permissions to run this command.\n\
        This command is marked as Admin only."""
        )
    return embeded


def e_miss_perm_owner():
    embeded = discord.Embed(
        color=0xFF0000,
        title="Missing Permissions",
        description="""You're missing permissions to run this command.\n\
        This command can only be used by Bot Owner."""
        )
    return embeded


def e_miss_perm_role():
    embeded = discord.Embed(
        color=0xFF0000,
        title="Missing Role",
        description="""You're missing permissions to run this command.\n\
        This command can only be used by members with "StressedOut" role or Administrator."""
        )
    return embeded


def e_whatpref(ctx):
    pre = get_pref('a', ctx)[0]
    embeded = discord.Embed(
        color=0x0000FF,
        title="StressMeOut Prefixes",
        description=f"""Bots custom prefix in this server is {pre}.\n\
            Bots Universal prefix is ' **#$** '
            You can also mention the bot
            You can change prefix using ('changepref' or 'changeprefix') command
            eg \" **#$change prefix %** \" to set % as prefix"""
    )
    return embeded
