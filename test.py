cmd = '&character -a --foo "I am dumb"'

split = cmd.split(" ")[1:]
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

argdict = {}
for i, arg in enumerate(formattedSplit):
    if arg.startswith('-'):
        if formattedSplit[i+1].startswith('-'):
            argdict[arg] = True
        else:
            argdict[arg] = formattedSplit[i+1]