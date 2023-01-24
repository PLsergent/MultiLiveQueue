import discord
from discord import app_commands, Embed, File
from dotenv import load_dotenv
import os
from ranking.RankingCommands import Rank
from matchmaking.QueueCommands import Queue
from user.UserCommands import User
from match.MatchCommands import Match

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@app_commands.command(name="help", description="Help command")
async def help(ctx):
    embed = Embed(title=f"ℹ️ Help!! ℹ️", description="Simple steps to start using the bot", color=0x64e4f5)
    file = File("./assets/Marvin.png")
    embed.set_thumbnail(url="attachment://Marvin.png")
    embed.add_field(name="1. User", value="/user ingame <your-username>", inline=False)
    embed.add_field(name="2. Queue", value="/queue casual", inline=False)
    embed.add_field(name="3. Report match", value="/match report win 4-2", inline=False)
    embed.add_field(name="4. Check your stats", value="/user stats", inline=False)
    await ctx.response.send_message(file=file, embed=embed)

@client.event
async def on_ready():
    tree.add_command(Queue(client))
    tree.add_command(User())
    tree.add_command(Rank())
    tree.add_command(Match(client))
    tree.add_command(help)
    await tree.sync()
    print("Bot is ready!")

client.run(os.getenv('TOKEN'))