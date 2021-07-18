"""
Copyright (C) 2021  Koviubi56

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
import aiohttp

from os import getenv
from typing import Any
from discord.ext import commands
from datetime import datetime
from time import time
try:
    from dotenv import load_dotenv
except ImportError:
    pass

# /# ! \s+ V+/

if __name__ == "__main__":
    print("Loading...")

try:
    load_dotenv()
except Exception:
    pass

client = commands.Bot(
    command_prefix=".",
    description="A cool discord bot",
    owner_id=510548663496474660
)


class mydb:

    def get() -> Any:
        """
        Get something or everything from the database

        Returns:
            Any: What you want
        """
        import db
        del db
        import db

        tmp = db.db
        while not isinstance(tmp, dict):
            tmp = tmp.db
        return tmp

    def set(what: dict) -> None:
        """
        Set the whole databse

        Args:
            what (dict): What to set it to
        """
        with open("db.py", "w") as f:
            f.write("db = " + str(what))


assert isinstance(
    mydb.get(), dict), f"db.get() returned {type(mydb.get())}, and not dict"


class color:
    WHITE = 0xFFFFFF
    BLACH = 0x000000

    RED = 0xFF0000
    DISCORDRED = 0xED4245

    ORANGE = 0xFF8000

    YELLOW = 0xFFFF00
    DISCORDYELLOW = 0xFEE75C

    GREEN = 0x00FF00
    OKGREEN = 0x00B600
    DISCORDGREEN = 0x57F287

    CYAN = 0x00FFFF

    BLUE = 0x0000FF
    BLURPLE = 0x7289DA

    PURPLE = 0x7D00FF

    ROSE = 0xFF0080
    FUCHSIA = 0xFF00FF
    DISCORDFUCHSIA = 0xEB459E


def myEmbed(desc=None, title=None, color=color.BLURPLE):
    if title:
        return discord.Embed(color=color, description=desc,
                             timestamp=datetime.now(), title=title)
    return discord.Embed(color=color, description=desc,
                         timestamp=datetime.now())


@client.event
async def on_ready():
    print("Ready!")


@client.command()
async def ping(ctx: commands.Context):
    """
    # receiving time
    receive = datetime.now()

    # ping by us
    pingbyus = float(receive.timestamp()) - \
        float(ctx.message.created_at.timestamp())
    """

    async with ctx.typing():

        # embed
        embed = myEmbed(
            desc="The response time",
            title="Ping"
        )

        embed.add_field(name="Ping by Discord",
                        value=f"{client.latency:.2f} s/{client.latency * 1000:.2f} ms",
                        inline=False)

        dbping = 0
        for _ in range(100):
            old = time()
            dbping += time() - old
        try:
            dbping = dbping / 100_000
        except ZeroDivisionError:
            dbping = 0
        embed.add_field(name="Database latency",
                        value=f"{dbping / 1000}s/{dbping}ms",
                        inline=False)

    # send
    await ctx.send(embed=embed)
    return


@client.command()
async def unsplash(ctx: commands.Context, keyword: str):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://source.unsplash.com/featured/?{keyword}',
                                   timeout=10) as r:
                if r.ok:
                    await ctx.reply(r.url)
                    return
                else:
                    await ctx.reply(f"**ERROR!** ({str(r.status_code)} | {str(hash(r.json()))})")
                    return


@client.command()
async def embed(ctx: commands.Context, title: str, fieldTitle: str, fieldValue: str):
    async with ctx.typing():
        embed = myEmbed(title=title)

        embed.add_field(name=fieldTitle, value=fieldValue)

    await ctx.reply(embed=embed)
    return


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_suggestion_channel(ctx: commands.Context,
                                 channel: discord.TextChannel = None):
    # * Checks MUST be OUTSIDE of "async with ctx.typing()"
    if channel is None:
        # !                                            VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        embed = myEmbed(
            desc="What to be the suggestion channel?\n`.set_suggestion_channel <CHANNEL>`")
        await ctx.reply(embed=embed)
        return
    async with ctx.typing():
        tmp = {}
        # Get DB
        tmp = mydb.get()
        # check is there a dict for server
        if tmp.get(ctx.guild.id) is None:
            tmp[ctx.guild.id] = {}
        # set channel
        tmp[ctx.guild.id]["suggestion_chn"] = channel.id
        mydb.set(tmp)
        tmp = myEmbed(desc="Done!", color=color.OKGREEN)
    await ctx.reply(embed=tmp)
    return


@client.command()
async def suggest(ctx: commands.Context,
                  *suggestion: str):
    # * Checks MUST be OUTSIDE of "async with ctx.typing()"
    if suggestion is None or suggestion == "" or suggestion == () or len(suggestion) <= 0:
        # !                                       VVVVVVVVVVVVVVVVVVVVV
        embed = myEmbed(
            desc="What are you want to suggest?\n`.suggest <SUGGESTION>`", color=color.RED)
        await ctx.reply(embed=embed)
        return
    async with ctx.typing():
        if ctx.guild.id in mydb.get() and "suggestion_chn" in mydb.get()[ctx.guild.id]:
            chn = await client.fetch_channel(
                mydb.get()[ctx.guild.id]["suggestion_chn"])
            try:
                embed = myEmbed(desc=suggestion if isinstance(
                    suggestion, str) else " ".join(suggestion))
            except Exception:
                embed = myEmbed(desc=suggestion)
                embed.set_footer(
                    text="There was an error when we wanted to create this embed.")

            msg = await chn.send(embed=embed)
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")
            return
        else:
            embed = myEmbed(desc="There isn't a suggestion channel for this server.",
                            color=color.RED)
            await ctx.reply(embed=embed)
            return


def main():
    client.run(getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
