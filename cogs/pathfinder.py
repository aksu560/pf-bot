# -*- coding: utf-8 -*-
from discord.ext import commands
from .tools import argparse


class Pathfinder(commands.Cog):
    """This is an example cog, to be used as a base for creating your own. Do not load it."""

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Spell(self, ctx, *, argument: str):
        """Example command"""

        args = argparse.parse(ctx.message)

        await ctx.send(args)


def setup(client: commands.Bot):
    client.add_cog(Pathfinder(client))
