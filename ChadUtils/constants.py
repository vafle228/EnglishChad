import os

# AWS constants
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "eu-central-1"

# Telegram constants
API_KEY = os.getenv("API_KEY")
API_REQUEST = f"https://api.telegram.org/file/bot{API_KEY}/"

# Bot constants
TEMP_ROOT = "tmp/{0}"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
ENTRY_PER_PAGE = 5

