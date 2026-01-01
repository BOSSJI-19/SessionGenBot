import asyncio
import os
from threading import Thread
from flask import Flask  # ✅ Flask Import kiya
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
import pyromod

# =========================================
# 🔥 FAKE WEB SERVER (ALIVE RAKHNE KE LIYE)
# =========================================

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "<h1>Session Generator Bot is Running 24/7! 🚀</h1>"

def run_flask():
    # Render/Heroku dynamic port deta hai, isliye os.environ use kiya
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# =========================================
# 🤖 MAIN BOT LOGIC
# =========================================

# Plugins folder define kiya
plugins = dict(root="plugins")

# Bot Client
app = Client(
    "SessionGen",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins
)

async def start_bot():
    print("🚀 Starting Session Generator Bot...")
    await app.start()
    me = await app.get_me()
    print(f"✅ Bot is Online! @{me.username}")
    await idle()
    await app.stop()

if __name__ == "__main__":
    # 🔥 Sabse pehle Fake Server start karo
    keep_alive()
    print("✅ Fake Web Server Started!")
    
    # Fir Bot start karo
    app.run(start_bot())
    
