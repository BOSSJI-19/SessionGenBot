import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
import pyromod  # 🔥 IMPORTANT: Ye bot.ask() feature deta hai

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
    app.run(start_bot())
  
