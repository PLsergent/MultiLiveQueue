from discord import app_commands, Embed, File

from ranking.RankingController import RankingController
from user.UserController import UserController


@app_commands.guild_only()
class Rank(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranks = RankingController()

    @app_commands.command(name="leaderboard", description="View the leaderboard")
    async def leaderboard(self, ctx):
        leaderboard = self.ranks.get_leaderboard()
        embed = Embed(title="Leaderboard 🔥", description="Top 10 players", color=0x64e4f5)
        file = File("./assets/Marvin.png")
        embed.set_thumbnail(url="attachment://Marvin.png")
        for i, player in enumerate(leaderboard):
            user = UserController(player)
            embed.add_field(name=f"{i + 1}. {player}", value=f"Rank: {user.ranking}\nPoints: {user.ranking_points}", inline=False)
        await ctx.response.send_message(file=file, embed=embed)

    @app_commands.command(name="me", description="Get your rank")
    async def me(self, ctx):
        await ctx.response.send_message(self.ranks.get_my_rank(ctx.user.name + "#" + ctx.user.discriminator))