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
import pickledb

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
db = pickledb.load('database.db', True)


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
        # https://github.com/koviubi56/YUU8/issues/new
        BLANK = "https://yerl.org/9TwySiyYmZoSCHsiXYb90t"
        # https://github.com/koviubi56/YUU8/issues/new?assignees=&labels=Priority%3A+Medium&template=report-bad-user.md&title=
        HACKER = "https://yerl.org/eCPRDRalWRL5e8mqn8bRKD"

    class file:
        # https://github.com/koviubi56/YUU8/blob/main/CONTRIBUTORS
        CONTRIBUTORS = "https://yerl.org/eRL8uhfAvPIB19CfxUOLlj"


IFERROR = f"If you think this is an error, report it at {urls.issue.BUG}"


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
    if title and desc:
        embed = discord.Embed(color=color, description=desc,
                              timestamp=datetime.now(), title=title)
    elif title and not desc:
        embed = discord.Embed(
            color=color, timestamp=datetime.now(), title=title)
    elif not title and desc:
        embed = discord.Embed(color=color, description=desc,
                              timestamp=datetime.now())
    elif not title and not desc:
        embed = discord.Embed(color=color, timestamp=datetime.now())
    if footer:
        embed.set_footer(text=footer)
    return embed


class MyParameter:
    def __init__(self, name) -> None:
        self.myname = name

    @property
    def name(self) -> str:
        return str(self.myname)


def testUser(user: discord.User) -> bool:
    if db.get("BANNED_USERS") is False:
        raise Exception('db.get("BANNED_USERS") is {}'.format(
            db.get("BANNED_USERS")))
    return user.id in db.get("BANNED_USERS")


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

    if testUser(ctx.author):
        return

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
        db.getall()
        dbping += time() - old
    try:
        dbping = dbping / 100
    except ZeroDivisionError:
        dbping = 0
    embed.add_field(name="Database latency",
                    value=f"{dbping / 1000:f}s/{dbping:f}ms",
                    inline=False)

    # send
    await ctx.send(embed=embed)


@client.command()
async def unsplash(ctx: commands.Context, keyword: str):
    if testUser(ctx.author):
        return
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://source.unsplash.com/featured/?{keyword}',
                                   timeout=10) as r:
                if r.ok:
                    await ctx.reply(r.url)
                else:
                    await ctx.reply(f"**ERROR!** ({str(r.status_code)} | {str(hash(r.json()))})")


@client.command()
async def embed(ctx: commands.Context, title: str, fieldTitle: str, *fieldValue: str):
    if testUser(ctx.author):
        return
    embed = myEmbed(title=title)

    embed.add_field(name=fieldTitle, value=" ".join(
        fieldValue) if isinstance(fieldValue, tuple) else fieldValue)

    await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_suggestion_channel(ctx: commands.Context,
                                 channel: discord.TextChannel):
    if testUser(ctx.author):
        return
    # check is there a dict for server
    if db.get(ctx.guild.id) is False:
        db.set(str(ctx.guild.id), {})
    tmp = db.get(str(ctx.guild.id))
    # set channel
    tmp["suggestion_chn"] = channel.id
    db.set(str(ctx.guild.id), tmp)
    await ctx.reply(embed=myEmbed(desc=f"Set suggestion channel to {str(channel)}!", color=color.OKGREEN))


@client.command()
async def suggest(ctx: commands.Context,
                  *suggestion: str):
    if testUser(ctx.author):
        return
    if db.get(str(ctx.guild.id)) is not False and "suggestion_chn" in db.get(str(ctx.guild.id)):
        chn = await client.fetch_channel(
            db.get(str(ctx.guild.id))["suggestion_chn"])
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
    else:
        embed = myEmbed(desc="There isn't a suggestion channel for this server.",
                        color=color.RED)
        await ctx.reply(embed=embed)


@client.command()
async def debug(ctx: commands.Context):
    if testUser(ctx.author):
        return
    raise Exception(
        f"Debug exception was made by {str(ctx.author)} / {ctx.author.id}")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, user: Union[discord.User, int], *reason: str):
    if testUser(ctx.author):
        return
    try:
        if user == client.user:
            await ctx.reply(embed=myEmbed(
                desc="After all my good work *this* is how you reward me? What a disgrace.",
                color=color.ORANGE))
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
        tmp = db.get(str(user.id)) if db.get(
            str(user.id)) is not False else {}
        if tmp.get("punishments") is None:
            tmp["punishments"] = []
        tmp["punishments"].append({
            "type": "kick",
            "moderator": ctx.author.id,
            "reason": " ".join(reason) if isinstance(reason, tuple) else reason,
            "time": datetime.now().timestamp()
        })
        db.set(str(user.id), tmp)
        await ctx.reply(embed=myEmbed(
            desc="Kicked {} for reason `{}`!".format(
                str(user),
                tmp["punishments"][len(tmp["punishments"]) - 1]["reason"]
            ), color=color.OKGREEN))


