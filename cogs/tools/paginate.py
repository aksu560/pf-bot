async def send_codeblocks(msg: str, ctx, syntax='css'):
    if len(msg) > 2000:
        texts = []
        pos1 = msg.find('\n', 1700, 1900)
        texts.append(msg[:pos1] + "```")
        texts.append(f"```{syntax}\n{msg[pos1:]}```")
        for i in texts:
            await ctx.send(i)
    else:
        await ctx.send(msg + "```")