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

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, spread_to_rows, ComponentContext

from utils.myembeds import e_stress
from utils.misc import is_user_authorized, ordinal
from utils.google_sheet_funcs import delete_row_sheet


class DeleteStuffSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="Delete",
        description="to delete 'stuff' from bot"
    )
    async def delete_stuff_from_bot(self, ctx):
        if not is_user_authorized(ctx.author_id):
            await ctx.send("no prems 4 u")
            return

        something = e_stress(-1)

        buttons = [
            create_button(style=ButtonStyle.red, label=ordinal(x), custom_id=f"{x}") for x in range(1, something[1] + 1)
        ]
        rows = spread_to_rows(*buttons)
        await ctx.send("select the option which you want to delete", embed=something[0], components=rows)

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        if not is_user_authorized(ctx.author_id):
            await ctx.send("no prems 4 u nab", hidden=True)
        await ctx.edit_origin(
            content=f"succesfully deleted {ordinal(int(ctx.custom_id))} thing\n\tby- {ctx.author}",
            components=None,
            embed=None
        )
        delete_row_sheet(int(ctx.custom_id))


def setup(bot):
    bot.add_cog(DeleteStuffSlash(bot))
