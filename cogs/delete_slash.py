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
from my_utils import is_user_authorized
from myembeds import e_stress
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle



class DeleteStuffSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="Delete",
        description="to delete 'stuff' from bot"
    )
    async def delete_stuff_from_bot(self, ctx):
        if not is_user_authorized(ctx.author_id):
            await ctx.send("no prems 4 u")
            return

        buttons = [
            create_button(
                style=ButtonStyle.green,
                label="A Green Button"
            )
        ]
        action_row = create_actionrow(*buttons)
        await ctx.send(embed=e_stress(-1), components=[action_row])
        button_ctx = await wait_for_component(self.client, components=action_row)
        await button_ctx.edit_origin(content="You pressed a button!")


def setup(client):
    client.add_cog(DeleteStuffSlash(client))
