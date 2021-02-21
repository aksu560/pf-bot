# This is a shit flag argument parser, with confusing logic, and borderline nonsensical configuration. Don't use it.

async def parse(msg, cmd_args, ctx):
    split = msg.content.split(" ")[1:]
    formattedSplit = []
    wip_brackets = ""
    in_brackets = False
    for entry in split:
        # Checking if the argument is in quotation marks due to whitespaces
        if entry.startswith("'") or entry.startswith('"') or in_brackets:
            in_brackets = True
            # Remove the quotation marks from the string if present
            if entry.startswith("'") or entry.startswith('"'):
                wip_brackets += entry[1:]
            elif entry.endswith('"') or entry.endswith("'"):
                wip_brackets += entry[:-1]
            else:
                wip_brackets += entry

            # Add back the spaces we removed with split
            if not (entry.endswith("'") or entry.endswith('"')):
                wip_brackets += " "
            # Handle closing the argument
            if entry.endswith('"') or entry.endswith("'"):
                in_brackets = False
                formattedSplit.append(wip_brackets)
                wip_brackets = ""

        else:
            formattedSplit.append(entry)

    if len(formattedSplit) == 1 and not formattedSplit[0].startswith("-"):
        return {"single": formattedSplit[0]}

    argdict = {}
    for i, arg in enumerate(formattedSplit):
        try:
            if arg.startswith('-'):
                if formattedSplit[i + 1].startswith('-'):
                    argdict[arg] = True
                else:
                    argdict[arg] = formattedSplit[i + 1]
        except IndexError as e:
            argdict[arg] = True

    # Handling aliases
    for arg in argdict.keys():
        if arg in cmd_args["arg_alias"]:
            # Store the value for the alised flag.
            arg_value = argdict[arg]
            # Remove the alias value from output.
            argdict.pop(arg)
            # add the non aliased flag in, with the correct value.
            argdict[cmd_args["arg_alias"][arg]] = arg_value

    # Validate types
    for arg in argdict.keys():
        try:
            if not type(argdict[arg]) == cmd_args["arg_index"][arg]:
                expected_type = str(cmd_args['arg_index'][arg]).split("'")[1]
                got_type = str(type(argdict[arg])).split("'")[1]
                await ctx.send(
                    f"Command {ctx.command} flag {arg} expected type {expected_type}. Got {got_type} instead")
                return False
        except KeyError as e:
            return f'Command "{ctx.command}" has no flag {e}'

    return argdict


# Returns all the aliases for target flag.
def parse_aliases(target_arg, args):
    output = []
    for alias in args["arg_alias"].keys():
        if args["arg_alias"][alias] == target_arg:
            output.append(alias)

    return output


def help_text(arg_dict):
    flaglist = []
    for arg in arg_dict["arg_help"].keys():
        flaglist.append(
            f"{str(arg)}{', '.join(['']+parse_aliases(arg, arg_dict))}: {arg_dict['arg_help'][arg]}"
        )
    flaglist.sort()
    output = "```"
    for flag in flaglist:
        output += f"{flag}\n"
    output += "```"
    return output
