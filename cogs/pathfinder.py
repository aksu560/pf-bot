# -*- coding: utf-8 -*-
from discord.ext import commands
from .tools import argparse
from .tools import sheets
from .tools import paginate
from fuzzywuzzy import fuzz
from copy import deepcopy


class Pathfinder(commands.Cog):
    """This is an example cog, to be used as a base for creating your own. Do not load it."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.spell_sheet_id = '1cqjnKrvx2qjqlI09K8HapGoBxq42wOsFn87_t8xxn5s'
        self.spell_sheet = sheets.get_pf_sheet().get(spreadsheetId=self.spell_sheet_id, range='A2:CO').execute() \
            .get('values', [])

        # The different flags for classes, and what column they correspond to
        self.class_filters = {
            "--wizard": 26,
            "--cleric": 28,
            "--druid": 29,
            "--ranger": 30,
            "--bard": 31,
            "--paladin": 32,
            "--alchemist": 33,
            "--summoner": 34,
            "--witch": 35,
            "--inquisitor": 36,
            "--oracle": 37,
            "--antipaladin": 38,
            "--magus": 39,
            "--adept": 40,
            "--bloodrager": 78,
            "--shaman": 79,
            "--psychic": 80,
            "--medium": 81,
            "--mesmerist": 82,
            "--occultist": 83,
            "--spiritualist": 84,
            "--skald": 85,
            "--investigator": 86,
            "--hunter": 87,
            "--unchained-summoner": 92,
        }

        self.schools = []

        for spell in self.spell_sheet:
            if spell[1] not in self.schools:
                self.schools.append(spell[1])

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
                    "--search": type(True),
                    "--accuracy": type(""),
                    "--long": type(True),
                    "--level": type(""),
                    "--school": type(""),
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
                    "--sorcerer": "--wizard",
                    "-S": "--school",
                },
            "arg_help":
                {
                    "--help": "Shows this message",
                    "--name": "Get spell by name",
                    "--accuracy": "Define accuracy for your search. 100 has to be exact match, 0 anything goes. "
                                  "Default 80",
                    "--long": "Show extended output",
                    "--[Class]": "Filter search by the class. Example --wizard, --unchained-summoner",
                    "--level": "Define spell level to filter by. Example: --level 6 gives only 6th level spells",
                    "--school": "Lets you search by spell school"
                }
        }

        # Add all the classes to the flags
        for cls in self.class_filters.keys():
            arg_dict["arg_index"][cls] = type(True)

        args = await argparse.parse(ctx.message, arg_dict, ctx)
        # All command logic should go under this, because if the return from argparse.parse() is false, incorrect
        # flags have been passed.
        if not args:
            await ctx.send("Something went wrong")
            return
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

            # Search functionality
            if "--search" in args.keys():
                results = deepcopy(self.spell_sheet)
                temp_results = []

                # Fuzzy searching through spell names
                if "--name" in args.keys():
                    query = args["--name"]
                    for i, spell in enumerate(results):
                        if fuzz.ratio(spell[0], query) >= target_acc:
                            temp_results.append(spell)
                    results = temp_results
                    temp_results = []

                # Filtering for classes able to cast the spell
                filtered_with_class = False
                for arg in args.keys():
                    if arg in self.class_filters:
                        filtered_with_class = True
                        for i, spell in enumerate(results):
                            if self.spell_filter_class(i, arg):
                                if "--level" in args.keys():
                                    if spell[self.class_filters[arg]] == args["--level"]:
                                        temp_results.append(spell)
                                else:
                                    temp_results.append(spell)

                if filtered_with_class:
                    results = temp_results
                    temp_results = []

                # Filter by school
                if "--school" in args.keys():
                    target_school = ""
                    highest = 0
                    for school in self.schools:
                        ratio = fuzz.ratio(school, args["--school"])
                        if ratio > highest:
                            highest = ratio
                            target_school = school

                    if highest < 80:
                        await ctx.send(f'Cannot find school "{args["--school"]}"')
                        return

                    for spell in results:
                        if spell[1] == target_school:
                            temp_results.append(spell)

                    results = temp_results
                    temp_results = []


                output = "```"
                for result in results:
                    output += f"{result[0]}\n"
                await paginate.send_codeblocks(output, ctx, "")
                return

            # Get one spell by name
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
                        closest = [i, ratio]

                output += f"{self.spell_sheet[closest[0]][0]}"

                if closest[1] < 95 or "--accuracy" in args or "--long" in args:
                    output += f" (Accuracy of {closest[1]}%)"

                output += ":```\n"

                # Small details
                small_deets.append(f"School: {self.spell_sheet[closest[0]][1]}")
                small_deets.append(f"Level: {self.spell_sheet[closest[0]][4]}")
                small_deets.append(f"Range: {self.spell_sheet[closest[0]][8]}")
                small_deets.append(f"Duration: {self.spell_sheet[closest[0]][12]}")

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


                # Constructing the SRD link
                spell_name = self.spell_sheet[closest[0]][0].lower()
                link = f"https://www.d20pfsrd.com/magic/all-spells/{spell_name[0]}/{spell_name.replace(' ', '-')}"
                output += f"Source: <{link}>"

                if output and matched:
                    print(output)
                    await paginate.send_codeblocks(output, ctx, "")
                else:
                    spell_name = args["--name"]
                    await ctx.send(f'Could not find spell "{spell_name}" :c')
                return

    # @Spell.error
    # async def Spell_eh(self, ctx: commands.Context, err: Exception):
    #     # Professional error handling
    #     print(err)
    #     await ctx.send("An error occurred. You might have done something wrong. Get fucked nerd.")

    def spell_filter_class(self, spell_i, cls):
        cls_i = self.class_filters[cls]
        return self.spell_sheet[spell_i][cls_i] != "NULL"


def setup(client: commands.Bot):
    client.add_cog(Pathfinder(client))
