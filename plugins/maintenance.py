from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import OWNER_ID

# --- VARIABLES ---
MAINTENANCE_MODE = False

# Default Message (Small Caps mein)
DEFAULT_MSG = "sᴏʀʀʏ, ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
CURRENT_MSG = DEFAULT_MSG

# --- FONT CONVERTER FUNCTION ---
def make_small_caps(text):
    # Normal text ko Small Caps mai badalne ka map
    mapping = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz", 
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    )
    return text.lower().translate(mapping)

# --- 1. GATEKEEPER (USER BLOCKER) ---
@Client.on_message(filters.incoming & ~filters.user(OWNER_ID), group=-1)
async def maintenance_gatekeeper(bot, message: Message):
    global MAINTENANCE_MODE, CURRENT_MSG
    
    if MAINTENANCE_MODE:
        # Simple Message bhejayega (Bina Header ke)
        await message.reply_text(f"**{CURRENT_MSG}**")
        message.stop_propagation()

@Client.on_callback_query(~filters.user(OWNER_ID), group=-1)
async def maintenance_callback_gatekeeper(bot, query: CallbackQuery):
    global MAINTENANCE_MODE
    
    if MAINTENANCE_MODE:
        await query.answer("sᴏʀʀʏ, ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ɪs ᴏɴ!", show_alert=True)
        query.stop_propagation()

# --- 2. ADMIN COMMANDS ---
@Client.on_message(filters.command("maintenance") & filters.user(OWNER_ID))
async def maintenance_command(bot, message: Message):
    global MAINTENANCE_MODE, CURRENT_MSG, DEFAULT_MSG
    
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **Format:**\n"
            "`/maintenance on`\n"
            "`/maintenance on [Custom Message]`\n"
            "`/maintenance off`"
        )
    
    action = message.command[1].lower()
    
    if action == "on":
        MAINTENANCE_MODE = True
        
        # Agar custom message diya hai to usko Small Caps mai convert karo
        if len(message.command) > 2:
            raw_text = message.text.split(None, 2)[2]
            CURRENT_MSG = make_small_caps(raw_text)
        else:
            CURRENT_MSG = DEFAULT_MSG
            
        await message.reply_text(f"✅ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴏɴ!**\n\n💬 **Msg:** {CURRENT_MSG}")
        
    elif action == "off":
        MAINTENANCE_MODE = False
        await message.reply_text("✅ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴏꜰꜰ!**")
        
    else:
        await message.reply_text("❌ Use `on` or `off`.")
      
