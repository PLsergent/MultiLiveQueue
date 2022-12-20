from discord import app_commands
from user.UserController import UserController


PATH = "./data/"
PATH_PLAYER = "./data/players/"

@app_commands.guild_only()
class User(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = UserController()
    
    @app_commands.command(name="rank", description="Shows your rank")
    async def rank(self, ctx):
        self.user.init_user(ctx.user.name + "#" + ctx.user.discriminator)
        await ctx.response.send_message(
            f"{self.user.username} is rank {self.user.ranking} with {self.user.ranking_points} ranking points."
        )

    @app_commands.command(name="ingame", description="Sets your in-game username")
    async def ingame(self, ctx, ingame_username: str):
        self.user.init_user(ctx.user.name + "#" + ctx.user.discriminator)
        self.user.add_ingame_username(ingame_username)
        await ctx.response.send_message(f"Your in-game username is now {ingame_username}.")
    
    @app_commands.command(name="stats", description="Shows your stats")
    async def stats(self, ctx):
        self.user.init_user(ctx.user.name + "#" + ctx.user.discriminator)
        await ctx.response.send_message(
            f"{self.user.username} has played {self.user.matches_played} matches, winning {self.user.matches_won}, losing {self.user.matches_lost} and abandoning {self.user.matches_abandoned}."
        )
    
    @app_commands.command(name="muliversus", description="Shows your Muliversus stats")
    async def muliversus(self, ctx):
        self.user.init_user(ctx.user.name + "#" + ctx.user.discriminator)
        await ctx.response.send_message(
            f"https://muliversus.plsergent.xyz/{self.user.in_game_username}"
        )
        