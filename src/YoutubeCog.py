from disnake.ext import commands, tasks
from dotenv import load_dotenv
import json
import os
import requests
import YoutubeAPI

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_check.start()

    @commands.slash_command(description="Register for channel updates")
    async def get_channel_updates(self, ctx, yt_channel_id, notification_channel=None, message=""):
        if notification_channel is None:
            notification_channel = ctx.channel.id
        #check if yt_channel_id is valid
        YoutubeAPI.update_channel_registry(yt_channel_id, notification_channel, message)
        YoutubeAPI.save_channel_registry()
        await ctx.send("Registration successful!")
        
    @commands.slash_command(description="youtube test")
    async def yt_test(self, ctx):
        await ctx.send("youtube cog success")
    
    @tasks.loop(minutes=1.0)
    async def scheduled_check(self):
        updates = YoutubeAPI.check_for_new_videos()
        print(updates)
        for video_id in updates.keys():
            url = YoutubeAPI._get_video_by_id()
            for registration in updates[video_id]: #post the notification_message in the notification_channel
                channel = bot.get_channel(registration['notification_channel'])
                message = registration['notification_message'] + "\n" + url
                await channel.send(message)
        