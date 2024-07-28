from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# دالة الرد على الأمر /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبا! أرسل "السلام عليكم" لأرد عليك.')

# دالة للرد على رسالة "السلام عليكم"
def reply_to_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "السلام عليكم":
        update.message.reply_text("وعليكم السلام")

def main():
    # استبدل 'YOUR_BOT_TOKEN' برمز التوكن الخاص بالبوت الذي حصلت عليه من BotFather
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    
    # الحصول على الموزع
    dp = updater.dispatcher

    # إضافة معالجات الأوامر
    dp.add_handler(CommandHandler("start", start))

    # إضافة معالج للرسائل العادية
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_message))

    # بدء البوت
    updater.start_polling()

    # الانتظار حتى يتم إيقاف البوت يدويا
    updater.idle()

if __name__ == '__main__':
    main()
