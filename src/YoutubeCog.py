from disnake.ext import commands, tasks
import youtube
from channel_registry import ChannelRegistry
from upload_watcher import UploadWatcher

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.registry = ChannelRegistry()
        self.watcher = UploadWatcher(self.registry)
        self.scheduled_check.start()

    @commands.slash_command(description="Register for channel updates")
    async def get_channel_updates(self, ctx, yt_channel_id, notification_channel=None, message=""):
        if notification_channel is None:
            notification_channel = ctx.channel.id
        self.registry.update(yt_channel_id, notification_channel, message)
        self.registry.save()
        await ctx.send("Registration successful!")
        
    @commands.slash_command(description="Cancel channel updates")
    async def stop_channel_updates(self, ctx, yt_channel_id, notification_channel=None):
        if notification_channel is None:
            for channel in ctx.guild.channels:
                self.registry.remove(yt_channel_id, channel.id) 
        else:
            self.registry.remove(yt_channel_id, notification_channel)
        self.registry.save()
        await ctx.send("Removed registration!")
        
    @commands.slash_command(description="youtube test")
    async def yt_test(self, ctx):
        await ctx.send("youtube cog success")
    
    @tasks.loop(minutes=60.0)
    async def scheduled_check(self):
        updates = self.watcher.check_for_new_videos()
        print(updates)
        for video_id in updates.keys():
            url = youtube.get_video_by_id(video_id)
            for entry in updates[video_id]: #post the notification_message in the notification_channel
                channel = bot.get_channel(entry['notification_channel'])
                message = entry['notification_message'] + "\n" + url
                await channel.send(message)
        