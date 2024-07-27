import os
import logging
import time
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from telegram.error import TelegramError

# إعدادات البوت
TOKEN = '7472129592:AAFFqjqnXNITuLHhzeIcIURf8pHmbVnoUQY'
INSTANT_PAYMENT_ADDRESS = "mobander@instapay"
VODAFONE_CASH = "01007265599"

# تعريف متغير رقم المستخدم
USER_ID = None
USER_CHAT_ID = None

# رسائل مختلفة
MESSAGE_ABOUT_ARAB_TECHNO = (
    "معاك البوت الرسمي الخاص ب عرب تكنو ستور🤖\n\n"
    "مرحبا في عالم عرب تكنو❤️🌍\n\n"
    "اتمنى تكون مشترك معانا ف الديسكورد\n"
    "https://discord.com/invite/VAUxAtn8qn\n\n"
    "ولو متعرفش دة الاستور الخاص ب أسوو - ASSO \n"
    "وقناة عرب تكنو\n\n"
    "ودي صفحه الانستا بتاعنا تابعنا علشان تعرف كل الاخبار\n"
    "https://www.instagram.com/asso.altorky\n\n"
    "ودي قناة اليوتيوب\n"
    "https://www.youtube.com/c/3rabtechno\n\n"
    "دة التيك توك\n"
    "https://www.tiktok.com/@assoaltorky\n\n"
    "دة الفيس بوك\n"
    "https://www.facebook.com/ASSO.ALTORKY/\n\n"
    "متنساش تشترك وتتابعنا عليهم😍❤️"
)
MESSAGE_SORRY="sorryy"
MESSAGE_REQUEST_ID="id?"
MESSAGE_SELL_ACCOUNT="selll"
MESSAGE_RECHARGE_PUBG = (
    "الاسعار الموجودة 🏷\n"
    "ببجي العالمية فقط 🎮🔫\n\n"
    "الشحن بالأيدي 🆔\n"
    "60 UC💵 = 50 EG💷\n"
    "355 UC💵 = 260 EG💷\n"
    "720 UC💵 = 490 EG💷\n"
    "1950 UC💵 = 1200 EG💷\n"
    "4000 UC💵 = 2250 EG💷\n"
    "8400 UC💵 = 4500 EG💷\n"
    "16800 UC💵 = 9000 EG💷\n"
    "25200 UC💵 = 13600 EG💷\n\n"
    "اسعار عروض الايدي المره الواحدة ...\n"
    "60 UC💵 = 40 EG💷\n"
    "120 UC💵 = 70 EG💷\n"
    "360 UC💵 = 200 EG💷"
)

MESSAGE_RECHARGE_DONE = (
    "شداتك وصلت حسابك بالسلامه ياصديقي🚀❤️\n"
    "اتمني تكون تكون خدمتنا مرضيه بالنسبه ليك 💖👑\n"
    "متسناش تقيمنا علي التيليجرام وتقول رايك ف الاستور 💞❣️\n"
    "https://t.me/arabtechnogroup/5020"
)

MESSAGE_SURE_PAY = (
    "❗️اهلا بحضرتك اتمني منك انك تتاكد ب ارسال الاموال و انو تم خصم المبلغ من عندك ❗️"
)

MESSAGE_SURE_PAY_ADMIN = (
    "🖤⚠️تم ابلاغ العميل بعدم الشدات⚠️🖤"
)

MESSAGE_RECHARGE_DONE_ADMIN = (
    "❤️⚠️تم ابلاغ العميل بوصول الشدات⚠️❤️"
)

MESSAGE_WELCOME = (
    "نورت جروب العائلة الملكية (جروب عرب تكنو) ❤️😍\n"
    "اتفضل ياحبيب قلبي قولي اقدر اساعدك ازاي.؟❤️‍🔥👌"
)

MESSAGE_ONE_TIME_ID = "شرح عروض المره الواحده"

MESSAGE_FEEDBACK = (
    "تقدر تشوف الفيد باك و اراء الناس ف الاستور من خلال اللينك دا ❤️\n"
    "https://t.me/arabtechnogroup/5020"
)

# معلومات المسؤول
TARGET_CHAT_ID = 1212985250

# مسار حفظ الصورة
IMAGE_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Photos')

