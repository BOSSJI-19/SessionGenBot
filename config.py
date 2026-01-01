import os

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "your_hash_here")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

# Log Group ID (Integer hona chahiye, -100 se start hota hai usually)
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "-100123456789"))

# Welcome Photo
START_IMG = os.environ.get("START_IMG", "https://i.ibb.co/TMsyF7sQ/images-1.jpg")

