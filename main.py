"""
Copyright (C) 2022  Koviubi56

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# pylint: disable=too-many-lines
import asyncio
import contextlib
import enum
import functools
import re
import shutil
import traceback
from datetime import datetime
from os import getcwd  # pylint: disable=no-name-in-module
from os import chdir, environ, getenv
from pathlib import Path
from secrets import SystemRandom, choice
from time import time
from traceback import print_exc
from typing import Callable, List, Literal, Optional, Set, TypeVar, Union

import aiohttp
import discord
import pickledb  # nosec  # noqa
import youtube_dl
from discord.ext import commands
from imageio_ffmpeg import get_ffmpeg_exe

import statuspage

with contextlib.suppress(ImportError):
    from dotenv import load_dotenv

    load_dotenv()

if __name__ == "__main__":
    print("Loading...")

# ! Turn this OFF
DEBUG = True

intents = discord.Intents.default()
intents.members = True  # pylint: disable=assigning-non-slot
intents.message_content = True
client = commands.Bot(
    command_prefix=".",
    description="A cool discord bot",
    owner_id=510548663496474660,
    intents=intents,
)
db = pickledb.load(Path("database.db").resolve().__fspath__(), True)
YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": not DEBUG,
    "no_warnings": not DEBUG,
    "verbose": DEBUG,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    # bind to ipv4 since ipv6 addresses cause issues sometimes
}
FFMPEG_OPTIONS = {"options": "-vn"}
try:
    _f = get_ffmpeg_exe()
except RuntimeError:
    _f = r"ffmpeg.exe"
EXES: Set[str] = {"ffmpeg", _f, "ffmpeg.exe"}
youtube_dl.utils.bug_reports_message = lambda: ""
YTDL = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)
CRASH_MESSAGE = (
    "Who set us up the TNT?",
    "Everything's going to plan. No, really, that was supposed to happen.",
    "Uh... Did I do that?",
    "Oops.",
    "Why did you do that?",
    "I feel sad now :(",
    "My bad.",
    "I'm sorry, Dave.",
    "I let you down. Sorry :(",
    "On the bright side, I bought you a teddy bear!",
    "Daisy, daisy...",
    "Oh - I know what I did wrong!",
    "Hey, that tickles! Hehehe!",
    "Don't be sad. I'll do better next time, I promise!",
    "Don't be sad, have a hug! <3",
    "I just don't know what went wrong :(",
    "Shall we play a game?",
    "Quite honestly, I wouldn't worry myself about that.",
    "I bet Cylons wouldn't have this problem.",
    "Sorry :(",
    "Surprise! Haha. Well, this is awkward.",
    "Would you like a cupcake?",
    "Hi. I'm YUU8, and I'm a crashaholic.",
    "Ooh. Shiny.",
    "This doesn't make any sense!",
    "Why is it breaking :(",
    "Don't do that.",
    "Ouch. That hurt :(",
    "You're mean.",
    "This is a token for 1 free hug: [~~HUG~~]",
    "There are four lights!",
    "But it works on my machine.",
)
NEW_LINE = "\n"
R = TypeVar("R")

del _f

if environ.get("KEEPALIVE", "0") == "1":
    from threading import Thread

    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

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

    Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000),
        daemon=True,
    ).start()


@contextlib.contextmanager
def change_working_directory(path):
    _old = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(_old)


def reload_db() -> Literal[True]:
    """
    Reload the database.

    Returns:
        Literal[True]: Always True
    """
    return db.load("database.db", True)


class Color(enum.IntEnum):
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


IFERROR = f"If you think this is an error, report it at {URLs.Issue.BUG}"


def my_embed(
    desc: Optional[str] = None,
    title: Optional[str] = None,
    color: Optional[int] = Color.BLURPLE,
    footer: Optional[str] = None,
) -> discord.Embed:
    """
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
    text = statuspage.get_text()
    if text:
        embed_.add_field(name=text[0], value=text[1])
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
        raise RuntimeError(
            f'db.get("BANNED_USERS") is {db.get("BANNED_USERS")}'
        )
    return user.id in db.get("BANNED_USERS")


@client.event
async def on_ready():
    """When the bot is ready."""
    await client.tree.sync()
    print("Ready!")


