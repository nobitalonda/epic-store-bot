from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = 25893261
API_HASH = "17034419f230472d0d1767da2f9cdd62"
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
ADMIN_ID = 6111910941

app = Client("epic_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start + Join check
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join @reversereon", url="https://t.me/reversereon")],
        [InlineKeyboardButton("📢 Join @epic001re", url="https://t.me/epic001re")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="menu")]
    ])
    await message.reply("👋 Welcome to Epic Store!\n\nPlease join both channels to continue:", reply_markup=keyboard)

# Show main menu
@app.on_callback_query(filters.regex("menu"))
async def menu_callback(client, callback):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Premium PFP", callback_data="premium_pfp")],
        [InlineKeyboardButton("📝 Premium Text", callback_data="premium_text")],
        [InlineKeyboardButton("💳 Premium CC", callback_data="premium_cc")],
        [InlineKeyboardButton("🔐 Premium Watermark", callback_data="premium_watermark")],
        [InlineKeyboardButton("🎚 Topaz Setting", callback_data="topaz")],
        [InlineKeyboardButton("🌟 AM Topaz CC", callback_data="amtopaz")],
        [InlineKeyboardButton("🖼 Banner", callback_data="banner")],
        [InlineKeyboardButton("📦 Free Material", callback_data="free")],
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/reonfx"),
            InlineKeyboardButton("👮 Admin", url="https://t.me/EpicAmz")
        ]
    ])
    await callback.message.edit("📦 *Main Menu*\nChoose a category:", reply_markup=keyboard)

# Premium PFP
@app.on_callback_query(filters.regex("premium_pfp"))
async def premium_pfp(client, callback):
    await callback.message.reply_photo(
        photo="https://telegra.ph/file/2b03ed21e60e3a227c013.jpg",  # replace with your image URL
        caption="💎 Premium PFP\n\n💰 Price: 30 stars",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])
    )

# Premium Text
@app.on_callback_query(filters.regex("premium_text"))
async def premium_text(client, callback):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Smooth bavel text", callback_data="smooth_bavel")],
        [InlineKeyboardButton("Premium glow text", callback_data="glow_text")],
        [InlineKeyboardButton("AE like text", callback_data="ae_text")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])
    await callback.message.edit("📝 Premium Text Options:", reply_markup=keyboard)

# Premium CC
@app.on_callback_query(filters.regex("premium_cc"))
async def premium_cc(client, callback):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Gaming cc", callback_data="gaming_cc")],
        [InlineKeyboardButton("Opium cc", callback_data="opium_cc")],
        [InlineKeyboardButton("By mistake cc", callback_data="mistake_cc")],
        [InlineKeyboardButton("Hammer cc", callback_data="hammer_cc")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])
    await callback.message.edit("💳 Premium CC Options:", reply_markup=keyboard)

# Other placeholders
@app.on_callback_query(filters.regex(".*"))
async def handle_others(client, callback):
    await callback.answer("🚧 Coming Soon or Not Configured!", show_alert=True)

app.run()
    
