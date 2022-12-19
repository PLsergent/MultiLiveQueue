from dataclasses import dataclass
from discord import app_commands
from matchmaking.Queues import Queues


@app_commands.guild_only()
class Queue(app_commands.Group):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queues = Queues()
    
    ranked = app_commands.Group(name="ranked", description="Ranked queue commands")

    @ranked.command(name="captain_queue", description="Queue for a match as a captain")
    async def captain(self, interaction):
        username = interaction.user.name + "#" + interaction.user.discriminator
        if not self.queues.add_to_ranked_queue(username, "captain_queue"):
            await interaction.response.send_message("You are already in a queue!")
            return
        await interaction.response.send_message(f"Added to captain queue! {self.queues.get_my_queue(username)}")

    @ranked.command(name="random_queue", description="Randomly match with someone")
    async def random(self, interaction):
        username = interaction.user.name + "#" + interaction.user.discriminator
        if not self.queues.add_to_ranked_queue(username, "random_queue"):
            await interaction.response.send_message("You are already in a queue!")
            return
        await interaction.response.send_message(f"Added to random queue! {self.queues.get_my_queue(username)}")

    @app_commands.command(name="casual", description="Queue for a casual match")
    async def casual(self, interaction):
        username = interaction.user.name + "#" + interaction.user.discriminator
        if not self.queues.add_to_casual_queue(username):
            await interaction.response.send_message("You are already in a queue!")
            return
        await interaction.response.send_message(f"Added to casual queue! {self.queues.get_my_queue(username)}")

    @app_commands.command(name="leave", description="Leave the queue")
    async def leave(self, interaction):
        username = interaction.user.name + "#" + interaction.user.discriminator
        if not self.queues.is_in_queue(username):
            await interaction.response.send_message("You are not in a queue!")
            return
        if self.queues.remove_from_casual_queue(username):
            await interaction.response.send_message("Removed from casual queue!")
            return
        if self.queues.remove_from_ranked_queue(username, "captain_queue"):
            await interaction.response.send_message("Removed from captain queue!")
            return
        if self.queues.remove_from_ranked_queue(username, "random_queue"):
            await interaction.response.send_message("Removed from random queue!")
            return
    
    @app_commands.command(name="status", description="Get the status of the queue")
    async def status(self, interaction):
        username = interaction.user.name + "#" + interaction.user.discriminator
        if not self.queues.is_in_queue(username):
            await interaction.response.send_message("You are not in a queue!")
            return
        await interaction.response.send_message(self.queues.get_my_queue(username))
