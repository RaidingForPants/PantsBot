"""
A cog for giving people fake money
"""

from disnake.ext import commands, tasks
import permissions
import logger
import threading
import channel_utils
import command_utils

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disabled_list = set()
        self.economy = {}
    
    @commands.slash_command()
    @permissions.requires_administrator
    async def economy_enable(self, ctx):
        """
        Enables the munnie economy
        """
        self.disabled_list.remove(ctx.guild.id)
        await ctx.send("Economy enabled")
        
    @commands.slash_command()
    @permissions.requires_administrator
    async def economy_disable(self, ctx):
        """
        Disables the munnie economy
        """
        self.disabled_list.add(ctx.guild.id)
        await ctx.send("Economy disabled")
    
    @commands.slash_command()
    @command_utils.toggle_command
    @permissions.requires_administrator    
    async def give_munnies(self, ctx, user, amount: int):
        """
        Gives munnies to the specified user
        """
        
        
        guild = ctx.guild.id
        user = channel_utils.convert_to_int(user)
        temp = await self.bot.fetch_user(user)
        name = temp.name
        
        
        self._give_funds(guild, user, amount)
        await ctx.send(f"Gave {name} {amount} munnies")
            
        
    @commands.slash_command()
    @command_utils.toggle_command
    @permissions.requires_administrator        
    async def take_munnies(self, ctx, user, amount: int):
        """
        Takes munnies from the specified user
        """
        
        
        guild = ctx.guild.id
        user = channel_utils.convert_to_int(user)
        temp = await self.bot.fetch_user(user)
        name = temp.name
        
        
        try:
            self._take_funds(guild, user, amount)
        except MoneyError:
            self.economy[guild].remove_all_funds(user)
        await ctx.send(f"Took {amount} munnies from {name}")
    
    @commands.slash_command()
    @command_utils.toggle_command
    async def show_munnies(self, ctx):
        """
        Shows your current amount of munnies
        """
        
        
        guild = ctx.guild.id
        user = ctx.author.id
        
        
        val = self._get_funds(guild, user)
        await ctx.send(f"You have {val} munnies")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id not in self.disabled_list:
            user = message.author.id
            guild = message.guild.id
            try:
                economy_obj = self.economy[guild]
            except KeyError:
                self.economy[guild] = GuildEconomy()
                economy_obj = self.economy[guild]
            if user not in economy_obj.lock_list:  
                economy_obj.add_funds(user, 1)
                economy_obj.lock_user(user, duration=60)
            
            
    def _take_funds(self, guild, user, amount: int):
        user = channel_utils.convert_to_int(user)
        try:
            self.economy[guild].remove_funds(user, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
    
    def _give_funds(self, guild, user, amount: int):
        user = channel_utils.convert_to_int(user)
        try:
            self.economy[guild].add_funds(user, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
            self.economy[guild].add_funds(user, amount)

    def _get_funds(self, guild, user):
        user = channel_utils.convert_to_int(user)
        try:
            retval = self.economy[guild].get_funds(user)
            return retval
        except KeyError:
            self.economy[guild] = GuildEconomy()
            return 0
        
        
class GuildEconomy:
    def __init__(self):
        self.bank = {}
        self.lock_list = set()
        
    def add_funds(self, user, amount: int):
        try:
            self.bank[user] += amount
        except KeyError:
            self.bank[user] = amount
        
    def remove_funds(self, user, amount: int):
        try:
            if self.bank[user] >= amount:
                self.bank[user] -= amount
            else:
                raise MoneyError("Not enough munnies!")
        except KeyError:
            self.bank[user] = 0
            raise MoneyError("Not enough munnies!")
            
    def get_funds(self, user):
        try:
            retval = self.bank[user]
            return retval
        except KeyError:
            self.bank[user] = 0
            return 0
            
    def remove_all_funds(self, user):
        self.bank[user] = 0
        
    def unlock_user(self, user):
        self.lock_list.remove(user)
            
    def lock_user(self, user, duration=None):
        self.lock_list.add(user)
        if duration is not None:
            unlock = threading.Timer(duration, self.unlock_user, args=(user,))
            unlock.start()
        
class MoneyError(Exception):
    pass
    
