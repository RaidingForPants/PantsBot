from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHANNEL_REGISTRY_FILENAME = os.getenv('CHANNEL_REGISTRY_FILENAME')
VIDEO_PREFIX = "https://www.youtube.com/watch?v="
channel_registry = None

def init_channel_registry():
    global channel_registry
    channel_registry = {}
    channel_registry['channels'] = {}
    
def save_channel_registry():
    global channel_registry
    with open(CHANNEL_REGISTRY_FILENAME, "w") as f:
        json.dump(channel_registry, f)
        
def update_channel_registry(channelId, notification_channel):
    global channel_registry
    channel_registry['channels'][notification_channel] = channelId

def init():
    global channel_registry
    try:
        with open(CHANNEL_REGISTRY_FILENAME, 'r') as f:
            channel_registry = json.load(f)
        print(channel_registry)
    except FileNotFoundError:
        init_channel_registry()

def _send_request(url):
    response = requests.get(url)
    json_response = json.loads(response.text)
    return json_response

def _list_channel_activity(channelId):
    return _send_request(f"https://youtube.googleapis.com/youtube/v3/activities?part=contentDetails&channelId={channelId}&maxResults=25&key={API_KEY}")
    
    
def _get_video_by_id(video_id):
    return VIDEO_PREFIX + video_id
    
def _get_most_recent_video(channelId):
    response = list_channel_activity(channelId)
    for item in response['items']:
        try:
            video_id = item['contentDetails']['upload']['videoId']
            return _get_video_by_id(video_id)
        except:
            #didn't find a video, go to next item
            pass
    
    
init()