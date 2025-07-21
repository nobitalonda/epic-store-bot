from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

API_ID = 25893261
API_HASH = "17034419f230472d0d1767da2f9cdd62"
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
OWNER_ID = 6111910941  # @reonfx7

bot = Client("store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def save_product(category, title, price, file_id, file_type):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if category not in data:
        data[category] = []

    data[category].append({
        "title": title,
        "price": price,
        "file_id": file_id,
        "type": file_type
    })

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@bot.on_message(filters.command("add") & filters.reply)
def add_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return message.reply("❌ Only the Owner can add products!")

    try:
        parts = message.text.split(" ", 1)[1].split("|")
        category = parts[0].strip().lower()
        title = parts[1].strip()
        price = parts[2].strip()

        reply = message.reply_to_message
        if reply.photo:
            file_id = reply.photo.file_id
            file_type = "photo"
        elif reply.document:
            file_id = reply.document.file_id
            file_type = "document"
        else:
            return message.reply("❌ Please reply to an image or file.")

        save_product(category, title, price, file_id, file_type)
        message.reply(f"✅ Product added in '{category}'!\n\n**{title}** - {price}")

    except Exception as e:
        message.reply(f"❌ Error: Format galat hai.\nUse: `/add category | title | price`", quote=True)

@bot.on_message(filters.command("view"))
def view_category(client, message):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    keyboard = []
    for cat in data.keys():
        keyboard.append([InlineKeyboardButton(cat.title(), callback_data=f"view_{cat}")])

    message.reply("📁 Select a category:", reply_markup=InlineKeyboardMarkup(keyboard))

@bot.on_callback_query()
def handle_callback(client, callback_query):
    data = callback_query.data
    if data.startswith("view_"):
        category = data.replace("view_", "")
        with open(DATA_FILE, "r") as f:
            db = json.load(f)

        if category not in db:
            return callback_query.message.edit("❌ Category not found.")

        for item in db[category]:
            caption = f"**{item['title']}**\n💰 Price: {item['price']}"
            if item["type"] == "photo":
                client.send_photo(callback_query.message.chat.id, item["file_id"], caption=caption)
            elif item["type"] == "document":
                client.send_document(callback_query.message.chat.id, item["file_id"], caption=caption)

        callback_query.answer()

bot.run()
              