def slash_command(func: Callable[..., R]) -> discord.app_commands.Command:
    @functools.wraps(func)
    async def wrapper(interaction: discord.Interaction, *args, **kwargs) -> R:
        try:
            if test_user(interaction.user):
                return
            return await func(interaction, *args, **kwargs)
        except Exception:
            report = gen_crash_report(
                f"{func!r} ({func.__module__}.{func.__qualname__})",
                f"Interaction: {interaction!r}\nArgs: {args!r}\nKwargs:"
                f" {kwargs!r}",
            )
            if getenv("BOT_TOKEN") in report:
                report = "<Not shown since it contains token>"
            try:
                embed_ = my_embed(
                    title="Error. Something went wrong.",
                    desc=f"We tried everything, but we're not perfect. Please"
                    f" report it here: {URLs.Issue.BUG} with the following"
                    f" information:\n```py\n{report}\n```",
                    color=Color.RED,
                    footer="Please report it.",
                )
            except Exception:
                message = (
                    "**Error. Something went wrong.**\nWe tried everything,"
                    " but we're not perfect. Please report it here:"
                    f" {URLs.Issue.BUG} with the following information:"
                    f"\n```py\n{report}\n```",
                )
                try:
                    await interaction.response.send_message(message)
                except (
                    discord.errors.NotFound,
                    discord.errors.InteractionResponded,
                ):
                    await interaction.channel.send(message)
            else:
                try:
                    await interaction.response.send_message(embed=embed_)
                except (
                    discord.errors.NotFound,
                    discord.errors.InteractionResponded,
                ):
                    await interaction.channel.send(embed=embed_)

    return client.tree.command()(wrapper)


@slash_command
async def ping(interaction: discord.Interaction):
    """[Command] Ping the bot."""
    # embed
    embed_ = my_embed(desc="The response time", title="Ping")

    try:
        embed_.add_field(
            name="Ping by Discord",
            value=f"{client.latency:.2f} s/{client.latency * 1000:.2f} ms",
            inline=False,
        )
    except Exception:
        print_exc()
        embed_.add_field(
            name="Ping by Discord",
            value="Error",
            inline=False,
        )

    try:
        reload_db()
        dbping = 0.0
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
    except Exception:
        print_exc()
        embed_.add_field(
            name="Database latency",
            value="Error",
            inline=False,
        )

    # send
    await interaction.response.send_message(embed=embed_)


