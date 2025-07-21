from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

API_ID = 25893261
API_HASH = "17034419f230472d0d1767da2f9cdd62"
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
OWNER_ID = 6111910941

app = Client("store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type != "private":
        return

    buttons = [
        [InlineKeyboardButton("Join @reversereon", url="https://t.me/reversereon")],
        [InlineKeyboardButton("Join @epic001re", url="https://t.me/epic001re")],
        [
            InlineKeyboardButton("Premium PFP", callback_data="view_premium_pfp"),
            InlineKeyboardButton("Premium Text", callback_data="view_premium_text")
        ],
        [
            InlineKeyboardButton("Premium CC", callback_data="view_premium_cc"),
            InlineKeyboardButton("Premium Watermark", callback_data="view_premium_watermark")
        ],
        [
            InlineKeyboardButton("Topaz Setting", callback_data="view_topaz_setting"),
            InlineKeyboardButton("AM Topaz CC", callback_data="view_am_topaz_cc")
        ],
        [
            InlineKeyboardButton("Banner", callback_data="view_banner"),
            InlineKeyboardButton("Free Material", callback_data="view_free_material")
        ],
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/reonfx7"),
            InlineKeyboardButton("Admin", url="https://t.me/EpicAmz")
        ]
    ]
    await message.reply(
        "👋 Welcome to Epic Store!\n\nSelect a category below to explore products.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.command("add") & filters.private)
async def add_item(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only the owner can use this command.")

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("❗ Reply to a photo with this command.")

    try:
        if len(message.command) < 2:
            raise ValueError("Missing caption text.")
        caption = message.text.split(" ", 1)[1]
        category, title, price = [x.strip() for x in caption.split("|")]
        category_key = category.lower().replace(" ", "_")
    except:
        return await message.reply("❌ Format: `/add category | title | price` (reply to photo)", parse_mode="Markdown")

    file_id = message.reply_to_message.photo.file_id
    data = load_data()

    if category_key not in data:
        data[category_key] = []

    data[category_key].append({
        "file_id": file_id,
        "title": title,
        "price": price
    })

    save_data(data)
    await message.reply(f"✅ Added to `{category}`!", parse_mode="Markdown")

@app.on_callback_query()
async def view_category(client, callback_query):
    data = load_data()
    category_key = callback_query.data.replace("view_", "")
    items = data.get(category_key, [])

    if not items:
        return await callback_query.message.edit("❌ No items added yet.")

    media = items[-1]
    caption = f"**{media['title']}**\n💸 Price: {media['price']}"
    buttons = [
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    await callback_query.message.edit_text(
        text=caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

@app.on_callback_query(filters.regex("main_menu"))
async def back_home(client, callback_query):
    await start(client, callback_query.message)

app.run()
        
