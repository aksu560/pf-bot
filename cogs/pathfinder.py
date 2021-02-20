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

        # Data structure where we define all the flags and their types/aliases.
        arg_dict = {
            # Define all the arguments and their types here. You should avoid single character arguments here. Put
            # those into the aliases.
            "arg_index":
                {
                    "--help": type(True),
                    "--name": type(""),
                },
            # Define all the aliases for arguments here.
            "arg_alias":
                {
                    "-h": "--help",
                    "-f": "--help",
                    "-n": "--name",
                },
            "arg_help":
                {
                    "--help": "Shows this message",
                    "--name": "Name of the spell",
                    "--foo": "Test flag",
                }
        }

        args = await argparse.parse(ctx.message, arg_dict, ctx)

        # All command logic should go under this, because if the return from argparse.parse() is false, incorrect
        # flags have been passed.
        if args:

            # Help output
            if "--help" in args.keys():
                await ctx.send(argparse.help_text(arg_dict))
                return

            await ctx.send(args)


def setup(client: commands.Bot):
    client.add_cog(Pathfinder(client))
