from discord import app_commands, Embed, File
from user.UserController import UserController


PATH = "./data/"
PATH_PLAYER = "./data/players/"

@app_commands.guild_only()
class User(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @app_commands.command(name="stats", description="Shows your stats on MultiLiveQueue")
    async def stats(self, ctx):
        username = ctx.user.name + "#" + ctx.user.discriminator
        user = UserController(username)
        if user.matches_played == 0:
            winrate = 0
        else:
            winrate = (user.matches_won/user.matches_played)*100

        embed = Embed(title=f"📊 {username} stats!", color=0x64e4f5)
        file = File("./assets/Marvin.png")
        embed.set_thumbnail(url="attachment://Marvin.png")
        embed.add_field(name="In-game", value=user.in_game_username, inline=False)
        embed.add_field(name="⚔️ Played", value=user.matches_played, inline=True)
        embed.add_field(name="✅ Won", value=user.matches_won, inline=True)
        embed.add_field(name="😬 Winrate", value=f"{winrate:.2f}%", inline=True)
        embed.add_field(name="❌ Multiplier", value=user.winstreak_multiplier, inline=True)
        embed.add_field(name="🏅 Ranking", value=user.ranking, inline=True)
        embed.add_field(name="💯 Points", value=user.ranking_points, inline=True)
        await ctx.response.send_message(file=file, embed=embed)
    
    @app_commands.command(name="rank", description="Shows your rank")
    async def rank(self, ctx):
        user = UserController(ctx.user.name + "#" + ctx.user.discriminator)
        await ctx.response.send_message(
            f"{user.username} is rank {user.ranking} with {user.ranking_points} ranking points."
        )

    @app_commands.command(name="ingame", description="Sets your in-game username")
    async def ingame(self, ctx, ingame_username: str):
        user = UserController(ctx.user.name + "#" + ctx.user.discriminator)
        user.add_ingame_username(ingame_username)
        await ctx.response.send_message(f"Your in-game username is now {ingame_username}.")
    
    @app_commands.command(name="muliversus", description="Shows your Muliversus stats")
    async def muliversus(self, ctx):
        user = UserController(ctx.user.name + "#" + ctx.user.discriminator)
        await ctx.response.send_message(
            f"https://muliversus.plsergent.xyz/{user.in_game_username}"
        )
        