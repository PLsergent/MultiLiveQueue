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
        await ctx.response.defer()
        leaderboard = self.ranks.get_leaderboard()
        embed = Embed(title="Leaderboard 🏆", description="Top 10 players", color=0x64e4f5)
        file = File("./assets/Marvin.png")
        embed.set_thumbnail(url="attachment://Marvin.png")
        for i, player in enumerate(leaderboard):
            user = UserController(player)
            embed.add_field(name=f"{i + 1}. {player}", value=f"Rank: {user.ranking}\nPoints: {user.ranking_points}", inline=False)
        user_leaderboard = self.ranks.get_player_global_ranking(ctx.user.name + "#" + ctx.user.discriminator)
        embed.set_footer(text=f"Your global rank: n° {user_leaderboard + 1}")
        await ctx.followup.send(file=file, embed=embed)

    @app_commands.command(name="me", description="Get your rank")
    async def me(self, ctx):
        await ctx.response.defer()
        username = ctx.user.name + "#" + ctx.user.discriminator
        user_leaderboard = self.ranks.get_player_global_ranking(username)
        user = UserController(username)
        embed = Embed(title=f"{username} 🏆", color=0x64e4f5)
        embed.add_field(name="Rank", value=user.ranking, inline=True)
        embed.add_field(name="Points", value=user.ranking_points, inline=True)
        embed.add_field(name="Global rank", value=f"n° {user_leaderboard}", inline=False)
        file = File("./assets/Marvin.png")
        embed.set_thumbnail(url="attachment://Marvin.png")
        await ctx.followup.send_message(file=file, embed=embed)