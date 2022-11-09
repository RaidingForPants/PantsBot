"""
A cog for doing gambling stuff
"""

from disnake.ext import commands, tasks
import permissions
import logger

class GambleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
    
    @commands.slash_command()
    @permissions.requires_administrator
    async def gamble_enable(self, ctx):
        self.enabled = True
        await ctx.send("Gambling enabled")
        
    @commands.slash_command()
    @permissions.requires_administrator
    async def gamble_disable(self, ctx):
        self.enabled = False
        await ctx.send("Gambling disabled")
        