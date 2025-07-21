from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json, os

API_ID = 25893261
API_HASH = "17034419f230472d0d1767da2f9cdd62"
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
OWNER_ID = 6111910941
REQUIRED_CHANNELS = ["@reversereon", "@epic001re"]

app = Client("epic_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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

async def check_subscription(user_id):
    try:
        for ch in REQUIRED_CHANNELS:
            member = await app.get_chat_member(ch, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        return True
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        buttons = [[InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch[1:]}")] for ch in REQUIRED_CHANNELS]
        await message.reply("🚫 Please join the required channels to use this bot.", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [
        [InlineKeyboardButton("Premium PFP", callback_data="view_premium_pfp"),
         InlineKeyboardButton("Premium Text", callback_data="view_premium_text")],
        [InlineKeyboardButton("Premium CC", callback_data="view_premium_cc"),
         InlineKeyboardButton("Premium Watermark", callback_data="view_premium_watermark")],
        [InlineKeyboardButton("Topaz Setting", callback_data="view_topaz_setting"),
         InlineKeyboardButton("AM Topaz CC", callback_data="view_am_topaz_cc")],
        [InlineKeyboardButton("Banner", callback_data="view_banner"),
         InlineKeyboardButton("Free Material", callback_data="view_free_material")],
        [InlineKeyboardButton("👑 Owner", url="https://t.me/reonfx7"),
         InlineKeyboardButton("👮‍♂️ Admin", url="https://t.me/EpicAmz")]
    ]
    await message.reply(
        "👋 Welcome to Epic Store!\n\nExplore premium items below:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.command("add") & filters.private)
async def add_item(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only the owner can use this command.")

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("❗Reply to a photo with this command.")

    try:
        parts = message.text.split(" ", 1)[1]
        category, title, price = [x.strip() for x in parts.split("|")]
        key = category.lower().replace(" ", "_")
    except:
        return await message.reply("❌ Format: `/add category | title | price`\n(Reply to image)", quote=True)

    file_id = message.reply_to_message.photo.file_id
    data = load_data()

    if key not in data:
        data[key] = []

    data[key].append({"file_id": file_id, "title": title, "price": price})
    save_data(data)
    await message.reply(f"✅ Added under `{category}`.")

@app.on_callback_query()
async def handle_cb(client, callback):
    data = load_data()
    cb_data = callback.data.replace("view_", "")
    items = data.get(cb_data, [])

    if not items:
        return await callback.message.edit("❌ No items in this category.")

    item = items[-1]
    caption = f"**{item['title']}**\n💰 Price: {item['price']}"
    buttons = [[
        InlineKeyboardButton("🔙 Back", callback_data="back"),
        InlineKeyboardButton("🏠 Menu", callback_data="main_menu")
    ]]
    await callback.message.edit_media(
        media=item["file_id"],
        reply_markup=InlineKeyboardMarkup(buttons),
        caption=caption
    )

@app.on_callback_query(filters.regex("back|main_menu"))
async def back_menu(client, callback):
    await start(client, callback.message)

app.run()
        
