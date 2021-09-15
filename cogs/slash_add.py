"""MIT License

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

import main
import discord
import pytz

from config import scheduler

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils.google_sheet_funcs import insert_row_sheet
from utils.misc import change_timeformat, is_user_authorized
from discord_slash.utils.manage_commands import create_option


async def send_to_discord(channel_id: int, assignment_name: str, role_id: int = None):
    channel = main.bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title=assignment_name,
            description="Due in 1 Hour",
            colour=0xff0000
        )
        await channel.send(f"<&@{role_id}>", embed=embed)


class AddStuffSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
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
            self,
            ctx,
            name: SlashContext,
            date: SlashContext,
            month: SlashContext,
            hours: SlashContext,
            minutes: SlashContext
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


def setup(bot):
    bot.add_cog(AddStuffSlash(bot))
