from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 🔐 Tera token aur admin ID yahan set kiya hai
BOT_TOKEN = "8084124965:AAGWr03hVIejWDThbqe9oeTof8hKK93qMIc"
ADMIN_ID = 6111910941

# 🛒 Store items will be stored here temporarily (in memory)
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

# 📋 Main Menu layout
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Premium PFP", callback_data="cat:Premium PFP")],
        [InlineKeyboardButton("Premium Text", callback_data="cat:Premium Text")],
        [InlineKeyboardButton("Premium CC", callback_data="cat:Premium CC")],
        [InlineKeyboardButton("Premium Watermark", callback_data="cat:Premium Watermark")],
        [InlineKeyboardButton("Topaz Setting", callback_data="cat:Topaz Setting")],
        [InlineKeyboardButton("AM Topaz CC", callback_data="cat:AM Topaz CC")],
        [InlineKeyboardButton("Banner", callback_data="cat:Banner")],
        [InlineKeyboardButton("Free Material", callback_data="cat:Free Material")],
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/reonfx"),
            InlineKeyboardButton("🛠️ Admin", url="https://t.me/EpicAmz")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔗 Join @reversereon", url="https://t.me/reversereon")],
        [InlineKeyboardButton("🔗 Join @epic001re", url="https://t.me/epic001re")],
        [InlineKeyboardButton("✅ Done", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hey {user.mention_html()}! 👋\n\nWelcome to *Epic Store*.\nPlease join the channels below to access the store menu.",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# 📂 Menu handler
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📦 *Main Menu* — Choose a category:", parse_mode="Markdown", reply_markup=main_menu())

# 🔍 Category display handler
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category = query.data.split(":")
    items = products.get(category, [])
    if not items:
        await query.edit_message_text(f"🚫 No items in {category} yet.", reply_markup=back_menu())
        return
    first = items[0]
    caption = f"📌 *{first['title']}*\n💸 Price: {first['price']}"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    await query.edit_message_media(InputMediaPhoto(media=first['image_url'], caption=caption, parse_mode="Markdown"))
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

# ⬅️ Back button layout
def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu")]])

# ➕ /add command (Admin only)
async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Only admin can use this.")
        return
    try:
        if not context.args or len(context.args) < 3:
            await update.message.reply_text("❗ Usage: /add [Category] [Price] [Title] (send with image)")
            return
        category = context.args[0]
        price = context.args[1]
        title = " ".join(context.args[2:])
        if category not in products:
            await update.message.reply_text("❌ Invalid category.")
            return
        if not update.message.photo:
            await update.message.reply_text("📸 Please send this command with a product image.")
            return
        image_file = await update.message.photo[-1].get_file()
        image_url = image_file.file_path
        products[category].append({
            "title": title,
            "price": price,
            "image_url": image_url
        })
        await update.message.reply_text(f"✅ Added to *{category}*:\n• {title}\n• Price: {price}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# 🧠 Main function to run the bot
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_handler))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat:"))
    print("Bot started successfully.")
    app.run_polling()
