from discord.ext import commands
import configparser
import os
import logging

prefix = "&"

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = commands.AutoShardedBot(command_prefix=prefix, help_command=None)
client.remove_command("help")

client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
client.cfgParser.read_file(auth)
clientKey = client.cfgParser.get("discord", "key")

client.allCogs = [
    "cogs.help",
    "cogs.pathfinder",
    "cogs.upkeep",
]


@client.event
async def on_ready():
    print("==== Booting Up ====")

    print("Loading cogs...")
    for cog in client.allCogs:
        try:
            client.load_extension(cog)
            print(f"Successfully loaded cog \"{cog}\"")
        except Exception as err:
            print(f"Failed to load cog \"{cog}\" [{type(err).__name__}: {err}]")

    print(f"-- Connected to {len(client.guilds)} servers:")
    for server in client.guilds:
        print(f":: {server.name}")

    print("==== Boot Success! ====")


@client.event
async def on_message(msg):
    await client.process_commands(msg)

@client.event
async def on_guild_join(guild):
    print(f"Joined {guild.name}.")

@client.event
async def on_guild_remove(guild):
    print(f"Left {guild.name}.")


client.run(clientKey)
