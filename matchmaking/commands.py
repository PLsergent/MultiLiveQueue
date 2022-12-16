from discord import app_commands

# List of captain_queue
captain_queue_list= []

# List of random_queue
random_queue_list = []

@app_commands.command(name="captain_queue", description="Queue for a match as a captain")
async def captain_queue(interaction):
    if(interaction.user.name + "#" + interaction.user.discriminator in captain_queue_list):
        await interaction.response.send_message("You are already in the captain queue!")
        return
    captain_queue_list.append(interaction.user.name + "#" + interaction.user.discriminator)
    print(captain_queue_list)
    await interaction.response.send_message("Added to captain queue!")

@app_commands.command(name="random_queue", description="Randomly match with someone")
async def random_queue(interaction):
    if(interaction.user.name + "#" + interaction.user.discriminator in random_queue_list):
        await interaction.response.send_message("You are already in the random queue!")
        return
    random_queue_list.append(interaction.user.name + "#" + interaction.user.discriminator)
    await interaction.response.send_message("Added to random queue!")