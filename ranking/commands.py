from discord import app_commands


@app_commands.command(name="leaderboard", description="View the leaderboard")
async def leaderboard(interaction):
    await interaction.response.send_message("Leaderboard!")

@app_commands.command(name="rank", description="Get your rank")
async def rank(interaction):
    await interaction.response.send_message("Your rank is 1000!")