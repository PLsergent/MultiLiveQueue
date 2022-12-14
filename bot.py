import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from ranking.commands import *
from matchmaking.commands import *

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    tree.add_command(captain_queue)
    tree.add_command(random_queue)
    tree.add_command(leaderboard)
    tree.add_command(rank)
    await tree.sync()
    print("Bot is ready!")

client.run(os.getenv('TOKEN'))