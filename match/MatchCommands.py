import discord
from discord import app_commands
from discord import Embed
from match.MatchController import MatchController
from user.UserController import UserController


class Match(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_match_for_user(self, username):
        user = UserController(username)
        if user.current_game_id != "":
            return MatchController(user.current_game_id)
        return None
    
    async def teamates_autocomplete(self, ctx, current: str):
        match = self.get_match_for_user(ctx.user.name + "#" + ctx.user.discriminator)
        teamates = []
        if match is not None:
            teamates = match.available_players 
        return [
                app_commands.Choice(name=teamate, value=teamate)
                for teamate in teamates if current.lower() in teamate.lower()
            ]
    
    @app_commands.command(name="pick", description="Pick a teamate")
    @app_commands.autocomplete(teamate=teamates_autocomplete)
    async def pick(self, ctx, teamate: str):
        username = ctx.user.name + "#" + ctx.user.discriminator
        match = self.get_match_for_user(username)
        if match is None:
            embed = Embed(title=f"⚠️ {username}, you are not in a match!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if username not in match.team1:
            embed = Embed(title=f"⚠️ {username}, you are not the captain!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if teamate not in match.available_players:
            embed = Embed(title=f"⚠️ {teamate} is not available!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        match.pick_mate(teamate)
        embed = Embed(title=f"✅ You picked {teamate} for your team.", color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
        users_team1 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team1]
        members_team1 = [ctx.guild.get_member(user.id) for user in users_team1]
        users_team2 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team2]
        members_team2 = [ctx.guild.get_member(user.id) for user in users_team2]
        await self.create_match_category_and_channels(ctx.guild_id, match, members_team1, members_team2)
    
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
        