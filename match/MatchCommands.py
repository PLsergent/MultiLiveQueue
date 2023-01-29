import discord
from discord import app_commands
from discord import Embed
from match.MatchController import MatchController
from user.UserController import UserController
import re


class Match(app_commands.Group):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)
    
    def get_match_for_user(self, username):
        user = UserController(username)
        if user.current_game_id != "":
            return MatchController(user.current_game_id)
        return None
    
    async def teammates_autocomplete(self, ctx, current: str):
        match = self.get_match_for_user(ctx.user.name + "#" + ctx.user.discriminator)
        teammates = []
        if match is not None:
            teammates = match.available_players
        return [
                app_commands.Choice(name=teammate, value=teammate)
                for teammate in teammates if current.lower() in teammate.lower()
            ]
    
    @app_commands.command(name="pick", description="Pick a teammate")
    @app_commands.autocomplete(teammate=teammates_autocomplete)
    async def pick(self, ctx, teammate: str):
        username = ctx.user.name + "#" + ctx.user.discriminator
        match = self.get_match_for_user(username)

        if match is None:
            embed = Embed(title=f"⚠️ {username}, you are not in a match!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if match.queue_type != "captain_queue":
            embed = Embed(title=f"⚠️ {username}, you are not in a captain queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if username not in match.team1:
            embed = Embed(title=f"⚠️ {username}, you are not the captain!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if teammate not in match.available_players:
            embed = Embed(title=f"⚠️ {teammate} is not available!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        
        match.pick_mate(teammate)
        embed = Embed(title=f"✅ You picked {teammate} for your team.", color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
        users_team1 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team1]
        members_team1 = [ctx.guild.get_member(user.id) for user in users_team1]
        users_team2 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team2]
        members_team2 = [ctx.guild.get_member(user.id) for user in users_team2]
        await self.create_match_category_and_channels(ctx.guild_id, match, members_team1, members_team2)

    @app_commands.command(name="report", description="Report match result")
    @app_commands.choices(result=[
        app_commands.Choice(name="win", value="win"),
        app_commands.Choice(name="loss", value="loss")
    ])
    async def report(self, ctx, result: app_commands.Choice[str], score: str):
        username = ctx.user.name + "#" + ctx.user.discriminator
        match = self.get_match_for_user(username)
        if match is None or match.status != "Ready":
            embed = Embed(title=f"⚠️ {username}, you are not in a match or the match is not ready!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        
        if not re.match(r"^\d+-\d+$", score):
            embed = Embed(title=f"⚠️ {username}, the score is not valid!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        
        if match.queue_type != "casual":
            if result.value == "win":
                ko_winner = score.split("-")[0]
                ko_loser = score.split("-")[1]
                match.report_winner(username, int(ko_winner), int(ko_loser))
            elif result.value == "loss":
                ko_winner = score.split("-")[1]
                ko_loser = score.split("-")[0]
                match.report_loser(username, int(ko_winner), int(ko_loser))
            else:
                embed = Embed(title=f"⚠️ {username}, the result is not valid!", color=0x64e4f5)
                await ctx.response.send_message(embed=embed)
                return

        embed = Embed(title=f"✅ You reported a {result.value} for this match.", color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
        match.status = "Reported"
        match.write_match()
        await self.delete_match_category_and_channels(ctx.guild_id, match)
        match.delete_match()

    @app_commands.command(name="delete_channels", description="Delete match categories and channels")
    async def delete_channels(self, ctx):
        await self.delete_match_all_category_and_channels(ctx.guild_id)
        embed = Embed(title=f"✅ You deleted the match channels.", color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name="abandon", description="Abandon match")
    async def abandon(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        match = self.get_match_for_user(username)
        if match is None:
            embed = Embed(title=f"⚠️ {username}, you are not in a match!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        
        match.abandon_match(username)
        embed = Embed(title=f"✅ You abandoned this match.", color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
    
    async def delete_match_category_and_channels(self, guild_id, match):
        guild = self.client.get_guild(guild_id)
        category = discord.utils.get(guild.categories, name=f"Match {match.id}")
        if category is not None:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
    
    async def delete_match_all_category_and_channels(self, guild_id):
        guild = self.client.get_guild(guild_id)
        for category in guild.categories:
            if category.name.startswith("Match"):
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
    
    async def create_match_category_and_channels(self, guild_id, match, team1, team2):
        guild = await self.client.fetch_guild(guild_id)
        everyone = guild.default_role
        overwrites = {
            everyone: discord.PermissionOverwrite.from_pair(deny=discord.Permissions.all(), allow=[])
        }
        category = await guild.create_category(f"Match {match.id}", overwrites=overwrites)
       
        team1_text_channel = await guild.create_text_channel(f"Team 1", category=category)
        team1_voice_channel = await guild.create_voice_channel(f"Team 1", category=category)

        for member in team1:
            await team1_text_channel.set_permissions(member, read_messages=True, send_messages=True)
            await team1_voice_channel.set_permissions(member, connect=True, speak=True, view_channel=True)
        
        team2_text_channel = await guild.create_text_channel(f"Team 2", category=category)
        team2_voice_channel = await guild.create_voice_channel(f"Team 2", category=category)
        for member in team2:
            await team2_text_channel.set_permissions(member, read_messages=True, send_messages=True)
            await team2_voice_channel.set_permissions(member, connect=True, speak=True, view_channel=True)
        