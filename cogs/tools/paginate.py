async def send_codeblocks(msg: str, ctx, syntax='css'):
    splitted = msg.split("\n")

    temp_part = ""
    for split in splitted:
        temp_part += f"{split}\n"
        if len(temp_part) > 1900:
            temp_part += "```"
            await ctx.send(temp_part)
            temp_part = f"```{syntax}\n"
    temp_part += "```"
    if len(temp_part) > len(f"```{syntax}\n```")+1:
        await ctx.send(temp_part)