from disnake.ext import commands, tasks
import youtube
from channel_registry import ChannelRegistry
from upload_watcher import UploadWatcher
import permissions
import channel_utils
import logger

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.registry = ChannelRegistry()
        self.watcher = UploadWatcher(self.registry)
        self.scheduled_check.start()
        self.logger = logger.get_instance()

    @commands.slash_command()
    @permissions.requires_administrator
    async def get_channel_updates(self, ctx, yt_channel_id, notification_channel=None, message=""):
    
        """
        Register for channel updates

        """
        
        if notification_channel is None:
            notification_channel = ctx.channel.id
        else:
            notification_channel = channel_utils.convert_to_int(notification_channel)
            if notification_channel == None:
               await ctx.send("Invalid notification channel")
               return
        self.registry.update(yt_channel_id, notification_channel, message)
        self.watcher.update()
        self.registry.save()
        await ctx.send("Registration successful!")
        
    @commands.slash_command()
    @permissions.requires_administrator
    async def stop_channel_updates(self, ctx, yt_channel_id, notification_channel=None):
    
        """
        Cancels channel updates
        
        """
    
        if notification_channel is None:
            for channel in ctx.guild.channels:
                self.registry.remove(yt_channel_id, channel.id)
        else:
            self.registry.remove(yt_channel_id, notification_channel)
        self.watcher.update()
        self.registry.save()
        await ctx.send("Removed registration!")
        
    #@commands.slash_command(description="youtube test")
    #async def yt_test(self, ctx):
    #    await ctx.send("youtube cog success")
    
    @tasks.loop(minutes=1.0)
    async def scheduled_check(self):
        updates = self.watcher.check_for_new_videos()
        if updates:
            logger.log_info("New video(s) uploaded!")
        for video_id in updates.keys():
            url = youtube.get_video_by_id(video_id)
            for entry in updates[video_id]: #post the notification_message in the notification_channel
                channel = self.bot.get_channel(entry['notification_channel'])
                message = entry['notification_message'] + "\n" + url
                await channel.send(message)
        