"""
A cog for doing gambling stuff
"""

from disnake.ext import commands, tasks
import permissions
import logger
import random
import command_utils

class GambleCog(commands.Cog):

    winning_multiplier = 1.9
    
    def __init__(self, bot):
        self.bot = bot
        self.disabled_list = set()
    
    @commands.slash_command()
    @permissions.requires_administrator
    async def gamble_enable(self, ctx):
        """
        Enables the gambling function
        """
        self.disabled_list.remove(ctx.guild.id)
        await ctx.send("Gambling enabled")
        
    @commands.slash_command()
    @permissions.requires_administrator
    async def gamble_disable(self, ctx):
        """
        Disables the gambling function
        """
        self.disabled_list.add(ctx.guild.id)
        await ctx.send("Gambling disabled")
        
        
    @commands.slash_command()
    @command_utils.toggle_command
    async def gamble(self, ctx, amount: int):
        """
        Risk your hard-earned munnies to win big!
        
        Parameters
        ----------
        amount: :class:`int`
            The amount of money to wager
        """
        economy = self.bot.get_cog("EconomyCog")
        if economy is not None:
            money = economy._get_funds(ctx.guild.id, ctx.author.id)
            if amount > money:
                await ctx.send("You don't have enough munnie")
            else:
                economy._take_funds(ctx.guild.id, ctx.author.id, amount)
                if random.randint(0, 1) == 1:
                    economy._give_funds(ctx.guild.id, ctx.author.id, self._round_up(amount*GambleCog.winning_multiplier))
                    await ctx.send(f"{ctx.author.name} wins! {self._round_up(amount*(GambleCog.winning_multiplier-1))} munnies have been added to their account")
                else:
                    if economy._get_funds(ctx.guild.id, ctx.author.id) == 0:
                        await ctx.send(f"{ctx.author.name} lost all {amount} of their munnies gambling!")
                    else:
                        await ctx.send(f"{ctx.author.name} lost {amount} munnies. Better luck next time!")
                        
                        
    def _round_up(self, number):
        if number >= int(number) + 0.5:
            return int(number) + 1
        else:
            return int(number)
                    