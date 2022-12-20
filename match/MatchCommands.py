from discord import app_commands


@app_commands.guild_only()
class Match(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @app_commands.command(name="start", description="Start a match")
    async def start(self, ctx):
        await ctx.response.send_message("Match started!")