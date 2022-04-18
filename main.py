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

from datetime import datetime
from os import environ
from re import I, findall
from secrets import token_hex
from time import time
from typing import Optional, Union

import aiohttp
import discord
import pickledb  # nosec
from discord.ext import commands

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()

if __name__ == "__main__":
    print("Loading...")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix=".",
    description="A cool discord bot",
    owner_id=510548663496474660,
    intents=intents,
)

# TODO: Turn this OFF
DEBUG = True
db = pickledb.load("database.db", True)


def reloadDB():
    db.load("database.db", True)


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
        # BUG = "https://yerl.org/If5za9uTZntiwQmVXdVugX"
        BUG = "https://koviubi56-redirect.glitch.me/1.html"
        # https://github.com/koviubi56/YUU8/issues/new
        # BLANK = "https://yerl.org/9TwySiyYmZoSCHsiXYb90t"
        BLANK = "https://koviubi56-redirect.glitch.me/2.html"
        # https://github.com/koviubi56/YUU8/issues/new?assignees=&labels=Priority%3A+Medium&template=report-bad-user.md&title=
        # HACKER = "https://yerl.org/eCPRDRalWRL5e8mqn8bRKD"
        HACKER = "https://koviubi56-redirect.glitch.me/3.html"

    class file:
        # https://github.com/koviubi56/YUU8/blob/main/CONTRIBUTORS
        CONTRIBUTORS = "https://koviubi56-redirect.glitch.me/4.html"


IFERROR = (
    f"If you think this is an error, report it at {urls.issue.BUG}"
)


def myEmbed(
    desc: Optional[str] = None,
    title: Optional[str] = None,
    color: Optional[int] = color.BLURPLE,
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
        embed = discord.Embed(
            color=color,
            description=desc,
            timestamp=datetime.now(),
            title=title,
        )
    elif title:
        embed = discord.Embed(
            color=color, timestamp=datetime.now(), title=title
        )
    elif desc:
        embed = discord.Embed(
            color=color, description=desc, timestamp=datetime.now()
        )
    else:
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


def testUser(user: Union[discord.Member, discord.User]) -> bool:
    reloadDB()
    if db.get("BANNED_USERS") is False:
        raise Exception(
            'db.get("BANNED_USERS") is {}'.format(
                db.get("BANNED_USERS")
            )
        )
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
    embed = myEmbed(desc="The response time", title="Ping")

    embed.add_field(
        name="Ping by Discord",
        value=f"{client.latency:.2f} s/{client.latency * 1000:.2f} ms",
        inline=False,
    )

    reloadDB()
    dbping = 0
    for _ in range(100):
        old = time()
        reloadDB()
        db.getall()
        dbping += time() - old
    try:
        dbping /= 100
    except ZeroDivisionError:
        dbping = 0
    embed.add_field(
        name="Database latency",
        value=f"{dbping / 1000:f}s/{dbping:f}ms",
        inline=False,
    )

    # send
    await ctx.send(embed=embed)


@client.command()
async def unsplash(ctx: commands.Context, keyword: str):
    if testUser(ctx.author):
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
    fieldTitle: str,
    *fieldValue: str,
):
    if testUser(ctx.author):
        return
    embed = myEmbed(title=title)

    embed.add_field(
        name=fieldTitle,
        value=" ".join(fieldValue)
        if isinstance(fieldValue, tuple)
        else fieldValue,
    )

    await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_suggestion_channel(
    ctx: commands.Context, channel: discord.TextChannel
):
    if testUser(ctx.author):
        return
    try:
        # check is there a dict for server
        if db.get(ctx.guild.id) is False:
            db.set(str(ctx.guild.id), {})
        tmp = db.get(str(ctx.guild.id))
        # set channel
        tmp["suggestion_chn"] = channel.id
        db.set(str(ctx.guild.id), tmp)
    except Exception:
        raise
    else:
        await ctx.reply(
            embed=myEmbed(
                desc=f"Set suggestion channel to {str(channel)}!",
                color=color.OKGREEN,
            )
        )


