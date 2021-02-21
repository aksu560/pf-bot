# -*- coding: utf-8 -*-
from discord.ext import commands
from .tools import argparse
from .tools import sheets
from .tools import paginate
from fuzzywuzzy import fuzz


class Pathfinder(commands.Cog):
    """This is an example cog, to be used as a base for creating your own. Do not load it."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.spell_sheet_id = '1cqjnKrvx2qjqlI09K8HapGoBxq42wOsFn87_t8xxn5s'
        self.spell_sheet = sheets.get_pf_sheet().get(spreadsheetId=self.spell_sheet_id, range='A2:CO').execute() \
            .get('values', [])

    @commands.command()
    async def Spell(self, ctx, *, argument: str):
        """Pull Pathfinder spell data"""

        # Data structure where we define all the flags and their types/aliases.
        arg_dict = {
            # Define all the arguments and their types here. You should avoid single character arguments here. Put
            # those into the aliases.
            "arg_index":
                {
                    "--help": type(True),
                    "--name": type(""),
                    "--search": type(""),
                    "--accuracy": type(""),
                    "--long": type(True),
                },
            # Define all the aliases for arguments here.
            "arg_alias":
                {
                    "-h": "--help",
                    "-n": "--name",
                    "-s": "--search",
                    "-f": "--search",
                    "-find": "--search",
                    "-a": "--long",
                    "-A": "--accuracy",

                },
            "arg_help":
                {
                    "--help": "Shows this message",
                    "--name": "Get spell by name",
                    "--accuracy": "Define accuracy for your search. 100 has to be exact match, 0 anything goes. "
                                  "Default 80 ",
                    "--long": "Show extended output",
                }
        }

        args = await argparse.parse(ctx.message, arg_dict, ctx)
        # All command logic should go under this, because if the return from argparse.parse() is false, incorrect
        # flags have been passed.
        if type(args) == type(""):
            await ctx.send(args)
            return
        else:

            # Enter parameters that should be enabled for single parameter use.
            if "single" in args:
                args["--name"] = args["single"]
                del args["single"]

            # Help output
            if "--help" in args.keys():
                await ctx.send(argparse.help_text(arg_dict))
                return

            target_acc = 80
            if "--accuracy" in args.keys():
                target_acc = int(args["--accuracy"])

            # Search by name
            if "--name" in args.keys():
                output = ""
                small_deets = []

                # Closest match data. First one is row of spell, second one is accuracy
                closest = [0, 0]
                matched = False
                for i, spell in enumerate(self.spell_sheet):
                    ratio = fuzz.ratio(spell[0].lower(), args["--name"].lower())
                    if ratio >= target_acc and ratio > closest[1]:
                        matched = True
                        print(f"New hit {ratio} vs {target_acc}")
                        closest = [i, ratio]

                output += f"{self.spell_sheet[closest[0]][0]}"

                if closest[1] < 95 or "--accuracy" in args or "--long" in args:
                    output += f" (Accuracy of {closest[1]}%)"

                output += ":```\n"

                # Small details
                small_deets.append(f"School: {self.spell_sheet[closest[0]][1]}")
                small_deets.append(f"Level: {self.spell_sheet[closest[0]][4]}")
                small_deets.append(f"Range: {self.spell_sheet[closest[0]][8]}")

                # This is how we handle details that might not always be relevant
                target = self.spell_sheet[closest[0]][11]
                if target:
                    small_deets.append(f"Target: {target}")
                area = self.spell_sheet[closest[0]][9]
                if area:
                    small_deets.append(f"Target: {area}")

                if self.spell_sheet[closest[0]][7] == 1 and "--long" not in args:
                    small_deets.append(f"Components: {self.spell_sheet[closest[0]][6]}")

                if "--long" in args:
                    small_deets.append(f"Descriptor: {self.spell_sheet[closest[0]][3]}")
                    small_deets.append(f"Casting time: {self.spell_sheet[closest[0]][5]}")
                    small_deets.append(f"Components: {self.spell_sheet[closest[0]][6]}")

                    subschool = self.spell_sheet[closest[0]][2]
                    if area:
                        small_deets.append(f"Subschool: {subschool}")

                small_deets.sort()
                for deet in small_deets:
                    output += f"{deet}\n"

                # Description
                output += "\nDescription:\n"
                if "--long" in args:
                    output += self.spell_sheet[closest[0]][17]
                else:
                    output += self.spell_sheet[closest[0]][44]

                output += "```"

                # Constructing the SRD link
                spell_name = self.spell_sheet[closest[0]][0].lower()
                link = f"https://www.d20pfsrd.com/magic/all-spells/{spell_name[0]}/{spell_name.replace(' ', '-')}"
                output += f"Source: <{link}>"

                if output and matched:
                    await ctx.send(output)
                else:
                    spell_name = args["--name"]
                    await ctx.send(f'Could not find spell "{spell_name}" :c')
                return

    @Spell.error
    async def Spell_eh(self, ctx: commands.Context, err: Exception):
        # Professional error handling
        print(err)
        await ctx.send("An error occurred. You might have done something wrong. If not, sorry about that.")


def setup(client: commands.Bot):
    client.add_cog(Pathfinder(client))
