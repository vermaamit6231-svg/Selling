from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from database.models import User, db
from config import BOT_TOKEN
from backend.payment import create_deposit

menu = ReplyKeyboardMarkup([
    ["🛍 Browse Services"],
    ["💰 My Wallet", "➕ Deposit"],
    ["📦 My Orders", "💬 Contact Support"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id, balance=0)
        db.add(user)
        db.commit()

    await update.message.reply_text(
        f"Welcome!\n💰 Wallet: ₹{user.balance}",
        reply_markup=menu
    )

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.query(User).filter_by(user_id=update.effective_user.id).first()
    await update.message.reply_text(f"💰 Balance: ₹{user.balance}")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order = create_deposit(update.effective_user.id, 100)
    await update.message.reply_text(
        f"Pay ₹100\nUPI QR / Razorpay Link:\nhttps://rzp.io/i/{order['id']}"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("My Wallet"), wallet))
app.add_handler(MessageHandler(filters.Regex("Deposit"), deposit))

app.run_polling()
