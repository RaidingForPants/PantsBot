from disnake.ext import commands
from dotenv import load_dotenv
import json
import os
import requests
import YoutubeAPI

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register for channel updates")
    async def get_channel_updates(self, ctx, yt_channel_id, notification_channel=None):
        if notification_channel is None:
            notification_channel = ctx.channel.id
        #check if yt_channel_id is valid
        YoutubeAPI.update_channel_registry(channel_id, notification_channel)
        YoutubeAPI.save_channel_registry()
        await ctx.send("Registration successful!")
        
    @commands.slash_command(description="youtube test")
    async def yt_test(self, ctx):
        await ctx.send("youtube cog success")