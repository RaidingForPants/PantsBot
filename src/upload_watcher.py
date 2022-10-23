import youtube
import channel_registry

class UploadWatcher:

    def load_recent_video_ids(self):
        for channelId in self.channel_registry.get_channels():
            self.recent_video_ids[channelId] = youtube.get_most_recent_video(channelId)
            
    def check_for_new_videos(self):
        updates = {}
        print(self.recent_video_ids)
        for channel in self.channel_registry.get_channels(): #check each channel
            video_id = youtube.get_most_recent_video(channel) #for the most recent video
            print(video_id)
            if video_id != self.recent_video_ids[channel]: #if it's a different video
                print("New video uploaded!")
                channels = []
                for entry in self.channel_registry.get_entries(channel): #collate every entry for that channel 
                    channels.append(entry)
                updates[video_id] = channels
                self.recent_video_ids[channel] = video_id
        return updates
        
    def __init__(self, channel_registry):
        self.recent_video_ids = {}
        self.channel_registry = channel_registry
        self.load_recent_video_ids()