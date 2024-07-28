from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
TOKEN = '7472129592:AAFFqjqnXNITuLHhzeIcIURf8pHmbVnoUQY'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    user = update.message.from_user
    await update.message.reply_text(f"أهلاً وسهلاً {user.first_name}!")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