@slash_command
@discord.app_commands.describe(keyword="THe keyword to search for")
async def unsplash(interaction: discord.Interaction, keyword: str):
    """
    [Command] Get an image from unsplash.

    Args:
        keyword (str): The keyword to search
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://source.unsplash.com/featured/?{keyword}"
        # // print(url)
        async with session.get(
            url,
            timeout=10,
            verify_ssl=False,
        ) as r:
            if r.ok:
                await interaction.response.send_message(r.url)
            else:
                print(r.json())
                await interaction.response.send_message(
                    embed=my_embed(
                        desc=f"**ERROR!** ({str(r.status)} |"
                        f" {hash(r.json())})",
                        color=Color.RED,
                        footer=f"Please report this to {URLs.Issue.BUG}",
                    )
                )


@slash_command
@discord.app_commands.describe(
    desc="[OPTIONAL] The body of the embed; its description.",
    title="[OPTIONAL] The title of the embed",
    color="[OPTIONAL] The color of the embed. Must be one of:"
    f" {', '.join(map(lambda co: co.name, Color))}",
    field1_title="[OPTIONAL] The title of the 1st field. Required if"
    " field1_value is passed.",
    field1_value="[OPTIONAL] The value of the 1st field. Required if"
    " field1_title is passed.",
    field2_title="[OPTIONAL] The title of the 2nd field. Required if"
    " field2_value is passed. The 1st field must be provided to have a 2nd"
    " field.",
    field2_value="[OPTIONAL] The value of the 2nd field. Required if"
    " field2_title is passed. The 1st field must be provided to have a 2nd"
    " field.",
    field3_title="[OPTIONAL] The title of the 3rd field. Required if"
    " field3_value is passed. The 1st and 2nd fields must be provided to have"
    " a 3rd field.",
    field3_value="[OPTIONAL] The value of the 3rd field. Required if"
    " field3_title is passed. The 1st and 2nd fields must be provided to have"
    " a 3rd field.",
)
async def embed(
    interaction: discord.Interaction,
    desc: Optional[str] = None,
    title: Optional[str] = None,
    color: str = "BLURPLE",
    field1_title: Optional[str] = None,
    field1_value: Optional[str] = None,
    field2_title: Optional[str] = None,
    field2_value: Optional[str] = None,
    field3_title: Optional[str] = None,
    field3_value: Optional[str] = None,
):  # sourcery skip: remove-redundant-if
    """
    [Command] Create an embed.

    Args:
        desc: [OPTIONAL] The body of the embed; its description.
        title: [OPTIONAL] The title of the embed
        color: [OPTIONAL] The color of the embed.
        field1_title: [OPTIONAL] The title of the 1st field. Required if\
 field1_value is passed.
        field1_value: [OPTIONAL] The value of the 1st field. Required if\
 field1_title is passed.
        field2_title: [OPTIONAL] The title of the 2nd field. Required if\
 field2_value is passed. The 1st field must be provided to have a 2nd field.
        field2_value: [OPTIONAL] The value of the 2nd field. Required if\
 field2_title is passed. The 1st field must be provided to have a 2nd field.
        field3_title: [OPTIONAL] The title of the 3rd field. Required if\
 field3_value is passed. The 1st and 2nd fields must be provided to have a 3rd\
 field.
        field3_value: [OPTIONAL] The value of the 3rd field. Required if\
 field3_title is passed. The 1st and 2nd fields must be provided to have a 3rd\
 field.
    """
    try:
        color_ = getattr(Color, color)
    except Exception:
        await interaction.response.send_message(
            embed=my_embed(
                f'Well idk what "{color}"'
                " is. Please choose from"
                f" {', '.join(map(lambda co: co.name, Color))}",
                color=Color.RED,
                footer=IFERROR,
            ),
            ephemeral=True,
        )
        return
    got_text = statuspage.get_text()
    embed_ = my_embed(
        desc=desc,
        title=title,
        color=color_,
        footer="Not official message by YUU8; user-generated by"
        f" {interaction.user}"
        if not got_text
        else f"User-generated EXCEPT THE WARNING ({got_text[0]}), which is AN"
        " OFFICIAL YUU8 WARNING",
    )
    # field1
    if (field1_title and (not field1_value)) or (
        (not field1_title) and field1_value
    ):
        await interaction.response.send_message(
            "Have title AND value for field 1.",
            ephemeral=True,
        )
        return
    if field1_title and field1_value:
        embed_.add_field(name=field1_title, value=field1_value, inline=False)
    # field2
    if (field2_title and (not field2_value)) or (
        (not field2_title) and field2_value
    ):
        await interaction.response.send_message(
            "Have title AND value for field 2.",
            ephemeral=True,
        )
        return
    if field2_title and field2_value:
        if not (field1_title and field1_value):
            await interaction.response.send_message(
                "How do you want a second field when you don't have a first"
                " field?",
                ephemeral=True,
            )
            return
        embed_.add_field(name=field2_title, value=field2_value, inline=False)
    # field3
    if (field3_title and (not field3_value)) or (
        (not field3_title) and field3_value
    ):
        await interaction.response.send_message(
            "Have title AND value for field 3.",
            ephemeral=True,
        )
        return
    if field3_title and field3_value:
        if not (field1_title and field1_value):
            await interaction.response.send_message(
                "How do you want a third field when you don't have a first"
                " field?",
                ephemeral=True,
            )
            return
        if not (field2_title and field2_value):
            await interaction.response.send_message(
                "How do you want a third field when you don't have a second"
                " field?",
                ephemeral=True,
            )
            return
        embed_.add_field(name=field3_title, value=field3_value, inline=False)

    await interaction.response.send_message(embed=embed_)


@slash_command
@discord.app_commands.describe(
    channel="The discord text channel that where reports should go"
)
async def set_suggestion_channel(
    interaction: discord.Interaction, channel: discord.TextChannel
):
    """
    [Command] Set the suggestion channel.

    Args:
        channel (discord.TextChannel): The channel to set
    """
    if not interaction.user.resolved_permissions.manage_channels:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can manage"
                " channels, forget about setting the suggestion channel.",
                color=Color.RED,
            )
        )
        return
    # check is there a dict for server
    if db.get(interaction.guild.id) is False:
        db.set(str(interaction.guild.id), {})
    tmp = db.get(str(interaction.guild.id))
    # set channel
    tmp["suggestion_chn"] = channel.id
    db.set(str(interaction.guild.id), tmp)
    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Set suggestion channel to {str(channel)}!",
            color=Color.OKGREEN,
        )
    )


@slash_command
@discord.app_commands.describe(suggestion="The suggestion")
async def suggest(interaction: discord.Interaction, suggestion: str):
    """
    [Command] Suggest something.

    Args:
        suggestion (str): The suggestion
    """
    reload_db()
    if db.get(
        str(interaction.guild.id)
    ) is not False and "suggestion_chn" in db.get(str(interaction.guild.id)):
        chn = await client.fetch_channel(
            db.get(str(interaction.guild.id))["suggestion_chn"]
        )
        embed_ = my_embed(
            desc=suggestion, title=f"Suggestion by {interaction.user}"
        )

        msg = await chn.send(embed=embed_)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("⬇️")
        await interaction.response.send_message(
            embed=my_embed("Great! Suggestion sent.", color=Color.OKGREEN)
        )
    else:
        embed_ = my_embed(
            desc="There isn't a suggestion channel for this server.",
            color=Color.RED,
        )
        await interaction.response.send_message(embed=embed_)


@slash_command
@discord.app_commands.describe(
    user="The user to kick", reason="The reason of the punishment"
)
async def kick(
    interaction: discord.Interaction,
    user: Union[discord.User, discord.Member],
    reason: str,
):
    """
    [Command] Kick a user.

    Args:
        user (Union[discord.User, discord.Member]): The user to kick
        reason (str): The reason
    """
    if not interaction.user.resolved_permissions.kick_members:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can kick"
                " members yourself, forget about kicking anyone.",
                color=Color.RED,
                footer="Basically you don't have the permission to kick"
                " people",
            )
        )
        return
    if user == client.user:
        await interaction.response.send_message(
            embed=my_embed(
                desc="After all my good work *this* is how you reward me?"
                " What a disgrace.",
                color=Color.ORANGE,
            )
        )
        return
    # if isinstance(user, int):
    #     user = await client.fetch_user(user)
    try:
        await interaction.guild.kick(
            user=user,
            reason=reason,
        )
    except discord.errors.Forbidden:
        await interaction.response.send_message(
            embed=my_embed(
                f"Well... I can't kick members :(. Or maybe {user} is above"
                " me?",
                color=Color.RED,
            )
        )
        return
    reload_db()
    tmp = (
        db.get(str(interaction.guild.id))
        if db.get(str(interaction.guild.id)) is not False
        else {}
    )
    tmp[str(user.id)] = (
        db.get(str(interaction.guild.id))[str(user.id)]
        if tmp.get(str(user.id)) is not None
        else {}
    )
    tmp[str(user.id)]["punishments"] = (
        db.get(str(interaction.guild.id))[str(user.id)]["punishments"]
        if tmp.get(str(user.id)).get("punishments") is not None
        else []
    )
    tmp[str(user.id)]["punishments"].append(
        {
            "type": "kick",
            "moderator": interaction.user.id,
            "reason": reason,
            "time": datetime.now().timestamp(),
        }
    )
    db.set(str(interaction.guild.id), tmp)
    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Kicked {user} for reason `{reason}`!",
            color=Color.OKGREEN,
        )
    )


@slash_command
@discord.app_commands.describe(max_="The number of messages to remove")
async def purge(interaction: discord.Interaction, max_: int):
    """
    [Command] Purge messages.

    Args:
        ctx (commands.Context): The context
        max_ (int): The max messages to delete
    """
    if not interaction.user.resolved_permissions.manage_messages:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can manage"
                " messages yourself, forget about purge.",
                color=Color.RED,
                footer="Basically you don't have the permission to manage"
                " messages",
            )
        )
        return
    reload_db()
    # 255 is a nice number. There isn't (or i don't know of) any type of API
    # limitation, that is 255. It's just a nice number.
    if max_ >= 255 and interaction.user.id not in db.get("PURGE_LIMIT"):
        await interaction.response.send_message(
            embed=my_embed(
                desc=f"> Don't delete the whole channel\n- YUU8\n*(If you want"
                f" to delete a lot of messages, contact the developers"
                f" at {URLs.Issue.BLANK})*",
                color=Color.ORANGE,
                footer=f"Report hackers/bad people at {URLs.Issue.HACKER} and"
                f" they get banned from using this bot.",
            )
        )
        return
    tmp = await interaction.channel.purge(limit=max_)
    _color = Color.OKGREEN if max_ < 255 else Color.YELLOW

    await interaction.response.send_message(
        embed=my_embed(
            desc=f"{len(tmp)} messages have been deleted",
            color=_color,
        ),
        ephemeral=True,
    )


@slash_command
@discord.app_commands.describe(channel="The report channel")
async def set_report_channel(
    interaction: discord.Interaction, channel: discord.TextChannel
):
    """
    [Command] Set the report channel.

    Args:
        channel (discord.TextChannel): The channel to set
    """
    if not interaction.user.resolved_permissions.manage_channels:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can manage"
                " channels yourself, forget about setting the report channel.",
                color=Color.RED,
                footer="Basically you don't have the permission to manage"
                " channels",
            )
        )
        return
    reload_db()
    # check is there a dict for server
    if db.get(interaction.guild.id) is False:
        db.set(str(interaction.guild.id), {})
    tmp = db.get(str(interaction.guild.id))
    # set channel
    tmp["report_chn"] = channel.id
    db.set(str(interaction.guild.id), tmp)
    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Set report channel to {str(channel)}!",
            color=Color.OKGREEN,
        )
    )


@slash_command
@discord.app_commands.describe(
    user="The user you want to report", reason="The reason of the report"
)
async def report(
    interaction: discord.Interaction,
    user: Union[discord.User, discord.Member],
    reason: str,
):
    """
    [Command] Report a user.

    Args:
        user (Union[discord.User, discord.Member]): The user to report
        reason (str): The reason
    """
    reload_db()
    if (
        db.get(str(interaction.guild.id)) is False
        or db.get(str(interaction.guild.id)).get("report_chn") is None
    ):
        await interaction.response.send_message(
            embed=my_embed(
                desc="This server doesn't have a report channel",
                color=Color.RED,
            )
        )
        return
    chn = await client.fetch_channel(
        db.get(str(interaction.guild.id))["report_chn"]
    )

    await chn.send(
        embed=my_embed(
            title="Report",
            desc=f"Report by: {interaction.user}\nReported user: {user}"
            f"\nReason: {reason}",
        )
    )
    await interaction.response.send_message(
        embed=my_embed("OK. Report was sent.", color=Color.OKGREEN)
    )


@slash_command
@discord.app_commands.describe(
    cooldown="The slowmode in seconds. 0 to disable. Must be between [0,21600]"
)
async def slowmode(
    interaction: discord.Interaction, cooldown: Optional[int] = None
):
    """
    [Command] Manage the slowmode.

    Args:
        cooldown (Optional[int], optional): The cooldown. Defaults to None.
    """
    if not interaction.user.resolved_permissions.manage_channels:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can manage"
                " channels yourself, forget about setting the slowmode.",
                color=Color.RED,
                footer="Basically you don't have the permission to manage"
                " channels",
            )
        )
        return
    if cooldown is None:
        await interaction.response.send_message(
            embed=my_embed(
                desc=f"Slowmode is {interaction.channel.slowmode_delay}. If"
                " you want to disable it, set it to 0"
                if interaction.channel.slowmode_delay != 0
                else "Slowmode is disabled."
            )
        )
        return
    if cooldown > 21600:
        await interaction.response.send_message(
            embed=my_embed(
                desc="Cooldown must be between 0 and 21600",
                color=Color.RED,
            )
        )
        return
    await interaction.channel.edit(
        reason=f"{str(interaction.user)} set the slowmode to {cooldown}",
        slowmode_delay=max(cooldown, 0),
    )

    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Slowmode set to {cooldown}"
            if cooldown > 0
            else "Slowmode disabled",
            color=Color.OKGREEN,
        )
    )


@slash_command
@discord.app_commands.describe(
    user="The user to ban",
    reason="The reason of the punishment",
    delete_message_days="[OPTIONAL] Delete their messages that were sent in"
    " [n] days. If it's not passed, no messages will be removed.",
)
async def ban(
    interaction: discord.Interaction,
    user: Union[discord.User, discord.Member],
    reason: str,
    delete_message_days: Optional[int] = None,
):
    """
    [Command] Ban a user.

    Args:
        user (Union[discord.User, discord.Member, int]): The user to ban
        reason (str): The reason
        delete_message_days (Optional[int], optional): Delete message days.\
 Defaults to None.
    """
    if not interaction.user.resolved_permissions.ban_members:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can ban"
                " members yourself, forget about banning anyone",
                color=Color.RED,
                footer="Basically you don't have the permission to ban"
                " members",
            )
        )
        return
    if user == client.user:
        await interaction.response.send_message(
            embed=my_embed(
                desc="After all my good work *this* is how you reward me?"
                " What a disgrace.",
                color=Color.ORANGE,
            )
        )
        return
    if isinstance(delete_message_days, int) and (
        delete_message_days < 1 or delete_message_days > 7
    ):
        await interaction.response.send_message(
            embed=my_embed("delete_message_days must be between [1,7]")
        )
        return
    await interaction.guild.ban(
        user=user,
        reason=reason,
        delete_message_days=delete_message_days
        if delete_message_days is not None
        else 0,
    )
    reload_db()
    tmp = (
        db.get(str(interaction.guild.id))
        if db.get(str(interaction.guild.id)) is not False
        else {}
    )
    tmp[str(user.id)] = (
        db.get(str(interaction.guild.id))[str(user.id)]
        if tmp.get(str(user.id)) is not None
        else {}
    )
    tmp[str(user.id)]["punishments"] = (
        db.get(str(interaction.guild.id))[str(user.id)]["punishments"]
        if tmp.get(str(user.id)).get("punishments") is not None
        else []
    )
    tmp[str(user.id)]["punishments"].append(
        {
            "type": "ban",
            "moderator": interaction.user.id,
            "reason": reason,
            "delete_message_days": delete_message_days
            if delete_message_days is not None
            else 0,
            "time": datetime.now().timestamp(),
        }
    )
    db.set(str(interaction.guild.id), tmp)
    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Banned {user} for reason `{reason}`!", color=Color.OKGREEN
        )
    )


@slash_command
@discord.app_commands.describe(
    user="The user to unban", reason="The reason of the unban"
)
async def unban(
    interaction: discord.Interaction,
    user: Union[discord.User, discord.Member],
    reason: str,
):
    """
    [Command] Unban a user.

    Args:
        user (Union[discord.User, discord.Member, int]): The user to unban
        reason (str): The reason
    """
    if not interaction.user.resolved_permissions.ban_members:
        await interaction.response.send_message(
            embed=my_embed(
                "Not so fast! Who do you think you are? Until you can ban"
                " members yourself, forget about unbanning anyone.",
                color=Color.RED,
                footer="Basically you don't have the permission to ban"
                " members",
            )
        )
        return
    await interaction.guild.unban(
        user=user,
        reason=reason,
    )
    await interaction.response.send_message(
        embed=my_embed(
            desc=f"Unbanned {user} for reason `{reason}`!",
            color=Color.OKGREEN,
        )
    )


@slash_command
@discord.app_commands.describe(
    punishment="What should happen if the regex filter matches? del: Delete"
    " the message. kick: Delete the message + kick the member. ban: Delete the"
    " message + ban the user (forever). no: disable the regex filter.",
    pattern="The regex pattern. WithOUT slashes. Will be interpreted with the"
    " IGNORECASE flag.",
)
async def regex(
    interaction: discord.Interaction,
    punishment: Literal["del", "kick", "ban", "no"],
    pattern: Optional[str] = None,
):
    """
    [Command] Add a regex filter.

    Args:
        punishment (Literal["del", "kick", "ban", "no"]): The punishment
        pattern (Optional[str], optional): The regex pattern. Defaults to None.
    """
    if db.get(str(interaction.guild.id)) is False:
        db.set(str(interaction.guild.id), {})
    if punishment == "no":
        if pattern:
            await interaction.response.send_message(
                embed=my_embed(
                    "There's no need to repeat the regex pattern if you want"
                    " to delete it.",
                    color=Color.RED,
                )
            )
            return
        db.dadd(str(interaction.guild.id), ("regex", []))
        await interaction.response.send_message(
            embed=my_embed(desc="Deleted regex!", color=Color.OKGREEN)
        )
        return
    if pattern is None:
        await interaction.response.send_message(
            embed=my_embed(
                "A pattern is required. If you want to remove the pattern, use"
                ' "no"',
                color=Color.RED,
            )
        )
        return
    db.dadd(str(interaction.guild.id), ("regex", [pattern, "del"]))
    _desc = "If the regex `{}` matches anywhere, the message will be deleted{}."  # noqa
    if punishment == "ban":
        _desc = _desc.format(
            pattern,
            ", and the user will be banned forever,"
            " for reason: `Regex matched`",
        )
    elif punishment == "kick":
        _desc = _desc.format(
            pattern,
            ", and the user will be kicked, for reason: `Regex matched`",
        )
    else:
        _desc = _desc.format(pattern, "")
    await interaction.response.send_message(
        embed=my_embed(
            desc=_desc,
            color=Color.OKGREEN,
            title="Added regex!",
        )
    )


@slash_command
async def random(interaction: discord.Interaction):
    await interaction.response.send_message(str(SystemRandom().random()))


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None,
            lambda: YTDL.extract_info(url, download=not stream),
        )
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        return data["title"] if stream else YTDL.prepare_filename(data)


# ! NOT a command
async def _play(interaction: discord.Interaction, url: str):
    print(
        f"[PLAY] {url = !r};; creating youtube_dl.YoutubeDL with"
        f" {YTDL_FORMAT_OPTIONS!r}"
    )
    server: discord.Guild = interaction.guild
    while Path(".").name == "music_tmp":
        if Path("..").name == "music_tmp":
            shutil.rmtree(Path("."), ignore_errors=True)
        chdir("..")
    Path("./music_tmp").mkdir(parents=True, exist_ok=True)

    with change_working_directory("./music_tmp"):
        filename = await YTDLSource.from_url(url, loop=client.loop)
    if not interaction.user.voice:
        try:
            await interaction.response.send_message(
                embed=my_embed(
                    f"{interaction.user} is not connected to a voice channel",
                    color=Color.RED,
                )
            )
        except (discord.errors.NotFound, discord.errors.InteractionResponded):
            await interaction.channel.send(
                embed=my_embed(
                    f"{interaction.user} is not connected to a voice channel",
                    color=Color.RED,
                )
            )
        return 1
    channel: Union[
        discord.VoiceChannel, discord.StageChannel
    ] = interaction.user.voice.channel

    with contextlib.suppress(discord.errors.ClientException):
        await channel.connect()
    voice_client: discord.VoiceProtocol = server.voice_client
    for exe in EXES:
        try:
            replaced = str(Path(exe).absolute())
            print(f"[X] [PLAYMP3] Trying {exe!r} ({replaced!r})")
            if server.voice_client.is_playing():
                server.voice_client.stop()
            with change_working_directory("./music_tmp"):
                voice_client.play(
                    discord.FFmpegPCMAudio(
                        executable=replaced,
                        source=filename,
                        **FFMPEG_OPTIONS,
                    )
                )
        except Exception:
            print(f"[X] [PLAYMP3] {exe!r} did not work!")
            continue
        else:
            print("[☑] [PLAYMP3] Successfully played mp3")
            break
    else:
        raise RuntimeError("No ffmpeg worked")


def gen_crash_report(desc: str, custom: Optional[str] = None) -> None:
    rv = f"""---- YUU8 crash report ----
