import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_REGISTRY_FILENAME = os.getenv('CHANNEL_REGISTRY_FILENAME')
API_KEY = os.getenv('API_KEY')
VIDEO_PREFIX = "https://www.youtube.com/watch?v="
ERROR_FILENAME_PREFIX = "logs/error_log-"
LOG_FILENAME_PREFIX = "logs/log-"
ERROR_FILENAME = "logs/error_log.txt"
LOG_FILENAME = "logs/log.txt"