from discord import app_commands


@app_commands.command(name="captain_queue", description="Queue for a match as a captain")
async def captain_queue(interaction):
    await interaction.response.send_message("Added to captain queue!")

@app_commands.command(name="random_queue", description="Randomly match with someone")
async def random_queue(interaction):
    await interaction.response.send_message("Added to random queue!")