@client.command()
async def suggest(ctx: commands.Context, *suggestion: str):
    if testUser(ctx.author):
        return
    reloadDB()
    if db.get(
        str(ctx.guild.id)
    ) is not False and "suggestion_chn" in db.get(str(ctx.guild.id)):
        chn = await client.fetch_channel(
            db.get(str(ctx.guild.id))["suggestion_chn"]
        )
        try:
            embed = myEmbed(
                desc=suggestion
                if isinstance(suggestion, str)
                else " ".join(suggestion)
            )
        except Exception:
            embed = myEmbed(
                desc=suggestion,
                footer="There was an error when we wanted to create this embed. Please report every bug at {}".format(
                    urls.issue.BUG
                ),
            )

        msg = await chn.send(embed=embed)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("⬇️")
    else:
        embed = myEmbed(
            desc="There isn't a suggestion channel for this server.",
            color=color.RED,
        )
        await ctx.reply(embed=embed)


@client.command()
async def debug(ctx: commands.Context):
    if testUser(ctx.author):
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
    if testUser(ctx.author):
        return
    try:
        if user == client.user:
            await ctx.reply(
                embed=myEmbed(
                    desc="After all my good work *this* is how you reward me? What a disgrace.",
                    color=color.ORANGE,
                )
            )
            return
        if not reason:
            raise commands.MissingRequiredArgument(
                MyParameter("reason")
            )
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
    except Exception:
        raise
    else:
        reloadDB()
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
        await ctx.reply(
            embed=myEmbed(
                desc="Kicked {} for reason `{}`!".format(
                    str(user),
                    tmp[str(user.id)]["punishments"][
                        len(tmp[str(user.id)]["punishments"]) - 1
                    ]["reason"],
                ),
                color=color.OKGREEN,
            )
        )


@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
@client.command()
async def purge(ctx: commands.Context, max: int):
    if testUser(ctx.author):
        return
    try:
        int(max)
    except Exception:
        await ctx.reply(
            embed=myEmbed(
                desc="Max must be an integer number.",
                color=color.RED,
                footer=IFERROR,
            )
        )
        return
    reloadDB()
    # 255 is a nice number. There isn't (or i don't know of) any type of API limitation, that is 255. It's just a nice number.
    if int(max) >= 255 and ctx.author.id not in db.get("PURGE_LIMIT"):
        await ctx.reply(
            embed=myEmbed(
                desc=f"> Don't delete the whole channel\n- YUU8\n*(If you want to delete a lot of messages, contact the developers at {urls.issue.BLANK})*",
                color=color.ORANGE,
                footer=f"Report hackers/bad people at {urls.issue.HACKER} and they get banned from using this bot.",
            )
        )
        return
    try:
        tmp = await ctx.channel.purge(limit=int(max) + 1)
    except Exception:
        raise
    else:
        # *                                                                  This is important because if the user WANTS to delete lots of messages, then it should be yellow
        # *                                                                                                             VVVVVVVV
        await ctx.channel.send(
            embed=myEmbed(
                desc=f"{str(len(tmp))} messages have been deleted",
                color=color.OKGREEN
                if int(max) < 255
                else color.YELLOW,
                footer=f"This user have been reached the purge limit! Report hackers/bad people at {urls.issue.HACKER} and they get banned from using this bot."
                if len(tmp) >= 255
                else "This message will be automaticly deleted after 5 seconds.",
            ),
            delete_after=5.0,
        )


@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
@client.command()
async def clear(ctx: commands.Context, *args, **kwargs):
    if testUser(ctx.author):
        return
    try:
        await purge(ctx, *args, **kwargs)
    except Exception:
        await ctx.reply(
            embed=myEmbed(
                desc="Something went wrong.\nDo you passed the max parameter? Is it an integer number that is bigger than zero?\n`.clear <MAX>`",
                color=color.RED,
                footer=IFERROR,
            )
        )


@client.command()
@commands.has_permissions(manage_channels=True)
async def set_report_channel(
    ctx: commands.Context, channel: discord.TextChannel
):
    if testUser(ctx.author):
        return
    try:
        reloadDB()
        # check is there a dict for server
        if db.get(ctx.guild.id) is False:
            db.set(str(ctx.guild.id), {})
        tmp = db.get(str(ctx.guild.id))
        # set channel
        tmp["report_chn"] = channel.id
        db.set(str(ctx.guild.id), tmp)
    except Exception:
        raise
    else:
        await ctx.reply(
            embed=myEmbed(
                desc=f"Set report channel to {str(channel)}!",
                color=color.OKGREEN,
            )
        )


