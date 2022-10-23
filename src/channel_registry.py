import json
import environment

class ChannelRegistry:

    def init_channel_registry(self):
        try:
            with open(environment.CHANNEL_REGISTRY_FILENAME, 'r') as f:
                self.channel_registry = json.load(f)
        except FileNotFoundError:
            self.channel_registry = {}
        
    def save(self):
        with open(environment.CHANNEL_REGISTRY_FILENAME, "w") as f:
            json.dump(self.channel_registry, f)
            
    def update(self, channelId, notification_channel, message):
        if not channelId in self.channel_registry.keys():
            self.channel_registry[channelId] = []
        #check if the notification channel has already been entered:
        already_entered = False
        for entry in self.channel_registry[channelId]:
            if entry['notification_channel'] == notification_channel:
                already_entered = True
                entry['notification_message'] = message
                break
        if not already_entered:
            new_entry = {}
            new_entry['notification_channel'] = notification_channel
            new_entry['notification_message'] = message
            self.channel_registry[channelId].append(new_entry)
            
    def remove(self, channelId, notification_channel):
        try:
            for entry in self.channel_registry[channelId]:
                if entry['notification_channel'] == notification_channel:
                    self.channel_registry[channelId].remove(entry)
                    if len(self.channel_registry[channelId]) == 0:
                        del self.channel_registry[channelId]
                    break
        except Exception as err:
            print(err)

    def get_channels(self):
        return self.channel_registry.keys()
        
    def get_entries(self, channel):
        return self.channel_registry[channel]

    def __init__(self):
        self.init_channel_registry()