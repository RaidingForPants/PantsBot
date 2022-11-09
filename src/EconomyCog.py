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
    async def give_funds(self, ctx, member, amount):
        guild = ctx.guild.id
        member = channel_utils.convert_to_int(member)
        try:
            self.economy[guild].add_funds(member, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
            self.economy[guild].add_funds(member, amount)
            
        
    @commands.slash_command()
    @permissions.requires_administrator        
    async def take_funds(self, ctx, member, amount):
        guild = ctx.guild.id
        member = channel_utils.convert_to_int(member)
        try:
            self.economy[guild].remove_funds(member, amount)
        except KeyError:
            self.economy[guild] = GuildEconomy()
        except MoneyError:
            self.economy[guild].remove_all_funds(member)
            
        
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author.id
        try:
            economy_obj = self.economy[message.guild.id]
        except KeyError:
            self.economy[message.guild.id] = GuildEconomy()
        if member not in economy_obj.lock_list:  
            economy_obj.add_funds(member, 1)
            economy_obj.lock_user(member, duration=60)
        
        
class GuildEconomy:
    def __init__(self):
        self.bank = {}
        self.lock_list = set()
        
    def add_funds(self, member, amount):
        try:
            self.bank[member] += amount
        except KeyError:
            self.bank[member] = amount
        
    def remove_funds(self, member, amount):
        try:
            if self.bank[member] >= amount:
                self.bank[member] -= amount
            else:
                raise MoneyError("Not enough funds!")
        except KeyError:
            self.bank[member] = 0
            raise MoneyError("Not enough funds!")
            
    def remove_all_funds(self, member):
        self.bank[member] = 0
            
    def lock_user(self, member, duration=None):
        self.lock_list.add(member)
        if duration is not None:
            unlock = threading.Timer(duration, unlock_user, args=member)
            unlock.start()
        
    def unlock_user(self, member):
        self.lock_list.remove(member)
        
        
class MoneyError(Exception):
    pass