@client.command()
async def report(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member],
    *reason,
):
    if testUser(ctx.author):
        return
    reloadDB()
    if (
        db.get(str(ctx.guild.id)) is False
        or db.get(str(ctx.guild.id)).get("report_chn") is None
    ):
        await ctx.reply(
            embed=myEmbed(
                desc="This server isn't have a report channel",
                color=color.RED,
            )
        )
        return
    if (
        reason is None
        or reason == ""
        or reason == " "
        or reason == ()
    ):
        raise commands.MissingRequiredArgument(MyParameter("reason"))
    chn = await client.fetch_channel(
        db.get(str(ctx.guild.id))["report_chn"]
    )

    await chn.send(
        embed=myEmbed(
            title="Report",
            desc="Report by: {report_by}\nReported user: {reported_user}\nReason: {reason}".format(
                report_by=str(ctx.author),
                reported_user=str(user),
                reason=" ".join(reason)
                if isinstance(reason, tuple)
                else reason,
            ),
        )
    )


@client.command()
async def slowmode(
    ctx: commands.Context, cooldown: Optional[int] = None
):
    if testUser(ctx.author):
        return
    if cooldown is None:
        await ctx.reply(
            embed=myEmbed(
                desc=f"Slowmode is {ctx.channel.slowmode_delay}. If you want to disable it, type `.slowmode 0`"
                if ctx.channel.slowmode_delay != 0
                else "Slowmode is disabled. To enable it, type `.slowmode <COOLDOWN>`"
            )
        )
        return
    if cooldown > 21600:
        await ctx.reply(
            embed=myEmbed(
                desc="Cooldown must be between 0 and 21600",
                color=color.RED,
            )
        )
        return
    try:
        await ctx.channel.edit(
            reason=f"{str(ctx.author)} set the slowmode to {cooldown}",
            slowmode_delay=max(cooldown, 0),
        )

    except Exception:
        raise
    else:
        await ctx.reply(
            embed=myEmbed(
                desc=f"Slowmode set to {cooldown}"
                if cooldown > 0
                else "Slowmode disabled",
                color=color.OKGREEN,
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
    if testUser(ctx.author):
        return
    try:
        if user == client.user:
            await ctx.reply(
                embed=myEmbed(
                    desc="After all my good work *this* is how you reward me? What a disgrace.",
                    color=color.ORANGE,
                )
            )
            return
        if reason == ():
            raise commands.MissingRequiredArgument(
                MyParameter("reason")
            )
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
    except Exception:
        raise
    else:
        reloadDB()
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
        await ctx.reply(
            embed=myEmbed(
                desc="Banned {} for reason `{}`!".format(
                    str(user),
                    tmp[str(user.id)]["punishments"][
                        len(tmp[str(user.id)]["punishments"]) - 1
                    ]["reason"],
                ),
                color=color.OKGREEN,
            )
        )


@client.command()
@commands.cooldown(3, 10, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def unban(
    ctx: commands.Context,
    user: Union[discord.User, discord.Member, int],
    reason: str,
):
    if testUser(ctx.author):
        return
    try:
        if user == client.user:
            await ctx.reply(
                embed=myEmbed(
                    desc="I'm not banned", color=color.ORANGE
                )
            )
            return
        if reason == ():
            raise commands.MissingRequiredArgument(
                MyParameter("reason")
            )
        if isinstance(user, int):
            user = await client.fetch_user(user)
        await ctx.guild.unban(
            user=user,
            reason=" ".join(reason)
            if isinstance(reason, tuple)
            else reason,
        )
    except Exception:
        raise
    else:
        await ctx.reply(
            embed=myEmbed(
                desc="Unbanned {} for reason `{}`!".format(
                    str(user),
                    " ".join(reason)
                    if isinstance(reason, tuple)
                    else reason,
                ),
                color=color.OKGREEN,
            )
        )


@client.command()
@commands.has_permissions(
    ban_members=True, kick_members=True, manage_messages=True
)
async def regex(
    ctx: commands.Context,
    punishment: str,
    regex: Optional[str] = None,
):
    if testUser(ctx.author):
        return
    if punishment not in ["del", "kick", "ban", "no"]:
        ctx.reply(
            'Punishment can be "del" to delete, "kick" to delete and kick, "ban" to delete and ban, or "no" to delete the regex.'
        )
        return
    if punishment == "no":
        db.dadd(str(ctx.message.guild.id), ("regex", []))
        await ctx.reply(
            embed=myEmbed(desc="Deleted regex!", color=color.OKGREEN)
        )
        return
    if regex is None:
        raise commands.MissingRequiredArgument(MyParameter("regex"))
    db.dadd(str(ctx.message.guild.id), ("regex", [regex, "del"]))
    await ctx.reply(
        embed=myEmbed(
            desc='If the regex `{}` matches anywhere, the message will be deleted{}.\nIf someone (including hackers, admins and mods) changes the regex to "." or something else, then you can\'t turn off the regex. For this reasons, type this command: `.get_code`.'.format(
                regex,
                ", and the user will be banned forever, for reason: `Regex matched`"
                if punishment == "ban"
                else ", and the user will be kicked, for reason: `Regex matched`"
                if punishment == "kick"
                else "",
            ),
            color=color.OKGREEN,
            title="Added regex!",
        )
    )


@client.command()
async def get_code(ctx: commands.Context):
    if ctx.author != ctx.guild.owner:
        await ctx.reply(
            embed=myEmbed(
                "Just the owner of the server can use this command, "
                + str(ctx.guild.owner),
                color=color.RED,
            )
        )
        return
    # yes, I know that this is unnecessary, but I want 101% security
    else:
        db.dadd(str(ctx.guild.id), ("code", token_hex(740)))
        dm = await ctx.guild.owner.create_dm()
        await dm.send(
            "This is the code for your server. This MUST be kept a secret! DO NOT share it even with your admins, mods!\n* Disable regex (in DM): `disable regex <SERVER ID> <CODE>` replace <SERVER ID> with the server's ID, <CODE> with the code.\n* Generate a new code (in DM): `new code <SERVER ID> <OLD CODE>` replace <SERVER ID> with your server's ID, <OLD CODE> with the (old) code.\n* Remove code (in DM): `remove code <SERVER ID> <CODE>` replace <SERVER ID> with your server's ID, <CODE> with the code.\n\nThis is the code:\n```\n{}\n```".format(
                db.dget(str(ctx.guild.id), "code")
            )
        )


@client.event
async def on_message(message):
    reloadDB()
    if message.guild is None:
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
                    "Done!\n(Note: For 69420% security you may want to generate a new code.)"
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
                    "This is the code for your server. This MUST be kept a secret! DO NOT share it even with your admins, mods!\n* Disable regex (in DM): `disable regex <SERVER ID> <CODE>` replace <SERVER ID> with the server's ID, <CODE> with the code.\n* Generate a new code (in DM): `new code <OLD CODE>` replace <OLD CODE> with the (old) code.\n* Remove code (in DM): `remove code <CODE>` replace <CODE> with the code.\n\nThis is the code:\n```\n{}\n```".format(
                        db.dget(str(tmp[2]), "code")
                    )
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
                    "This is the code for your server. This MUST be kept a secret! DO NOT share it even with your admins, mods!\n* Disable regex (in DM): `disable regex <SERVER ID> <CODE>` replace <SERVER ID> with the server's ID, <CODE> with the code.\n* Generate a new code (in DM): `new code <OLD CODE>` replace <OLD CODE> with the (old) code.\n* Remove code (in DM): `remove code <CODE>` replace <CODE> with the code.\n\nThis is the code:\n```\n{}\n```".format(
                        db.dget(str(tmp[2]), "code")
                    )
                )
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
    if testUser(ctx.author):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(
            embed=myEmbed(
                desc="Sorry, but you don't have permissions for that.",
                color=color.RED,
            )
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            embed=myEmbed(
                desc=error.args[0].capitalize(),
                color=color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.reply(
            embed=myEmbed(
                desc=error.args[0],
                color=color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
    elif (
        isinstance(error, discord.Forbidden) and error.code == 50013
    ) or error.args[
        0
    ] == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await ctx.reply(
            embed=myEmbed(
                desc="I don't have permission to do that.",
                color=color.RED,
            )
        )
    else:
        # Check for sensitive information
        tmp = next(
            (
                f"""Something went wrong!
For security reasons, we can't say more.
Please, open an issue here: {urls.issue.BUG}.
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
If you think that this is an error that we can fix, open an issue here: {urls.issue.BUG} and include this:
```py
{error.__class__ = }
{error.__cause__ = }{backslashn + str(error.args) if DEBUG else ""}
```
If you help us, you will be in the CONTRIBUTORS file ({urls.file.CONTRIBUTORS})""",
        )

        # Send
        await ctx.reply(
            embed=myEmbed(
                desc=tmp,
                color=color.RED,
                footer="Please, do not abuse with these informations!",
            )
        )
        raise error.__cause__
    if DEBUG:
        raise error.__cause__


def main():
    try:
        client.run(environ["BOT_TOKEN"])
    except KeyError as e:
        print(
            f"\n[ERROR] Environment variable `{e.args[0]}` is not set."
        )
        raise


if __name__ == "__main__":
    main()
