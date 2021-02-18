from discord.ext import commands


# Just checks if the command author's userID matches. This one is mine, replace this with your's if you are hosting
# this by yourself
def isCreator(ctx: commands.Context):
    return ctx.author.id == 114796980739244032

async def isCreatorAsync(ctx: commands.Context):
    return ctx.author.id == 114796980739244032