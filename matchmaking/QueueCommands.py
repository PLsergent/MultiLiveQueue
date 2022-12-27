from discord import app_commands
from discord import Embed
from discord import Member
from discord import utils
from matchmaking.QueueController import QueueController
from user.UserController import UserController


@app_commands.guild_only()
class Queue(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queues = QueueController()
    
    ranked = app_commands.Group(name="ranked", description="Ranked queue commands")

    @ranked.command(name="captain_queue", description="Queue for a match as a captain")
    async def captain(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queues.add_to_ranked_queue(username, "captain_queue"):
            embed = Embed(title=f"⚠️ {username}, you are already in a queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *ranked captain* queue !", description=message, color=0xd96664)
        await ctx.response.send_message(embed=embed)

        match = self.queues.check_if_match_ready(username, "captain_queue")
        if match:
            captain_username = match.team1[0]
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}, Captain: {captain_username}", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            # send ephemeral message to captain to pick a teamate
            captain = ctx.guild.get_member_named(captain_username)
            teamates = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in match.available_players)
            embed_dm = Embed(title="Pick a teamate:", description=teamates, color=0x64e4f5)
            await captain.send(embed=embed_dm, ephemeral=True)

    @ranked.command(name="random_queue", description="Randomly match with someone")
    async def random(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queues.add_to_ranked_queue(username, "random_queue"):
            embed = Embed(title=f"⚠️ {username}, you are already in a queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *ranked random* queue !", description=message, color=0xd96664)
        await ctx.response.send_message(embed=embed)

        match = self.queues.check_if_match_ready(username, "random_queue")
        if match:
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            await self.create_match_category_and_channels()

    @app_commands.command(name="casual", description="Queue for a casual match")
    async def casual(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        if not self.queues.add_to_casual_queue(username):
            embed = Embed(title=f"⚠️ {username}, you are already in a queue!", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            return
        message = '*🙋‍♂️ Discord Username  |  👾 Multiversus Gamertag*\n\n' + '\n'.join(f'🙋‍♂️ {currentUser}  |  👾 {UserController(currentUser).in_game_username}' for currentUser in self.queues.get_my_queue(username))

        embed = Embed(title="🆕 challenger to the *ranked random* queue !", description=message, color=0x76d964)
        await ctx.response.send_message(embed=embed)

        match = self.queues.check_if_match_ready(username, "casual")
        if match:
            embed = Embed(title="🎉 Match ready !", description=f"👾 {match.id}", color=0x64e4f5)
            await ctx.response.send_message(embed=embed)
            await self.create_match_category_and_channels()

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
    
    async def create_match_category_and_channels(self, guild, match):
        category = await guild.create_category(f"Match {match.id}")
        for player in match.players:
            member = await guild.get_member_named(player)
            await category.set_permissions(member, read_messages=True, send_messages=True)
    
        team1_text_channel = await guild.create_text_channel(f"Match {match.id} - Team 1", category=category)
        team1_voice_channel = await guild.create_voice_channel(f"Match {match.id} - Team 1", category=category)
        for player in match.team1:
            member = await guild.get_member_named(player)
            await team1_text_channel.set_permissions(member, read_messages=True, send_messages=True)
            await team1_voice_channel.set_permissions(member)
        
        team2_text_channel = await guild.create_text_channel(f"Match {match.id} - Team 2", category=category)
        team2_voice_channel = await guild.create_voice_channel(f"Match {match.id} - Team 2", category=category)
        for player in match.team2:
            member = await guild.get_member_named(player)
            await team2_text_channel.set_permissions(member, read_messages=True, send_messages=True)
            await team2_voice_channel.set_permissions(member)