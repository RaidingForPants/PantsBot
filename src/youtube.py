import json
import requests
import environment

def _send_request(url):
    response = requests.get(url)
    json_response = json.loads(response.text)
    return json_response

def list_channel_activity(channelId):
    return _send_request(f"https://youtube.googleapis.com/youtube/v3/activities?part=contentDetails&channelId={channelId}&maxResults=25&key={environment.API_KEY}")
    
    
def get_video_by_id(video_id):
    return environment.VIDEO_PREFIX + video_id
    
def get_most_recent_video(channelId):
    response = list_channel_activity(channelId)
    for item in response['items']:
        try:
            video_id = item['contentDetails']['upload']['videoId']
            return video_id
        except:
            #didn't find a video, go to next item
            pass