from discord import app_commands
from discord import Embed
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
