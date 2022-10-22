from disnake.ext import commands

class CogTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="cog test")
    async def my_test(self, ctx):
        await ctx.send("Cog success")
