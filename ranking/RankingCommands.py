from discord import app_commands

from ranking.RankingController import RankingController


@app_commands.guild_only()
class Rank(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranks = RankingController()

    @app_commands.command(name="leaderboard", description="View the leaderboard")
    async def leaderboard(self, ctx):
        await ctx.response.send_message(self.ranks.get_leaderboard())

    @app_commands.command(name="me", description="Get your rank")
    async def me(self, ctx):
        await ctx.response.send_message(self.ranks.get_my_rank(ctx.user.name + "#" + ctx.user.discriminator))