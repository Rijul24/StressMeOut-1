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

import os
import discord
from discord.ext import commands
from getpref import get_pref
import myembeds
import discord_slash
from flask_thing import keep_alive


print("Initializing...")


intents = discord.Intents.all()
client = commands.Bot(
    command_prefix=get_pref,
    intents=intents,
    case_insensitive=True,
    help_command=None,
    when_mentioned=True
)
slash = discord_slash.SlashCommand(client, sync_commands=True)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=myembeds.e_miss_perm_admin())
        return
    if isinstance(error, commands.CheckAnyFailure):
        await ctx.send(embed=myembeds.e_miss_perm_role())
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send(embed=myembeds.e_miss_perm_owner())
        return
    print(error)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"**Loaded {extension}**")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"**Unloaded {extension}**")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"**Reloaded {extension}**")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


token = os.getenv('TOKEN')


if __name__ == "__main__":
    # Run the bot with the token
    keep_alive()
    client.run(token)
