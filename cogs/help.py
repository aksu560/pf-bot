# -*- coding: utf-8 -*-
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx, target_cog: str = ""):
        """Is a very helpful command"""

        # If no target cog was specified, we simply show all cogs.
        if target_cog == "":
            commands_text = f"Here are all the cogs available, please use &Help [cogname] for" \
                            f" help with individual commands```css\n"

            for cog in self.client.allCogs:
                commands_text += f"{cog[4:]}\n"

        # If a cog is specified, show the commands from target cog
        else:
            # Turn the target cog text into an actual cog object we can iterate over
            target_cog_object = self.client.get_cog(target_cog.capitalize())

            # If no cog is found, send an error message
            if target_cog_object is None:
                await ctx.send(f"{target_cog} was not found :c")
                return

            commands_text = f"Here are all the commands in {target_cog_object.qualified_name}```css"

            for command in target_cog_object.get_commands():
                commands_text += f"\n    &{command.name} "
                commands_text += f"{command.brief} " if command.brief is not None else ""
                commands_text += f"/* {command.help} */"

        # Cuts the output to multiple messages if the output would go over Discord's character limit
        if len(commands_text) > 2000:
            texts = []
            pos1 = commands_text.find('\n', 1700, 1900)
            texts.append(commands_text[:pos1] + "```")
            texts.append(f"```css\n{commands_text[pos1:]}```")
            for i in texts:
                await ctx.send(i)
        else:
            await ctx.send(commands_text + "```")

def setup(client: commands.Bot):
    client.add_cog(Help(client))
