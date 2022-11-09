"""
A cog for giving people fake money
"""

from disnake.ext import commands, tasks
import permissions
import logger
import threading
import channel_utils

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.economy = {}
    
    @commands.slash_command()
    @permissions.requires_administrator
    async def economy_enable(self, ctx):
        self.enabled = True
        await ctx.send("Economy enabled")
        
    @commands.slash_command()
    @permissions.requires_administrator
    async def economy_disable(self, ctx):
        self.enabled = False
        await ctx.send("Economy disabled")
    
    @commands.slash_command()
    @permissions.requires_administrator    
    async def give_funds(self, ctx, member, amount: int):
        guild = ctx.guild.id
        member = channel_utils.convert_to_int(member)
        temp = await self.bot.fetch_user(member)
        name = temp.name
        self._give_funds(guild, member, amount)
        await ctx.send(f"Gave {name} {amount} munnies")
            
        
    @commands.slash_command()
    @permissions.requires_administrator        
    async def take_funds(self, ctx, member, amount: int):
        guild = ctx.guild.id
        member = channel_utils.convert_to_int(member)
        temp = await self.bot.fetch_user(member)
        name = temp.name
        try:
            self._take_funds(guild, member, amount)
        except MoneyError:
            self.economy[guild].remove_all_funds(member)
        await ctx.send(f"Took {amount} munnies from {name}")
    
    @commands.slash_command()
    async def show_funds(self, ctx):
        guild = ctx.guild.id
        member = ctx.author.id
        val = self._get_funds(guild, member)
        await ctx.send(f"You have {val} munnies")
        
    def _take_funds(self, guild, member, amount: int):
        member = channel_utils.convert_to_int(member)
        try:
            self.economy[guild].remove_funds(member, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
            
    def _give_funds(self, guild, member, amount: int):
        member = channel_utils.convert_to_int(member)
        try:
            self.economy[guild].add_funds(member, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
            self.economy[guild].add_funds(member, amount)
            
    def _get_funds(self, guild, member):
        member = channel_utils.convert_to_int(member)
        try:
            retval = self.economy[guild].get_funds(member)
            return retval
        except KeyError:
            self.economy[guild] = GuildEconomy()
            return 0
        
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author.id
        guild = message.guild.id
        try:
            economy_obj = self.economy[guild]
        except KeyError:
            self.economy[guild] = GuildEconomy()
            economy_obj = self.economy[guild]
        if member not in economy_obj.lock_list:  
            economy_obj.add_funds(member, 1)
            economy_obj.lock_user(member, duration=60)
        
        
class GuildEconomy:
    def __init__(self):
        self.bank = {}
        self.lock_list = set()
        
    def add_funds(self, member, amount: int):
        try:
            self.bank[member] += amount
        except KeyError:
            self.bank[member] = amount
        
    def remove_funds(self, member, amount: int):
        try:
            if self.bank[member] >= amount:
                self.bank[member] -= amount
            else:
                raise MoneyError("Not enough funds!")
        except KeyError:
            self.bank[member] = 0
            raise MoneyError("Not enough funds!")
            
    def get_funds(self, member):
        try:
            retval = self.bank[member]
            return retval
        except KeyError:
            self.bank[member] = 0
            return 0
            
    def remove_all_funds(self, member):
        self.bank[member] = 0
        
    def unlock_user(self, member):
        self.lock_list.remove(member)
            
    def lock_user(self, member, duration=None):
        self.lock_list.add(member)
        if duration is not None:
            unlock = threading.Timer(duration, self.unlock_user, args=(member,))
            unlock.start()
        
class MoneyError(Exception):
    pass