from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHANNEL_REGISTRY_FILENAME = os.getenv('CHANNEL_REGISTRY_FILENAME')
VIDEO_PREFIX = "https://www.youtube.com/watch?v="
channel_registry = None
recent_video_ids = None

def init_channel_registry():
    global channel_registry, recent_video_ids
    channel_registry = {}
    
def save_channel_registry():
    global channel_registry
    with open(CHANNEL_REGISTRY_FILENAME, "w") as f:
        json.dump(channel_registry, f)
        
def update_channel_registry(channelId, notification_channel, message):
    global channel_registry, recent_video_ids
    if not channelId in channel_registry.keys():
        channel_registry[channelId] = []
    #check if the notification channel has already been entered:
    already_entered = False
    for entry in channel_registry[channelId]:
        if entry['notification_channel'] == notification_channel:
            already_entered = True
            entry['notification_message'] = message
            break
    if not already_entered:
        new_entry = {}
        new_entry['notification_channel'] = notification_channel
        new_entry['notification_message'] = message
        channel_registry[channelId].append(new_entry)
        recent_video_ids[channelId] = _get_most_recent_video(channelId)
    
def load_recent_video_ids():
    global recent_video_ids, channel_registry
    recent_video_ids = {}
    for channelId in channel_registry.keys():
        recent_video_ids[channelId] = _get_most_recent_video(channelId)
        
def check_for_new_videos():
    global channel_registry, recent_video_ids
    updates = {}
    for channelId in channel_registry.keys(): #check each channel
        video_id = _get_most_recent_video(channelId) #for the most recent video
        if video_id != recent_video_ids[channelId]: #if it's a different video
            channels = []
            for entry in channel_registry[channelId]: #collate every channel 
                channels.append(entry)
            updates[video_id] = channels
    return updates
                

def init():
    global channel_registry
    try:
        with open(CHANNEL_REGISTRY_FILENAME, 'r') as f:
            channel_registry = json.load(f)
    except FileNotFoundError:
        init_channel_registry()
    load_recent_video_ids()

def _send_request(url):
    response = requests.get(url)
    json_response = json.loads(response.text)
    return json_response

def _list_channel_activity(channelId):
    return _send_request(f"https://youtube.googleapis.com/youtube/v3/activities?part=contentDetails&channelId={channelId}&maxResults=25&key={API_KEY}")
    
    
def _get_video_by_id(video_id):
    return VIDEO_PREFIX + video_id
    
def _get_most_recent_video(channelId):
    response = _list_channel_activity(channelId)
    for item in response['items']:
        try:
            video_id = item['contentDetails']['upload']['videoId']
            return video_id
        except:
            #didn't find a video, go to next item
            pass
    
    
init()