# إعدادات تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# مجموعات لتخزين معرفات الصور والرسائل المرسلة
sent_photos = set()
sent_messages = set()

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    keyboard = [
        [InlineKeyboardButton("💌❤️عن عرب تكنو❤️💌", callback_data='about')],
        [InlineKeyboardButton("⚡💵شحن شدات ببجي موبايل💵⚡", callback_data='recharge')],
        [InlineKeyboardButton("💕❤فيدباك الاستور❤💕", callback_data='feedback')],
        [InlineKeyboardButton("✅💝بيع حسابات ببجي💝✅", callback_data='sell')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id,
        text=MESSAGE_WELCOME,
        reply_markup=reply_markup
    )

def delete_message(context: CallbackContext) -> None:
    job = context.job
    chat_id, message_id = job.context
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

def button(update: Update, context: CallbackContext) -> None:
    global USER_ID, USER_CHAT_ID
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    if query.data == 'about':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=MESSAGE_ABOUT_ARAB_TECHNO, reply_markup=reply_markup)
    elif query.data == 'feedback':
        message = context.bot.send_message(chat_id=chat_id, text=MESSAGE_FEEDBACK)
        context.job_queue.run_once(delete_message, 60, context=(chat_id, message.message_id))

    elif query.data == 'recharge':
        keyboard = [
            [InlineKeyboardButton("✅موافق✅", callback_data='agree')],
            [InlineKeyboardButton("ℹ️‼️ما هي عروض الايدي للمره الواحدة‼️ℹ️", callback_data='one_time_id')],
            [InlineKeyboardButton("❎غير موافق❎", callback_data='disagree')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.bot.send_message(chat_id=chat_id, text=MESSAGE_RECHARGE_PUBG, reply_markup=reply_markup)

    elif query.data == 'sell':
        context.bot.send_message(chat_id=chat_id, text=MESSAGE_SELL_ACCOUNT)

    elif query.data == 'agree':
        context.user_data['waiting_for_id'] = True
        context.bot.send_message(chat_id=chat_id, text=MESSAGE_REQUEST_ID)

    elif query.data == 'one_time_id':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=MESSAGE_ONE_TIME_ID, reply_markup=reply_markup)

    elif query.data == 'disagree':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=MESSAGE_SORRY, reply_markup=reply_markup)

    elif query.data == 'insta':
        keyboard = [
            [InlineKeyboardButton("✅تم التحويل✅", callback_data='insta_done')],
            [InlineKeyboardButton("❌الغاء❌", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.bot.send_message(chat_id=chat_id, text=INSTANT_PAYMENT_ADDRESS, reply_markup=reply_markup)
        context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))

    elif query.data == 'red':
        keyboard = [
            [InlineKeyboardButton("✅تم التحويل✅", callback_data='red_done')],
            [InlineKeyboardButton("❌الغاء❌", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.bot.send_message(chat_id=chat_id, text=VODAFONE_CASH, reply_markup=reply_markup)
        context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))

    elif query.data == 'insta_done':
        context.bot.send_message(chat_id=chat_id, text="لو سمحت ابعتلي IPN (عنوان الدفع)الخاص بكم او صوره التحويل❗️❤")
        context.user_data['action'] = 'user_ipn'
        USER_CHAT_ID = chat_id
        USER_ID = update.message.from_user.id

    elif query.data == 'red_done':
        context.bot.send_message(chat_id=chat_id, text="لو سمحت ابعتلي IPN (عنوان الدفع)الخاص بكم او صوره التحويل❗️❤")
        context.user_data['action'] = 'user_ipn'
        USER_CHAT_ID = chat_id
        USER_ID = update.message.from_user.id

    elif query.data == 'main_menu':
        start(update, context)

def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = update.message.text

    if context.user_data.get('waiting_for_id'):
        # معالجة إدخال ID للمستخدمين
        context.user_data['waiting_for_id'] = False
        context.bot.send_message(chat_id=chat_id, text="تم استلام الشحنة بنجاح, شكرًا لك!")
        context.bot.send_message(chat_id=TARGET_CHAT_ID, text=f"استلم ID من {chat_id}: {text}")
        context.bot.send_message(chat_id=USER_CHAT_ID, text=MESSAGE_RECHARGE_DONE)

def error(update: Update, context: CallbackContext) -> None:
    """يتم استدعاءه عند حدوث أي خطأ"""
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    """تشغيل البوت"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
