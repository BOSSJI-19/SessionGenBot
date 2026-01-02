from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import START_IMG, OWNER_ID, SUPPORT_CHAT

# --- SMALL CAPS FUNCTION ---
def to_small_caps(text):
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
        'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        ' ': ' '
    }
    return "".join(mapping.get(char.lower(), char) for char in text)

@Client.on_message(filters.command("start") & filters.private)
async def start_msg(bot, message: Message):
    user = message.from_user.first_name
    
    # Message Text
    raw_text = f"Hello {user}, Welcome to Session Generator Bot.\n\nSelect a library to generate string session."
    styled_text = to_small_caps(raw_text)

    # --- BUTTONS (Ab ye bhi Small Caps mai hain) ---
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴘʏʀᴏɢʀᴀᴍ", callback_data="gen_pyro"),
            InlineKeyboardButton("ᴛᴇʟᴇᴛʜᴏɴ", callback_data="gen_tele")
        ],
        [
            # Owner aur Support bhi design ke hisab se style kar diye
            InlineKeyboardButton("ᴏᴡɴᴇʀ 👑", url=f"tg://user?id={OWNER_ID}"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ 💬", url=SUPPORT_CHAT)
        ]
    ])

    if START_IMG:
        await message.reply_photo(photo=START_IMG, caption=styled_text, reply_markup=buttons)
    else:
        await message.reply_text(text=styled_text, reply_markup=buttons)
        
