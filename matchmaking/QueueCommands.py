import discord
from discord import app_commands, Embed
from matchmaking.QueueController import QueueController
from user.UserController import UserController


@app_commands.guild_only()
class Queue(app_commands.Group):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)
        self.queues = QueueController()
    
    ranked = app_commands.Group(name="ranked", description="Ranked queue commands")

    @ranked.command(name="captain_queue", description="Queue for a match as a captain")
    async def captain(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queue_check(username):
            embed = self.queue_check(username)
            await ctx.response.send_message(embed=embed)
            return
        
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *ranked captain* queue !", description=message, color=0xd96664)
        await ctx.response.send_message(embed=embed)

        match = self.queues.check_if_match_ready(username, "captain_queue")
        if match:
            captain_username = match.team1[0]
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}, Captain: {captain_username}", color=0x64e4f5)
            await ctx.followup.send(embed=embed)
            # send ephemeral message to captain to pick a teammate
            captain = ctx.guild.get_member_named(captain_username)
            teammates = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in match.available_players)
            embed_dm = Embed(title="Pick a teammate:", description=teammates, color=0x64e4f5)
            await captain.send(embed=embed_dm, ephemeral=True)

    @ranked.command(name="random_queue", description="Randomly match with someone")
    async def random(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queue_check(username):
            embed = self.queue_check(username)
            await ctx.response.send_message(embed=embed)
            return

        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *ranked random* queue !", description=message, color=0xd96664)
        await ctx.response.send_message(embed=embed)

        match = self.queues.check_if_match_ready(username, "random_queue")
        if match:
            users_team1 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team1]
            members_team1 = [ctx.guild.get_member(user.id) for user in users_team1]
            users_team2 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team2]
            members_team2 = [ctx.guild.get_member(user.id) for user in users_team2]
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}", color=0x64e4f5)
            await ctx.followup.send(embed=embed)
            await self.create_match_category_and_channels(ctx.guild_id, match, members_team1, members_team2)

    @app_commands.command(name="casual", description="Queue for a casual match")
    async def casual(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queue_check(username):
            embed = self.queue_check(username)
            await ctx.response.send_message(embed=embed)
            return
        
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *casual* queue !", description=message, color=0x76d964)
        await ctx.response.send_message(embed=embed)
        
        match = self.queues.check_if_match_ready(username, "casual")
        if match:
            users_team1 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team1]
            members_team1 = [ctx.guild.get_member(user.id) for user in users_team1]
            users_team2 = [discord.utils.get(ctx.guild.members, name=member.split("#")[0], discriminator=member.split("#")[1]) for member in match.team2]
            members_team2 = [ctx.guild.get_member(user.id) for user in users_team2]
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}", color=0x64e4f5)
            await ctx.followup.send(embed=embed)
            await self.create_match_category_and_channels(ctx.guild_id, match, members_team1, members_team2)

    @app_commands.command(name="leave", description="Leave the queue")
    async def leave(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queues.is_in_queue(username):
            embed = Embed(title=f"⚠️ {username}, you are not in a queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if self.queues.remove_from_casual_queue(username):
            embed = Embed(title=f"✅ {username}, you have been removed from casual queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if self.queues.remove_from_ranked_queue(username, "captain_queue"):
            embed = Embed(title=f"✅ {username}, you have been removed from ranked captain queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        if self.queues.remove_from_ranked_queue(username, "random_queue"):
            embed = Embed(title=f"✅ {username}, you have been removed from ranked random queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
    
    @app_commands.command(name="status", description="Get the status of the queue")
    async def status(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queues.is_in_queue(username):
            embed = Embed(title=f"⚠️ {username}, you are not in a queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))
        embed = Embed(title=f"ℹ️ {username}, you are in a queue ! Wait for the battle", description=message, color=0x64e4f5)
        await ctx.response.send_message(embed=embed)
    
    def queue_check(self, username):
        user = UserController(username)
        embed = None
        if self.queues.is_in_queue(username):
            embed = Embed(title=f"⚠️ {username}, you are already in a queue!", color=0x64e4f5)
        if user.current_game_id != "":
            embed = Embed(title=f"⚠️ {username}, you are already in a game!", color=0x64e4f5)
        if user.in_game_username == "":
            embed = Embed(title=f"⚠️ {username}, you need to set your in-game username first!", color=0x64e4f5)
        return embed

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