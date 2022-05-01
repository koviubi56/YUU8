git"""
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
# pylint: disable=too-many-lines
from datetime import datetime
from os import environ
from re import I, findall
from secrets import token_hex
from time import time
from typing import Literal, Optional, Union

import aiohttp
import discord
from discord.ext import commands
import pickledb  # nosec  # noqa

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()

if __name__ == "__main__":
    print("Loading...")

intents = discord.Intents.default()
intents.members = True  # pylint: disable=assigning-non-slot

client = commands.Bot(
    command_prefix=".",
    description="A cool discord bot",
    owner_id=510548663496474660,
    intents=intents,
)

# ! Turn this OFF
DEBUG = True
db = pickledb.load("database.db", True)


if environ.get("KEEPALIVE", "0") == "1":
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from threading import Thread
        
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
        
    @app.get("/")
    def index():
        return 200
            
    Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000), daemon=True).start()

def reload_db() -> Literal[True]:
    """
    Reload the database.

    Returns:
        Literal[True]: Always True
    """
    return db.load("database.db", True)


class Color:
    """Colors."""

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


class URLs:
    """Some URLs."""

    # ! Don't forget to change these links if needed!
    # There are no unnecessary URLs here.
    class Issue:
        """URLs for issues."""

        # https://github.com/koviubi56/YUU8/issues/new?assignees=&labels=Type%3A+Bug&template=bug_report.md&title=
        BUG = "https://koviubi56-redirect.glitch.me/1.html"
        # https://github.com/koviubi56/YUU8/issues/new
        BLANK = "https://koviubi56-redirect.glitch.me/2.html"
        # https://github.com/koviubi56/YUU8/issues/new?assignees=&labels=Priority%3A+Medium&template=report-bad-user.md&title=
        HACKER = "https://koviubi56-redirect.glitch.me/3.html"

    class File:
        """URLs for files."""

        # https://github.com/koviubi56/YUU8/blob/main/CONTRIBUTORS
        CONTRIBUTORS = "https://koviubi56-redirect.glitch.me/4.html"


IFERROR = (
    f"If you think this is an error, report it at {URLs.Issue.BUG}"
)


def my_ember(
    desc: Optional[str] = None,
    title: Optional[str] = None,
    color: Optional[int] = Color.BLURPLE,
    footer: Optional[str] = None,
) -> discord.Embed:
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
        embed_ = discord.Embed(
            color=color,
            description=desc,
            timestamp=datetime.now(),
            title=title,
        )
    elif title:
        embed_ = discord.Embed(
            color=color, timestamp=datetime.now(), title=title
        )
    elif desc:
        embed_ = discord.Embed(
            color=color, description=desc, timestamp=datetime.now()
        )
    else:
        embed_ = discord.Embed(color=color, timestamp=datetime.now())
    if footer:
        embed_.set_footer(text=footer)
    return embed_


class MyParameter:
    """My Parameter."""

    def __init__(self, name) -> None:
        self.myname = name

    @property
    def name(self) -> str:
        """
        The name of the parameter.

        Returns:
            str: The name of the parameter
        """
        return str(self.myname)


def test_user(user: Union[discord.Member, discord.User]) -> bool:
    """
    Test if the user is banned.

    Args:
        user (Union[discord.Member, discord.User]): The user to test

    Raises:
        Exception: If BANNED_USERS is False (no/wrong database?)

    Returns:
        bool: True if the user *is banned*, False otherwise
    """
    reload_db()
    if db.get("BANNED_USERS") is False:
        raise Exception(
            f'db.get("BANNED_USERS") is {db.get("BANNED_USERS")}'
        )
    return user.id in db.get("BANNED_USERS")


@client.event
async def on_ready():
    """When the bot is ready."""
    print("Ready!")


@client.command()
async def ping(ctx: commands.Context):
    """
    [Command] Ping the bot.

    Args:
        ctx (commands.Context): The context
    """
    if test_user(ctx.author):
        return

    # embed
    embed_ = my_ember(desc="The response time", title="Ping")

    embed_.add_field(
        name="Ping by Discord",
        value=f"{client.latency:.2f} s/{client.latency * 1000:.2f} ms",
        inline=False,
    )

    reload_db()
    dbping = 0
    for _ in range(100):
        old = time()
        reload_db()
        db.getall()
        dbping += time() - old
    try:
        dbping /= 100
    except ZeroDivisionError:
        dbping = 0
    embed_.add_field(
        name="Database latency",
        value=f"{dbping / 1000:f}s/{dbping:f}ms",
        inline=False,
    )

    # send
    await ctx.send(embed=embed_)


@client.command()
async def unsplash(ctx: commands.Context, keyword: str):
    """
    [Command] Get an image from unsplash.

    Args:
        ctx (commands.Context): The context
        keyword (str): The keyword to search
    """
    if test_user(ctx.author):
        return
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://source.unsplash.com/featured/?{keyword}",
                timeout=10,
            ) as r:
                if r.ok:
                    await ctx.reply(r.url)
                else:
                    await ctx.reply(
                        f"**ERROR!** ({str(r.status_code)} | {hash(r.json())})"
                    )


@client.command()
async def embed(
    ctx: commands.Context,
    title: str,
    field_title: str,
    *field_value: str,
):
    """
    [Command] Create an embed. By the way this is not really recommended.

    Args:
        ctx (commands.Context): The context
        title (str): The embed's title
        field_title (str): The embed's field title
        *field_value (str): The embed's field value
    """
    if test_user(ctx.author):
        return
    embed_ = my_ember(title=title)

    embed_.add_field(
        name=field_title,
        value=" ".join(field_value)
        if isinstance(field_value, tuple)
        else field_value,
    )

    await ctx.reply(embed=embed_)


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_suggestion_channel(
    ctx: commands.Context, channel: discord.TextChannel
):
    """
    [Command] Set the suggestion channel.

    Args:
        ctx (commands.Context): The context
        channel (discord.TextChannel): The channel to set
    """
    if test_user(ctx.author):
        return
    # check is there a dict for server
    if db.get(ctx.guild.id) is False:
        db.set(str(ctx.guild.id), {})
    tmp = db.get(str(ctx.guild.id))
    # set channel
    tmp["suggestion_chn"] = channel.id
    db.set(str(ctx.guild.id), tmp)
    await ctx.reply(
        embed=my_ember(
            desc=f"Set suggestion channel to {str(channel)}!",
            color=Color.OKGREEN,
        )
    )


@client.command()
async def suggest(ctx: commands.Context, *suggestion: str):
    """
    [Command] Suggest something.

    Args:
        ctx (commands.Context): The context
        *suggestion (str): The suggestion
    """
    if test_user(ctx.author):
        return
    reload_db()
    if db.get(
        str(ctx.guild.id)
    ) is not False and "suggestion_chn" in db.get(str(ctx.guild.id)):
        chn = await client.fetch_channel(
            db.get(str(ctx.guild.id))["suggestion_chn"]
        )
        try:
            embed_ = my_ember(
                desc=suggestion
                if isinstance(suggestion, str)
                else " ".join(suggestion)
            )
        except Exception:
            embed_ = my_ember(
                desc=suggestion,
                footer="There was an error when we wanted to create this"
                " embed. Please report every bug at "
                + URLs.Issue.BUG,
            )

        msg = await chn.send(embed=embed_)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("⬇️")
    else:
        embed_ = my_ember(
            desc="There isn't a suggestion channel for this server.",
            color=Color.RED,
        )
        await ctx.reply(embed=embed_)


@client.command()
async def debug(ctx: commands.Context):
    """
    [Command] Debug the bot.

    Args:
        ctx (commands.Context): The context

    Raises:
        Exception: Debug exception
    """
    if test_user(ctx.author):
        return
    raise Exception(
        f"Debug exception was made by {str(ctx.author)} / {ctx.author.id}"
    )


@client.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(3, 10, commands.BucketType.user)
async def kick(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member, int],
    *reason: str,
):
    """
    [Command] Kick a user.

    Args:
        ctx (commands.Context): The context
        user (Union[discord.User, discord.Member, int]): The user to kick
        *reason (str): The reason

    Raises:
        MissingRequiredArgument: If reason is missing
    """
    if test_user(ctx.author):
        return
    if user == client.user:
        await ctx.reply(
            embed=my_ember(
                desc="After all my good work *this* is how you reward me?"
                " What a disgrace.",
                color=Color.ORANGE,
            )
        )
        return
    if not reason:
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    # //if isinstance(reason, tuple):
    # //    reason = " ".join(reason)
    if isinstance(user, int):
        user = await client.fetch_user(user)
    # await user.kick(reason=reason)
    await ctx.guild.kick(
        user=user,
        reason=" ".join(reason)
        if isinstance(reason, tuple)
        else reason,
    )
    reload_db()
    tmp = (
        db.get(str(ctx.guild.id))
        if db.get(str(ctx.guild.id)) is not False
        else {}
    )
    tmp[str(user.id)] = (
        db.get(str(ctx.guild.id))[str(user.id)]
        if tmp.get(str(user.id)) is not None
        else {}
    )
    tmp[str(user.id)]["punishments"] = (
        db.get(str(ctx.guild.id))[str(user.id)]["punishments"]
        if tmp.get(str(user.id)).get("punishments") is not None
        else []
    )
    tmp[str(user.id)]["punishments"].append(
        {
            "type": "kick",
            "moderator": ctx.author.id,
            "reason": " ".join(reason)
            if isinstance(reason, tuple)
            else reason,
            "time": datetime.now().timestamp(),
        }
    )
    db.set(str(ctx.guild.id), tmp)
    __user = tmp[str(user.id)]
    __punishments = __user["punishments"]
    __last_punishment = __punishments[
        len(tmp[str(user.id)]["punishments"]) - 1
    ]
    _reason = __last_punishment["reason"]
    await ctx.reply(
        embed=my_ember(
            desc=f"Kicked {user} for reason `{_reason}`!",
            color=Color.OKGREEN,
        )
    )


@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
@client.command(aliases=["clear"])
async def purge(ctx: commands.Context, max_: int):
    """
    [Command] Purge messages.

    Args:
        ctx (commands.Context): The context
        max_ (int): The max messages to delete
    """
    if test_user(ctx.author):
        return
    try:
        int(max_)
    except Exception:
        await ctx.reply(
            embed=my_ember(
                desc="Max must be an integer number.",
                color=Color.RED,
                footer=IFERROR,
            )
        )
        return
    reload_db()
    # 255 is a nice number. There isn't (or i don't know of) any type of API
    # limitation, that is 255. It's just a nice number.
    if int(max_) >= 255 and ctx.author.id not in db.get(
        "PURGE_LIMIT"
    ):
        await ctx.reply(
            embed=my_ember(
                desc=f"> Don't delete the whole channel\n- YUU8\n*(If you want"
                f" to delete a lot of messages, contact the developers"
                f" at {URLs.Issue.BLANK})*",
                color=Color.ORANGE,
                footer=f"Report hackers/bad people at {URLs.Issue.HACKER} and"
                f" they get banned from using this bot.",
            )
        )
        return
    tmp = await ctx.channel.purge(limit=int(max_) + 1)
    if int(max_) < 255:
        _color = Color.OKGREEN
    else:
        _color = Color.YELLOW

    if len(tmp) >= 255:
        _footer = (
            f"This user have been reached the purge limit!"
            f" Report hackers/bad people at {URLs.Issue.HACKER} and they"
            f" get banned from using this bot."
        )
    else:
        _footer = (
            "This message will be automaticly deleted after 5"
            " seconds."
        )

    await ctx.channel.send(
        embed=my_ember(
            desc=f"{str(len(tmp))} messages have been deleted",
            color=_color,
            footer=_footer,
        ),
        delete_after=5.0,
    )


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_report_channel(
    ctx: commands.Context, channel: discord.TextChannel
):
    """
    [Command] Set the report channel.

    Args:
        ctx (commands.Context): The context
        channel (discord.TextChannel): The channel to set
    """
    if test_user(ctx.author):
        return
    reload_db()
    # check is there a dict for server
    if db.get(ctx.guild.id) is False:
        db.set(str(ctx.guild.id), {})
    tmp = db.get(str(ctx.guild.id))
    # set channel
    tmp["report_chn"] = channel.id
    db.set(str(ctx.guild.id), tmp)
    await ctx.reply(
        embed=my_ember(
            desc=f"Set report channel to {str(channel)}!",
            color=Color.OKGREEN,
        )
    )


@client.command()
async def report(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member],
    *reason: str,
):
    """
    [Command] Report a user.

    Args:
        ctx (commands.Context): The context
        user (Union[discord.User, discord.Member]): The user to report
        *reason (str): The reason

    Raises:
        MissingRequiredArgument: If reason is missing
    """
    if test_user(ctx.author):
        return
    reload_db()
    if (
        db.get(str(ctx.guild.id)) is False
        or db.get(str(ctx.guild.id)).get("report_chn") is None
    ):
        await ctx.reply(
            embed=my_ember(
                desc="This server isn't have a report channel",
                color=Color.RED,
            )
        )
        return
    if not reason:
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    chn = await client.fetch_channel(
        db.get(str(ctx.guild.id))["report_chn"]
    )

    _reason = (
        (" ".join(reason)) if isinstance(reason, tuple) else (reason)
    )
    await chn.send(
        embed=my_ember(
            title="Report",
            desc=f"Report by: {ctx.author}\nReported user: {user}"
            f"\nReason: {_reason}",
        )
    )


@client.command()
async def slowmode(
    ctx: commands.Context, cooldown: Optional[int] = None
):
    """
    [Command] Manage the slowmode.

    Args:
        ctx (commands.Context): The context
        cooldown (Optional[int], optional): The cooldown. Defaults to None.
    """
    if test_user(ctx.author):
        return
    if cooldown is None:
        await ctx.reply(
            embed=my_ember(
                desc=f"Slowmode is {ctx.channel.slowmode_delay}. If you want"
                " to disable it, type `.slowmode 0`"
                if ctx.channel.slowmode_delay != 0
                else "Slowmode is disabled. To enable it, type `.slowmode"
                " <COOLDOWN>`"
            )
        )
        return
    if cooldown > 21600:
        await ctx.reply(
            embed=my_ember(
                desc="Cooldown must be between 0 and 21600",
                color=Color.RED,
            )
        )
        return
    await ctx.channel.edit(
        reason=f"{str(ctx.author)} set the slowmode to {cooldown}",
        slowmode_delay=max(cooldown, 0),
    )

    await ctx.reply(
        embed=my_ember(
            desc=f"Slowmode set to {cooldown}"
            if cooldown > 0
            else "Slowmode disabled",
            color=Color.OKGREEN,
        )
    )


@client.command()
@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def ban(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member, int],
    reason: str,
    delete_message_days: Optional[int] = None,
):
    """
    [Command] Ban a user.

    Args:
        ctx (commands.Context): The context
        user (Union[discord.User, discord.Member, int]): The user to ban
        reason (str): The reason
        delete_message_days (Optional[int], optional): Delete message days.\
 Defaults to None.

    Raises:
        MissingRequiredArgument: If reason is missing
        BadArgument: If delete_message_days is not in [1,7]
    """
    if test_user(ctx.author):
        return
    if user == client.user:
        await ctx.reply(
            embed=my_ember(
                desc="After all my good work *this* is how you reward me?"
                " What a disgrace.",
                color=Color.ORANGE,
            )
        )
        return
    if reason == ():
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    if isinstance(delete_message_days, int) and (
        delete_message_days < 1 or delete_message_days > 7
    ):
        raise commands.BadArgument(
            "delete_message_days must be between 1 and 7"
        )
    # //if isinstance(reason, tuple):
    # //    reason = " ".join(reason)
    if isinstance(user, int):
        user = await client.fetch_user(user)
    await ctx.guild.ban(
        user=user,
        reason=" ".join(reason)
        if isinstance(reason, tuple)
        else reason,
        delete_message_days=delete_message_days
        if delete_message_days is not None
        else 0,
    )
    reload_db()
    tmp = (
        db.get(str(ctx.guild.id))
        if db.get(str(ctx.guild.id)) is not False
        else {}
    )
    tmp[str(user.id)] = (
        db.get(str(ctx.guild.id))[str(user.id)]
        if tmp.get(str(user.id)) is not None
        else {}
    )
    tmp[str(user.id)]["punishments"] = (
        db.get(str(ctx.guild.id))[str(user.id)]["punishments"]
        if tmp.get(str(user.id)).get("punishments") is not None
        else []
    )
    tmp[str(user.id)]["punishments"].append(
        {
            "type": "ban",
            "moderator": ctx.author.id,
            "reason": " ".join(reason)
            if isinstance(reason, tuple)
            else reason,
            "delete_message_days": delete_message_days
            if delete_message_days is not None
            else 0,
            "time": datetime.now().timestamp(),
        }
    )
    db.set(str(ctx.guild.id), tmp)
    __last_punishment = tmp[str(user.id)]["punishments"][
        len(tmp[str(user.id)]["punishments"]) - 1
    ]
    _reason = __last_punishment["reason"]
    await ctx.reply(
        embed=my_ember(desc=f"Banned {user} for reason `{_reason}`!")
    )


@client.command()
@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def unban(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member, int],
    reason: str,
):
    """
    [Command] Unban a user.

    Args:
        ctx (commands.Context): The context
        user (Union[discord.User, discord.Member, int]): The user to unban
        reason (str): The reason

    Raises:
        MissingRequiredArgument: If reason is missing
    """
    if test_user(ctx.author):
        return
    if user == client.user:
        await ctx.reply(
            embed=my_ember(desc="I'm not banned", color=Color.ORANGE)
        )
        return
    if reason == ():
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    if isinstance(user, int):
        user = await client.fetch_user(user)
    await ctx.guild.unban(
        user=user,
        reason=" ".join(reason)
        if isinstance(reason, tuple)
        else reason,
    )
    _reason = (
        (" ".join(reason)) if isinstance(reason, tuple) else (reason)
    )
    await ctx.reply(
        embed=my_ember(
            desc=f"Unbanned {user} for reason `{_reason}`!",
            color=Color.OKGREEN,
        )
    )


@client.command()
@commands.has_permissions(
    ban_members=True, kick_members=True, manage_messages=True
)
async def regex(
    ctx: commands.Context,
    punishment: str,
    pattern: Optional[str] = None,
):
    """
    [Command] Add a regex filter.

    Args:
        ctx (commands.Context): The context
        punishment (str): The punishment
        pattern (Optional[str], optional): The regex pattern. Defaults to None.

    Raises:
        MissingRequiredArgument: If pattern is missing
    """
    if test_user(ctx.author):
        return
    if punishment not in ["del", "kick", "ban", "no"]:
        ctx.reply(
            'Punishment can be "del" to delete, "kick" to delete and kick,'
            ' "ban" to delete and ban, or "no" to delete the regex.'
        )
        return
    if punishment == "no":
        db.dadd(str(ctx.message.guild.id), ("regex", []))
        await ctx.reply(
            embed=my_ember(desc="Deleted regex!", color=Color.OKGREEN)
        )
        return
    if pattern is None:
        raise commands.MissingRequiredArgument(MyParameter("pattern"))
    db.dadd(str(ctx.message.guild.id), ("regex", [pattern, "del"]))
    _desc = (
        "If the regex `{}` matches anywhere, the message will be"
        " deleted{}.\nIf someone (including hackers, admins and mods) changes"
        ' the regex to "." or something else, then you can\'t turn off the'
        " regex. For this reasons, type this command: `.get_code`."
    )
    if punishment == "ban":
        _desc = _desc.format(
            pattern,
            ", and the user will be banned forever,"
            " for reason: `Regex matched`",
        )
    elif punishment == "kick":
        _desc = _desc.format(
            pattern,
            ", and the user will be kicked, for"
            " reason: `Regex matched`",
        )
    else:
        _desc = _desc.format(pattern, "")
    await ctx.reply(
        embed=my_ember(
            desc=_desc,
            color=Color.OKGREEN,
            title="Added regex!",
        )
    )


@client.command()
async def get_code(ctx: commands.Context):
    """
    [Command] Get the code for the regex.

    Args:
        ctx (commands.Context): The context
    """
    if ctx.author != ctx.guild.owner:
        await ctx.reply(
            embed=my_ember(
                "Just the owner of the server can use this command, "
                + str(ctx.guild.owner),
                color=Color.RED,
            )
        )
        return
    # yes, I know that this is unnecessary, but I want 101% security
    else:
        db.dadd(str(ctx.guild.id), ("code", token_hex(740)))
        dm = await ctx.guild.owner.create_dm()
        await dm.send(
            "This is the code for your server. This MUST be kept a secret! DO"
            " NOT share it even with your admins, mods!\n* Disable regex (in"
            " DM): `disable regex <SERVER ID> <CODE>` replace <SERVER ID> with"
            " the server's ID, <CODE> with the code.\n* Generate a new code"
            " (in DM): `new code <SERVER ID> <OLD CODE>` replace <SERVER ID>"
            " with your server's ID, <OLD CODE> with the (old) code.\n* Remove"
            " code (in DM): `remove code <SERVER ID> <CODE>` replace <SERVER"
            " ID> with your server's ID, <CODE> with the code.\n\nThis is the"
            f' code:\n```\n{db.dget(str(ctx.guild.id), "code")}\n```'
        )


async def on_dm(message: discord.Message):
    """
    On DM. (If message.guild is None)

    Args:
        message (discord.Message): The message
    """
    if message.content.startswith("disable regex"):
        tmp = message.content.split(" ")
        if (
            db.get(str(tmp[2])) is False
            or db.get(str(tmp[2])).get("code") is None
            or db.dget(str(tmp[2]), "code") != tmp[3]
        ):
            await message.reply("No.")
            return
        # yes, I know that this is unnecessary, but I want 101% security
        else:
            db.dadd(str(tmp[2]), ("regex", []))
            await message.reply(
                "Done!\n(Note: For 69420% security you may want to"
                " generate a new code.)"
            )
    if message.content.startswith("new code"):
        tmp = message.content.split(" ")
        if (
            db.get(str(tmp[2])) is False
            or db.get(str(tmp[2])).get("code") is None
            or db.dget(str(tmp[2]), "code") != tmp[3]
        ):
            await message.reply("No.")
            return
        # yes, I know that this is unnecessary, but I want 101% security
        else:
            db.dadd(str(tmp[2]), ("code", token_hex(740)))
            await message.reply(
                "This is the code for your server. This MUST be kept as"
                " a secret! DO NOT share it even with your admins, mods!\n"
                "* Disable regex (in DM): `disable regex <SERVER ID>"
                " <CODE>` replace <SERVER ID> with the server's ID, <CODE>"
                " with the code.\n* Generate a new code (in DM): `new code"
                " <OLD CODE>` replace <OLD CODE> with the (old) code.\n*"
                " Remove code (in DM): `remove code <CODE>` replace <CODE>"
                " with the code.\n\nThis is the code:"
                f'\n```\n{db.dget(str(tmp[2]), "code")}\n```'
            )
    if message.content.startswith("remove code"):
        tmp = message.content.split(" ")
        if (
            db.get(str(tmp[2])) is False
            or db.get(str(tmp[2])).get("code") is None
            or db.dget(str(tmp[2]), "code") != tmp[3]
        ):
            await message.reply("No.")
            return
        # yes, I know that this is unnecessary, but I want 101% security
        else:
            tmp2 = db.get(str(tmp[2]))
            del tmp2["code"]
            db.set(str(tmp[2]), tmp2)
            await message.reply(
                "This is the code for your server. This MUST be kept a"
                " secret! DO NOT share it even with your admins, mods!\n*"
                " Disable regex (in DM): `disable regex <SERVER ID>"
                " <CODE>` replace <SERVER ID> with the server's ID, <CODE>"
                " with the code.\n* Generate a new code (in DM): `new code"
                " <OLD CODE>` replace <OLD CODE> with the (old) code.\n*"
                " Remove code (in DM): `remove code <CODE>` replace <CODE>"
                " with the code.\n\nThis is the code:"
                f'\n```\n{db.dget(str(tmp[2]), "code")}\n```'
            )
    return


@client.event
async def on_message(message: discord.Message):
    """
    On message event.

    Args:
        message (_type_): The message
    """
    reload_db()
    if message.guild is None:
        await on_dm(message)
        return
    if (
        str(message.guild.id) in db.db
        and db.get(str(message.guild.id)).get("regex")
        and findall(
            db.get(str(message.guild.id))["regex"][0],
            message.content,
            I,
        )
    ):
        await message.delete()
        if db.get(str(message.guild.id))["regex"][1] == "kick":
            await message.guild.kick(
                message.author, reason="Matched regex."
            )
        elif db.get(str(message.guild.id))["regex"][1] == "ban":
            await message.guild.ban(
                message.author, reason="Matched regex."
            )

    await client.process_commands(message)


backslashn = "\n"


@client.event
async def on_command_error(
    ctx: commands.Context, error: commands.errors.CommandError
):
    """
    On command error

    Args:
        ctx (commands.Context): The context
        error (commands.errors.CommandError): The error.

    Raises:
        error: Reraise if the error is unknown/unexpected or DEBUG is True.\
 (It's a commands.errors.CommandError)
    """
    if test_user(ctx.author):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(
            embed=my_ember(
                desc="Sorry, but you don't have permissions for that.",
                color=Color.RED,
            )
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            embed=my_ember(
                desc=error.args[0].capitalize(),
                color=Color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.reply(
            embed=my_ember(
                desc=error.args[0],
                color=Color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
    elif (
        isinstance(error, discord.Forbidden) and error.code == 50013
    ) or error.args[0] == (
        "Command raised an exception: Forbidden: 403 Forbidden (error code:"
        " 50013): Missing Permissions"
    ):
        await ctx.reply(
            embed=my_ember(
                desc="I don't have permission to do that.",
                color=Color.RED,
            )
        )
    else:
        # Check for sensitive information
        tmp = next(
            (
                f"""Something went wrong!
For security reasons, we can't say more.
Please, open an issue here: {URLs.Issue.BUG}.
Include, that we can't say details for security reasons!"""
                for j in (
                    error.__class__.__name__,
                    error.__class__,
                    error.args,
                )
                if environ.get("BOT_TOKEN", None) in str(j)
            ),
            f"""Something went wrong!
Error: `{error.__class__.__name__}`
If you think that this is an error that we can fix, open an issue here:\
 {URLs.Issue.BUG} and include this:
```py
{error.__class__ = }
{error.__cause__ = }{backslashn + str(error.args) if DEBUG else ""}
```
If you help us, you will be in the CONTRIBUTORS file\
 ({URLs.File.CONTRIBUTORS})""",
        )

        # Send
        await ctx.reply(
            embed=my_ember(
                desc=tmp,
                color=Color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
        raise error
    if DEBUG:
        raise error


def main():
    """
    Main function.

    Raises:
        KeyError: If the BOT_TOKEN env var is not set.
    """
    try:
        client.run(environ["BOT_TOKEN"])
    except KeyError as e:
        print(
            f"\n[ERROR] Environment variable `{e.args[0]}` is not set."
        )
        raise


if __name__ == "__main__":
    main()