@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
@client.command()
async def purge(ctx: commands.Context, max: int):
    if testUser(ctx.author):
        return
    try:
        int(max)
    except Exception:
        await ctx.reply(embed=myEmbed(desc="Max must be an integer number.", color=color.RED, footer=IFERROR))
        return
    # 255 is a nice number. There isn't (or i don't know of) any type of API limitation, that is 255. It's just a nice number.
    if int(max) >= 255 and ctx.author.id not in db.get("PURGE_LIMIT"):
        await ctx.reply(embed=myEmbed(desc=f"> Don't delete the whole channel\n- YUU8\n*(If you want to delete a lot of messages, contact the developers at {urls.issue.BLANK})*", color=color.ORANGE, footer=f"Report hackers/bad people at {urls.issue.HACKER} and they get banned from using this bot."))
        return
    tmp = await ctx.channel.purge(limit=int(max) + 1)
    # *                                                                  This is important because if the user WANTS to delete lots of messages, then it should be yellow
    # *                                                                                                             VVVVVVVV
    await ctx.channel.send(embed=myEmbed(desc=f"{str(len(tmp))} messages have been deleted", color=color.OKGREEN if int(max) < 255 else color.YELLOW, footer=f"This user have been reached the purge limit! Report hackers/bad people at {urls.issue.HACKER} and they get banned from using this bot." if len(tmp) >= 255 else "This message will be automaticly deleted after 5 seconds."), delete_after=5.0)


@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
@client.command()
async def clear(ctx: commands.Context, *args, **kwargs):
    if testUser(ctx.author):
        return
    try:
        await purge(ctx, *args, **kwargs)
    except Exception:
        await ctx.reply(embed=myEmbed(desc="Something went wrong.\nDo you passed the max parameter? Is it an integer number that is bigger than zero?\n`.clear <MAX>`", color=color.RED, footer=IFERROR))


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_report_channel(ctx: commands.Context,
                             channel: discord.TextChannel):
    if testUser(ctx.author):
        return
    # check is there a dict for server
    if db.get(ctx.guild.id) is False:
        db.set(str(ctx.guild.id), {})
    tmp = db.get(str(ctx.guild.id))
    # set channel
    tmp["report_chn"] = channel.id
    db.set(str(ctx.guild.id), tmp)
    await ctx.reply(embed=myEmbed(desc=f"Set report channel to {str(channel)}!", color=color.OKGREEN))


@client.command()
async def report(ctx: commands.Context, user: discord.User, *reason):
    if testUser(ctx.author):
        return
    if db.get(str(ctx.guild.id)) is False or db.get(str(ctx.guild.id)).get("report_chn") is None:
        await ctx.reply(embed=myEmbed(desc="This server isn't have a report channel", color=color.RED))
        return
    if reason is None or reason == "" or reason == " " or reason == ():
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    chn = await client.fetch_channel(
        db.get(str(ctx.guild.id))["report_chn"])

    await chn.send(embed=myEmbed(title="Report", desc="Report by: {report_by}\nReported user: {reported_user}\nReason: {reason}".format(
        report_by=str(ctx.author),
        reported_user=str(user),
        reason=" ".join(reason) if isinstance(
            reason, tuple) else reason
    )))

backslashn = "\n"


@client.event
async def on_command_error(ctx: commands.Context, error: commands.errors.CommandError):
    if testUser(ctx.author):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(embed=myEmbed(desc="Sorry, but you don't have permissions for that.", color=color.RED))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(embed=myEmbed(desc=error.args[0].capitalize(), color=color.RED, footer="Please, do not abuse with these informations!"))
    elif isinstance(error, commands.BadArgument):
        await ctx.reply(embed=myEmbed(desc=error.args[0], color=color.RED, footer="Please, do not abuse with these informations!"))
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
        raise error.__cause__
    if DEBUG:
        raise error.__cause__


def main():
    client.run(getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
