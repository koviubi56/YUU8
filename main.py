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
from typing import Optional, Union
from discord.ext import commands
from datetime import datetime
from time import time

try:
    from dotenv import load_dotenv
except ImportError:
    pass

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

# TODO: Turn this OFF
DEBUG = True


class mydb:

    def get() -> dict:
        """
        Get the database

        Returns:
            dict: The database
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
    BLACK = 0x000000

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


class urls:
    # TODO: Don't forget to change these links if needed!
    # There are no unnecessary URLs here.
    class issue:
        # https://github.com/koviubi56/YUU8/issues/new?assignees=&labels=Type%3A+Bug&template=bug_report.md&title=
        BUG = "https://yerl.org/If5za9uTZntiwQmVXdVugX"

    class file:
        # https://github.com/koviubi56/YUU8/blob/main/CONTRIBUTORS
        CONTRIBUTORS = "https://yerl.org/eRL8uhfAvPIB19CfxUOLlj"


def myEmbed(desc: Optional[str] = None, title: Optional[str] = None, color: Optional[int] = color.BLURPLE, footer: Optional[str] = None) -> discord.Embed:
    """
    **Don't forget to await! (Not this function)**
    Create an embed

    Args:
        desc (str, optional): The embed's description. Defaults to None.
        title (str, optional): The embed's title. Defaults to None.
        color (int, optional): The embed's color. Defaults to color.BLURPLE.
        footer (str, optional): The embed's footer. Defaults to None.

    Returns:
        discord.Embed: The embed
    """
    embed = discord.Embed(color=color, description=desc, timestamp=datetime.now(
    ), title=title) if title else discord.Embed(color=color, description=desc, timestamp=datetime.now())
    if footer:
        embed.set_footer(text=footer)
    return embed


class MyParameter:
    def __init__(self, name) -> None:
        self.myname = name

    @property
    def name(self) -> str:
        return str(self.myname)


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
async def embed(ctx: commands.Context, title: str, fieldTitle: str, *fieldValue: str):
    async with ctx.typing():
        embed = myEmbed(title=title)

        embed.add_field(name=fieldTitle, value=" ".join(
            fieldValue) if isinstance(fieldValue, tuple) else fieldValue)

    await ctx.reply(embed=embed)
    return


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_suggestion_channel(ctx: commands.Context,
                                 channel: discord.TextChannel):
    # * Checks MUST be OUTSIDE of "async with ctx.typing()"
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
        tmp = myEmbed(
            desc=f"Set suggestion channel to {str(channel)}!", color=color.OKGREEN)
    await ctx.reply(embed=tmp)
    return


@client.command()
async def suggest(ctx: commands.Context,
                  *suggestion: str):
    # * Checks MUST be OUTSIDE of "async with ctx.typing()"
    async with ctx.typing():
        if ctx.guild.id in mydb.get() and "suggestion_chn" in mydb.get()[ctx.guild.id]:
            chn = await client.fetch_channel(
                mydb.get()[ctx.guild.id]["suggestion_chn"])
            try:
                embed = myEmbed(desc=suggestion if isinstance(
                    suggestion, str) else " ".join(suggestion))
            except Exception:
                embed = myEmbed(
                    desc=suggestion, footer="There was an error when we wanted to create this embed. Please report every bug at {}".format(
                        urls.issue.BUG
                    ))

            msg = await chn.send(embed=embed)
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")
            return
        else:
            embed = myEmbed(desc="There isn't a suggestion channel for this server.",
                            color=color.RED)
            await ctx.reply(embed=embed)
            return


@client.command()
async def debug(ctx: commands.Context):
    raise Exception(
        f"Debug exception was made by {str(ctx.author)} / {ctx.author.id}")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, user: Union[discord.User, int], *reason: str):
    try:
        if user == client.user:
            await ctx.reply(embed=myEmbed(
                desc="After all my good work *this* is how you reward me? What a disgrace.", color=color.ORANGE))
            return
        if reason == ():
            raise commands.MissingRequiredArgument(MyParameter("reason"))
        if isinstance(reason, (tuple, list, set)):
            reason = " ".join(reason)
        if isinstance(user, int):
            user = await client.fetch_user(user)
        await user.kick(reason=reason)
    except Exception:
        raise
    else:
        tmp = mydb.get()
        if tmp.get(user.id) is None:
            tmp[user.id] = {}
        if tmp[user.id].get("punishments") is None:
            tmp[user.id]["punishments"] = []
        tmp[user.id]["punishments"].append({
            "type": "kick",
            "moderator": ctx.author.id,
            "reason": " ".join(reason) if isinstance(reason, tuple) else reason,
            "time": datetime.now().timestamp()
        })
        mydb.set()
        await ctx.reply(embed=myEmbed(
            desc=f"Kicked {str(user)} for reason `{reason}`!", color=color.OKGREEN))

backslashn = "\n"


@client.event
async def on_command_error(ctx: commands.Context, error: commands.errors.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(embed=myEmbed(desc="Sorry, but you don't have permissions for that.", color=color.RED))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(embed=myEmbed(desc=error.args[0].capitalize(), color=color.RED))
    else:
        # Check for sensitive information
        for j in (error.__class__.__name__, error.__class__, error.args):
            if str(j).find(getenv("BOT_TOKEN")) != -1:
                # Set text
                tmp = f"""Something went wrong!
For security reasons, we can't say more.
Please, open an issue here: {urls.issue.BUG}.
Include, that we can't say details for security reasons!"""
                break
        else:
            # Set text
            tmp = f"""Something went wrong!
Error: `{error.__class__.__name__}`
If you think that this is an error that we can fix, open an issue here: {urls.issue.BUG} and include this:
```py
{error.__class__ = }
{error.__cause__ = }{backslashn + str(error.args) if DEBUG else ""}
```
If you help us, you will be in the CONTRIBUTORS file ({urls.file.CONTRIBUTORS})"""
        # Send
        await ctx.reply(embed=myEmbed(desc=tmp, color=color.RED, footer="Please, do not abuse with these informations!"))
        if DEBUG:
            raise error.__cause__


def main():
    client.run(getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
