from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Wallet Addresses
BTC_ADDRESS = "bc1qkhczdqskrx57eh9mx0smr4ymavexhly3k3myna"
ETH_ADDRESS = "0x7f763ef4de908063f4f0917283f5a953de093b36"
USDT_ADDRESS = "0x7f763ef4de908063f4f0917283f5a953de093b36"

verified_users = set()  # In-memory (can connect to DB)

# Welcome / Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Rent for 1 Day - $100", callback_data='rent_day')],
        [InlineKeyboardButton("🏆 Rent for 1 Week - $500", callback_data='rent_week')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✨ *Welcome to BrainsClub Premium Bot!*\n\n"
        "🔐 This bot is designed for serious users only. We offer a fully automated, ultra-secure platform with industry-leading uptime.\n\n"
        "💼 *Usage Fees:*\n"
        "• 1 Day Access – `$100`\n"
        "• 1 Week Access – `$500`\n\n"
        "👇 Please choose your access plan to proceed.",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Payment Option
async def rent_option_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    rent_type = query.data
    price = "$100 for 1 Day" if rent_type == "rent_day" else "$500 for 1 Week"

    text = (
        f"💳 *You selected:* `{price}`\n\n"
        f"📩 Please send your payment to *one* of the addresses below:\n\n"
        f"🔸 *BTC:* `{BTC_ADDRESS}`\n"
        f"🔹 *ETH:* `{ETH_ADDRESS}`\n"
        f"🟡 *USDT (ERC20):* `{USDT_ADDRESS}`\n\n"
        "⚠️ *Important:* Use only the address provided. Once paid, click the button below to confirm."
    )
    
    keyboard = [[InlineKeyboardButton("✅ I've Sent the Payment", callback_data='confirm_payment')]]
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# Payment Confirmation
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    YOUR_ADMIN_ID = 7685837210

    await context.bot.send_message(
        chat_id=YOUR_ADMIN_ID,
        text=f"📬 *Payment Confirmation*\nUser ID: `{user_id}` has clicked confirm.\nUse /verify {user_id} after checking blockchain or transaction logs.",
        parse_mode="Markdown"
    )

    await query.answer()
    await query.edit_message_text(
        "✅ *Payment confirmation received!*\n\n"
        "🔎 Please wait while our team verifies your transaction.\n"
        "This usually takes a few minutes. You’ll be notified once approved.",
        parse_mode="Markdown"
    )

# Admin Command to Verify Payment
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    YOUR_ADMIN_ID = 7685837210
    if update.effective_user.id != YOUR_ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized access.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("📥 Usage: /verify <user_id>")
        return

    user_id = int(context.args[0])
    verified_users.add(user_id)

    await update.message.reply_text(f"✅ User `{user_id}` has been verified.", parse_mode="Markdown")
    await context.bot.send_message(
        chat_id=user_id,
        text="🎉 *Your payment has been verified!*\n\nYou now have access to premium features.\nUse `/pay` to begin.",
        parse_mode="Markdown"
    )

# /pay command
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in verified_users:
        await update.message.reply_text("💼 *Access Granted!*\n\nEnjoy full access to our premium bot services.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ You are not verified yet. Please complete your payment and wait for approval.")

# Main App
if __name__ == '__main__':
    app = ApplicationBuilder().token("7773486234:AAFQkq_9yWTaIcGEzxYzhP3mIZSS1Fe4oj0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verify", verify))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CallbackQueryHandler(rent_option_selected, pattern='^rent_'))
    app.add_handler(CallbackQueryHandler(confirm_payment, pattern='^confirm_payment$'))

    print("🟢 Bot is running...")
    app.run_polling()
