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

import os
import logging
import discord  # noqa
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=21,
                    format="[%(levelname)s %(name)s] %(message)s")
logging = logging.getLogger(__name__)  # noqa
print("Loading...")

load_dotenv()

client = commands.Bot(
    command_prefix=".", description="A cool discord bot", owner_id=510548663496474660)


@client.event
async def on_ready():
    print("Ready!")


@client.command()
async def ping(ctx):
    await ctx.send("pong!")

client.run(os.getenv("BOT_TOKEN"))