# {choice(CRASH_MESSAGE)}

Time: {time()}
Description: {desc}{NEW_LINE + custom if custom else ''}

{traceback.format_exc()}
"""
    print(rv)
    return rv


@slash_command
@discord.app_commands.describe(
    file="The .mp3 file withOUT the extension [MADE FOR PERSONAL USE ONLY]"
)
async def playmp3(interaction: discord.Interaction, file: str):
    """
    [Command] Play an .mp3 file. MADE FOR PERSONAL USE ONLY!

    Args:
        file (str): The .mp3 file withOUT the extension
    """
    with contextlib.suppress(discord.errors.ClientException):
        await interaction.user.voice.channel.connect()
    voice_client: discord.VoiceClient = discord.utils.get(
        client.voice_clients, guild=interaction.guild
    )

    for exe in EXES:
        try:
            print(f"[X] [PLAYMP3] Trying {exe!r}")
            audio_source = discord.FFmpegPCMAudio(
                f"{file}.mp3", executable=exe
            )
        except Exception:
            print("[X] [PLAYMP3] Failed to play mp3")
            continue
        else:
            print("[☑] [PLAYMP3] Successfully played mp3")
            break
    else:
        raise RuntimeError("No ffmpeg worked")
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(audio_source, after=None)
    await interaction.response.send_message(
        embed=my_embed(
            f"Playing `{file}`",
            color=Color.OKGREEN,
            footer="If there are any errors please open an issue at"
            f" {URLs.Issue.BUG}",
        )
    )


@slash_command
@discord.app_commands.describe(url="The YouTube video's URL")
async def play(
    interaction: discord.Interaction, url: str = "https://youtu.be/6BfKZLIEzZ0"
):
    """
    [Command] Play a YouTube video's audio

    Args:
        url (str, optional): The URL. Defaults to\
 "https://youtu.be/6BfKZLIEzZ0".
    """
    # <https://regexr.com/6sq1f>
    if not re.fullmatch(
        r"^https:\/\/(www\.)?youtu((\.be\/[0-9a-zA-Z]+)"
        r"|(be\.com\/watch\?v=[0-9a-zA-Z]+.*))$",
        url,
    ):
        await interaction.response.send_message(
            embed=my_embed(
                "I don't think so. Please gimme a YouTube URL including"
                " the HTTPS protocol. For example:"
                " `https://youtu.be/6BfKZLIEzZ0`",
                color=Color.RED,
            )
        )
        return
    await interaction.response.defer(thinking=True)
    loading = await interaction.channel.send(
        embed=my_embed(
            title="Loading...",
            desc="Downloading videos can take a lot of time, so just sit back,"
            " and relax. It can take up to 3-4 minutes. But at least you get"
            " the best quality audio, and there's no lag; the music doesn't"
            " stop randomly. The ETA is approx."
            " `video_time_in_seconds * 0.27`",
            color=Color.YELLOW,
        )
    )
    rv = await _play(interaction, url)
    await loading.delete()
    if rv == 1:
        await interaction.followup.send(
            embed=my_embed("Not connected to a voice channel", color=Color.RED)
        )
    else:
        embed_ = my_embed(f"Playing {url}", color=Color.OKGREEN)
        await interaction.followup.send(
            embed=embed_,
            view=PlayView(interaction.guild, embed_, url),
        )


class RepeatplayButton(discord.ui.Button["RepeatplayView"]):
    def __init__(self) -> None:
        super().__init__(style=discord.ButtonStyle.red, label="Stop")

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        self.disabled = True
        if db.get(str(self.view.guild.id)) is False:
            db.set(str(self.view.guild.id), {})
        db.dadd(str(self.view.guild.id), ("stop_repeatplay", True))
        await interaction.response.edit_message(view=self.view)


class RepeatplayView(discord.ui.View):
    children: List[RepeatplayButton]

    def __init__(self, guild: discord.Guild) -> None:
        super().__init__()
        self.guild = guild
        self.add_item(RepeatplayButton())


class Pause(discord.ui.Button["PlayView"]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.blurple, label="Pause", emoji="\u23f8"
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        self.view.guild.voice_client.pause()
        self.view.is_paused = True
        self.disabled = True
        self.style = discord.ButtonStyle.secondary
        self.view.children[1].disabled = False
        self.view.children[1].style = discord.ButtonStyle.blurple
        self.view.embed.color = Color.BLURPLE
        await interaction.response.edit_message(
            view=self.view, embed=self.view.embed
        )


class Resume(discord.ui.Button["PlayView"]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Resume",
            emoji="\u25b6",
            disabled=True,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        self.view.guild.voice_client.resume()
        self.view.is_paused = False
        self.disabled = True
        self.style = discord.ButtonStyle.secondary
        self.view.children[0].disabled = False
        self.view.children[0].style = discord.ButtonStyle.blurple
        self.view.embed.color = Color.OKGREEN
        await interaction.response.edit_message(
            view=self.view, embed=self.view.embed
        )


class RepeatOne(discord.ui.Button["PlayView"]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Repeat this song",
            emoji="\U0001f502",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        self.view.guild.voice_client.stop()
        self.view.disable_everything()
        await repeatplay.callback(interaction, self.view.url)


class Stop(discord.ui.Button["PlayView"]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Stop",
            emoji="\u23f9",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        self.view.guild.voice_client.stop()
        self.view.disable_everything(except_eject=True)
        await interaction.response.edit_message(
            view=self.view, embed=self.view.embed
        )


class Eject(discord.ui.Button["PlayView"]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Stop & Disconnect",
            emoji="\u23cf",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view
        await self.view.guild.voice_client.disconnect()
        self.view.disable_everything()
        await interaction.response.edit_message(
            view=self.view, embed=self.view.embed
        )


class PlayView(discord.ui.View):
    children: List[discord.ui.Button["PlayView"]]

    def __init__(
        self, guild: discord.Guild, embed_: discord.Embed, url: str
    ) -> None:
        super().__init__()
        self.guild = guild
        self.embed = embed_
        self.url = url
        self.add_item(Pause())
        self.add_item(Resume())
        self.add_item(RepeatOne())
        self.add_item(Stop())
        self.add_item(Eject())
        self.is_paused: bool = False

    def disable_everything(self, except_eject: bool = False) -> None:
        for butt in (
            (self.children[:-1]) if (except_eject) else (self.children)
        ):
            butt.style = discord.ButtonStyle.secondary
            butt.disabled = True
        self.embed.color = Color.BLACK


@slash_command
@discord.app_commands.describe(url="The YouTube video's URL")
async def repeatplay(interaction: discord.Interaction, url: str):
    """
    [Command] Play a YouTube video's audio forever

    Args:
        url (str): The URL.
    """
    # <https://regexr.com/6sq1f>
    if not re.fullmatch(
        r"^https:\/\/(www\.)?youtu((\.be\/[0-9a-zA-Z]+)"
        r"|(be\.com\/watch\?v=[0-9a-zA-Z]+.*))$",
        url,
    ):
        await interaction.response.send_message(
            embed=my_embed(
                "I don't think so. Please gimme a YouTube URL including"
                " the HTTPS protocol. For example:"
                " `https://youtu.be/6BfKZLIEzZ0`",
                color=Color.RED,
            )
        )
        return
    if not interaction.user.voice:
        await interaction.response.send_message(
            embed=my_embed(
                f"{interaction.user} is not connected to a voice channel",
                color=Color.RED,
            )
        )
        return
    await interaction.response.send_message(
        embed=my_embed(f"Playing {url} forever.", color=Color.OKGREEN),
        view=RepeatplayView(interaction.guild),
    )
    while_ = True
    while while_:
        await _play(interaction, url)
        try:
            while interaction.guild.voice_client.is_playing():
                await asyncio.sleep(1)
                with contextlib.suppress(KeyError):
                    if (
                        db.dget(str(interaction.guild.id), "stop_repeatplay")
                        is True
                    ):
                        db.dadd(
                            str(interaction.guild.id),
                            ("stop_repeatplay", False),
                        )
                        while_ = False
                        break
            if not while_:
                break
        except AttributeError:
            if interaction.guild.voice_client is not None:
                raise
    await interaction.guild.voice_client.disconnect()


@client.event
async def on_message(message: discord.Message):
    """
    On message event.

    Args:
        message (_type_): The message
    """
    reload_db()
    if message.guild is None:
        message.reply(
            embed=my_embed(
                "YUU8 does not accept commands or anything from DMs.",
                color=Color.ORANGE,
                footer=IFERROR,
            )
        )
        return
    if (
        str(message.guild.id) in db.db
        and db.get(str(message.guild.id)).get("regex")
        and re.search(
            db.get(str(message.guild.id))["regex"][0],
            message.content,
            re.I,
        )
    ):
        await message.delete()
        if db.get(str(message.guild.id))["regex"][1] == "kick":
            await message.guild.kick(message.author, reason="Matched regex.")
        elif db.get(str(message.guild.id))["regex"][1] == "ban":
            await message.guild.ban(message.author, reason="Matched regex.")

    # // await client.process_commands(message)


def main():
    print(
        """YUU8  Copyright (C) 2022  Koviubi56
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions."""
    )
    if not discord.opus.is_loaded():
        print("[X] [OPUS] Opus is not loaded. Trying to load it...")
        try:
            discord.opus.load_opus()
        except Exception as e:
            print(f"[X] [OPUS] Error while loading opus (without params): {e}")
            try:
                discord.opus.load_opus("opus")
            except Exception as e:
                print(
                    f"[X] [OPUS] Error while loading opus (with params): {e}"
                )
    if discord.opus.is_loaded():
        print("[☑] [OPUS] Opus loaded!")
    else:
        print("[X] [OPUS] Could not load opus!")
    client.run(getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
