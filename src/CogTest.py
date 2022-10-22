class CogTest:
	def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="cog test")
    async def cog_test(self, ctx):
        await ctx.send("Cog success")
        