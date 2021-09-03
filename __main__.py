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
import pytz
import discord
import discord_slash

from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or
from utils import myembeds
from utils.flask_thing import keep_alive
from utils.google_sheet_funcs import insert_row_sheet
from utils.misc import change_timeformat, is_user_authorized

from config import LOGGING_CHANNEL_ID, OWNERS, TOKEN, scheduler

from discord_slash.utils.manage_commands import create_option


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
    desc = f"```{ctx.message.content}\n{error}```"
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send(desc)


@bot.event
async def on_slash_command_error(ctx, error):
    desc = f"```error on /{ctx.name}\n{error}```"
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


@slash.slash(
        name="add",
        description="to add 'stuff' in StressMeOut",
        options=[
            create_option(
                name="name",
                description="name of the assignment/project",
                option_type=3,
                required=True
            ),
            create_option(
                name="date",
                description="date of deadline duh",
                option_type=4,
                required=True
            ),
            create_option(
                name="month",
                description="month of deadline duh",
                option_type=4,
                required=True
            ),
            create_option(
                name="hours",
                description="hour of deadline duh (24 hr format)",
                option_type=4,
                required=True
            ),
            create_option(
                name="minutes",
                description="minutes of deadline duh",
                option_type=4,
                required=True
            )
        ],
    )
async def add_stuff_in_bot(
    ctx,
    name: discord_slash.SlashContext,
    date: discord_slash.SlashContext,
    month: discord_slash.SlashContext,
    hours: discord_slash.SlashContext,
    minutes: discord_slash.SlashContext
):
    deadline = f"{date}.{month}.2021 {hours}:{minutes}"
    _name = f"{name}"
    if not is_user_authorized(ctx.author_id):
        await ctx.send("no prems 4 u")
        return
    if change_timeformat(deadline):
        await ctx.defer()
        insert_row_sheet(deadline, _name)
        try:
            scheduler.add_job(
                func=send_to_discord,
                trigger="cron",
                id=name,
                year=2021,
                month=month,
                day=date,
                # TODO: write correct logic for this
                hour=int(f"{hours}") - 1,
                minute=minutes,
                second=0,
                timezone=pytz.timezone("Asia/Kolkata"),
                kwargs={
                    "channel_id": 798458622836867094,
                    "assignment_name": _name,
                    # TODO: add support for this or something
                    # "role_id": func(stx.guild_id)
                }
            )
        except Exception as ex:
            await ctx.send("couldnt set reminder, error occured")
            # TODO: send to logging channel, make a function for logging
            print(ex)
            return
        await ctx.send("successful")
    else:
        await ctx.send("couldnt add, time format invalid")


async def send_to_discord(channel_id: int, assignment_name: str, role_id: int = None):
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title=assignment_name,
            description="Due in 1 Hour",
            colour=0xff0000
        )
        await channel.send("<&@{role_id}>", embed=embed)


def start():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    keep_alive()
    scheduler.start()
    bot.run(TOKEN)


if __name__ == "__main__":
    start()
