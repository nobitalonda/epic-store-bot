from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = 25893261
API_HASH = "17034419f230472d0d1767da2f9cdd62"
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
ADMIN_ID = 6111910941

app = Client("epic_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# In-memory product store
products = {
    "Premium PFP": [],
    "Premium Text": [],
    "Premium CC": [],
    "Premium Watermark": [],
    "Topaz Setting": [],
    "AM Topaz CC": [],
    "Banner": [],
    "Free Material": []
}

# Start + channel join check
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join @reversereon", url="https://t.me/reversereon")],
        [InlineKeyboardButton("📢 Join @epic001re", url="https://t.me/epic001re")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="menu")]
    ])
    await message.reply("👋 Welcome to Epic Store!\n\nPlease join both channels to continue:", reply_markup=keyboard)

# Main Menu
@app.on_callback_query(filters.regex("menu"))
async def menu_callback(client, callback):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Premium PFP", callback_data="view:Premium PFP")],
        [InlineKeyboardButton("📝 Premium Text", callback_data="view:Premium Text")],
        [InlineKeyboardButton("💳 Premium CC", callback_data="view:Premium CC")],
        [InlineKeyboardButton("🔐 Premium Watermark", callback_data="view:Premium Watermark")],
        [InlineKeyboardButton("🎚 Topaz Setting", callback_data="view:Topaz Setting")],
        [InlineKeyboardButton("🌟 AM Topaz CC", callback_data="view:AM Topaz CC")],
        [InlineKeyboardButton("🖼 Banner", callback_data="view:Banner")],
        [InlineKeyboardButton("📦 Free Material", callback_data="view:Free Material")],
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/reonfx"),
            InlineKeyboardButton("👮 Admin", url="https://t.me/EpicAmz")
        ]
    ])
    await callback.message.edit("📦 *Main Menu*\nChoose a category:", reply_markup=keyboard)

# Admin-only /add command
@app.on_message(filters.command("add") & filters.photo)
async def add_product(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Only admin can add products.")
        return

    try:
        parts = message.caption.split(" ", 2)
        category = parts[0].strip('"')
        price = parts[1]
        title = parts[2]

        if category not in products:
            await message.reply("❌ Invalid category.")
            return

        image_id = message.photo.file_id

        products[category].append({
            "title": title,
            "price": price,
            "file_id": image_id
        })

        await message.reply(f"✅ Added to *{category}*\n• {title}\n• ₹{price}", parse_mode="Markdown")

    except Exception as e:
        await message.reply("⚠️ Format: `/add \"Category\" price title`\n(Send with image and caption)", quote=True)

# Category view (for public)
@app.on_callback_query(filters.regex("view:"))
async def view_category(client, callback):
    category = callback.data.split(":")[1]
    items = products.get(category, [])
    if not items:
        await callback.answer("🚫 No items yet!", show_alert=True)
        return

    for item in items:
        await callback.message.reply_photo(
            photo=item['file_id'],
            caption=f"📌 *{item['title']}*\n💸 Price: ₹{item['price']}",
            parse_mode="Markdown"
        )

# Back to menu shortcut (if needed)
@app.on_message(filters.command("menu"))
async def menu_cmd(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")]
    ])
    await message.reply("⬅️ Tap to return to menu", reply_markup=keyboard)

app.run()
                              
