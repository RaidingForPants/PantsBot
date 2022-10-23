import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_REGISTRY_FILENAME = os.getenv('CHANNEL_REGISTRY_FILENAME')
API_KEY = os.getenv('API_KEY')
VIDEO_PREFIX = "https://www.youtube.com/watch?v="