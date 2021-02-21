# -*- coding: utf-8 -*-
from discord.ext import commands
from .permissions import creator
from .tools import paginate


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx, target_cog: str = ""):
        """Is a very helpful command"""

        restricted_cogs = [".upkeep", "Upkeep"]

        # If no target cog was specified, we simply show all cogs.
        if target_cog == "":
            commands_text = f"Here are all the cogs available, please use &Help [cogname] for" \
                            f" help with individual commands```css\n"

            for cog in self.client.allCogs:
                # Dont list Upkeep commands to people who aren't marked as the creator
                if cog[4:] in restricted_cogs and not creator.isCreator(ctx):
                    continue
                commands_text += f"{cog[4:]}\n"

        # If a cog is specified, show the commands from target cog
        else:
            # Turn the target cog text into an actual cog object we can iterate over
            target_cog_object = self.client.get_cog(target_cog.capitalize())

            if target_cog_object.qualified_name in restricted_cogs and not creator.isCreator(ctx):
                await ctx.send(">:c")
                return

            # If no cog is found, send an error message
            if target_cog_object is None:
                await ctx.send(f"{target_cog} was not found :c")
                return

            commands_text = f"Here are all the commands in {target_cog_object.qualified_name}```css"

            for command in target_cog_object.get_commands():
                commands_text += f"\n    &{command.name} "
                commands_text += f"{command.brief} " if command.brief is not None else ""
                commands_text += f"/* {command.help} */"

        await paginate.send_codeblocks(commands_text, ctx)

def setup(client: commands.Bot):
    client.add_cog(Help(client))
