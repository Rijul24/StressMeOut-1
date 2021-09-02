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
import discord_slash

from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or
from utils import myembeds
from utils.flask_thing import keep_alive

from constants import LOGGING_CHANNEL_ID, OWNERS, TOKEN


print("Initializing...")

activity = discord.Activity(type=discord.ActivityType.watching, name="you $stress out")

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=when_mentioned_or("$"),
    intents=intents,
    case_insensitive=True,
    help_command=None,
    when_mentioned=True,
    activity=activity,
    owner_ids=OWNERS
)
slash = discord_slash.SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send(f"Bot ready")


@bot.event
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
    desc = f"{ctx.message.content}\n{str(error)}"
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send(desc)


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"**Loaded {extension}**")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"**Unloaded {extension}**")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"**Reloaded {extension}**")


def start():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    keep_alive()

    # Run the bot with the token
    bot.run(TOKEN)


if __name__ == "__main__":
    start()
