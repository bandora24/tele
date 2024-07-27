import os
import logging
import asyncio
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

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
    "ولو متعرفش دة الاستور الخاص ب @Asso_Altorky\n"
    "وقناة عرب تكنو\n\n"
    "ودي صفحه الانستا بتاعنا تابعنا علشان تعرف كل الاخبار\n"
    "https://www.instagram.com/asso.altorky\n\n"
    "ودي قناة اليوتيوب\n"
    "https://www.youtube.com/c/3rabtechno\n\n"
    "دة التيك توك\n"
    "https://www.tiktok.com/@assoaltorky\n\n"
    "دة الفيس بوك\n"
    "https://www.facebook.com/ASSO.ALTORKY/\n\n"
    "متنساش تشترك وتتابعنا عليهم😍❤️\n"
    "لو احتاجت اي مساعده كلم @Mohamedbander"
)
MESSAGE_RECHARGE_PUBG = (
    "الاسعار الموجودة 🏷\n"
    "ببجي العالمية فقط 🎮🔫\n"
    "الشحن بالأيدي 🆔\n\n"
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
MESSAGE_SELL_ACCOUNT = "هذه رسالة لبيع حساب ببجي"
MESSAGE_WELCOME = 'نورت جروب العائلة الملكية (جروب عرب تكنو) ❤️😍\nاتفضل ياحبيب قلبي قولي اقدر اساعدك ازاي.؟❤️‍🔥👌'
MESSAGE_SORRY = "برجاء العلم ان هذه الاسعار هي اقل اسعار يمكن توفيرها حاليا نتمني لك يوم سعيد❤😍"
MESSAGE_RECHARGE_DONE = (
    "شداتك وصلت حسابك بالسلامه ياصديقي🚀❤️\n"
    "اتمني تكون تكون خدمتنا مرضيه بالنسبه ليك 💖👑\n"
    "متسناش تقيمنا علي التيليجرام وتقول رايك ف الاستور 💞❣️\n"
    "https://t.me/arabtechnogroup/5020"
)
MESSAGE_SURE_PAY = "❗️اهلا بحضرتك اتمني منك انك تتاكد ب ارسال الاموال و انو تم خصم المبلغ من عندك ❗️"
MESSAGE_REQUEST_ID = "يرجى إدخال الـ ID الخاص بك:"
MESSAGE_PROCESSING = "تم استلام بياناتك، وسيتم مراجعة العملية بواسطة المشرفين. شكراً لتعاونك."
MESSAGE_RECHARGE_DONE_ADMIN = "❤️⚠️تم ابلاغ العميل بوصول الشدات⚠️❤️"
MESSAGE_SURE_PAY_ADMIN = "🖤⚠️تم ابلاغ العميل بعدم الشدات⚠️🖤"
MESSAGE_ONE_TIME_ID = "شرح عروض المره الواحده"
MESSAGE_FEEDBACK = "تقدر تشوف الفيد باك و اراء الناس ف الاستور من خلال اللينك دا ❤️\nhttps://t.me/arabtechnogroup/5020"

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

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("💌❤️عن عرب تكنو❤️💌", callback_data='about')],
        [InlineKeyboardButton("⚡💵شحن شدات ببجي موبايل💵⚡", callback_data='recharge')],
        [InlineKeyboardButton("💕❤فيدباك الاستور❤💕", callback_data='feedback')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text=MESSAGE_WELCOME,
        reply_markup=reply_markup
    )

async def delete_message(context: CallbackContext) -> None:
    job = context.job
    chat_id, message_id = job.context
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

async def button(update: Update, context: CallbackContext) -> None:
    global USER_ID, USER_CHAT_ID
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == 'about':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_ABOUT_ARAB_TECHNO, reply_markup=reply_markup)
    elif query.data == 'feedback':
        message = await context.bot.send_message(chat_id=chat_id, text=MESSAGE_FEEDBACK)
        await context.job_queue.run_once(delete_message, 60, context=(chat_id, message.message_id))
    elif query.data == 'recharge':
        keyboard = [
            [InlineKeyboardButton("✅موافق✅", callback_data='agree')],
            [InlineKeyboardButton("ℹ️‼️ما هي عروض الايدي للمره الواحدة‼️ℹ️", callback_data='one_time_id')],
            [InlineKeyboardButton("❎غير موافق❎", callback_data='disagree')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=chat_id, text=MESSAGE_RECHARGE_PUBG, reply_markup=reply_markup)
    elif query.data == 'sell':
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_SELL_ACCOUNT)
    elif query.data == 'agree':
        context.user_data['waiting_for_id'] = True
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_REQUEST_ID)
    elif query.data == 'one_time_id':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_ONE_TIME_ID, reply_markup=reply_markup)
    elif query.data == 'disagree':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_SORRY, reply_markup=reply_markup)
    elif query.data == 'insta':
        keyboard = [
            [InlineKeyboardButton("✅تم التحويل✅", callback_data='insta_done')],
            [InlineKeyboardButton("❌الغاء❌", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=chat_id, text=INSTANT_PAYMENT_ADDRESS, reply_markup=reply_markup)
        await context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))
    elif query.data == 'red':
        keyboard = [
            [InlineKeyboardButton("✅تم التحويل✅", callback_data='insta_done')],
            [InlineKeyboardButton("❌الغاء❌", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=chat_id, text=VODAFONE_CASH, reply_markup=reply_markup)
        await context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))

async def handle_message(update: Update, context: CallbackContext) -> None:
    global USER_ID, USER_CHAT_ID
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        if photo not in sent_photos:
            sent_photos.add(photo)
            await update.message.reply_text("صورة جديدة تم استلامها. شكراً.")
    elif update.message.text:
        if 'waiting_for_id' in context.user_data:
            USER_ID = update.message.text
            context.user_data['waiting_for_id'] = False
            await update.message.reply_text(MESSAGE_PROCESSING)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=f"استلام بيانات:\n\nID: {USER_ID}\nChat ID: {USER_CHAT_ID}")
            await update.message.reply_text(MESSAGE_RECHARGE_DONE)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGE_RECHARGE_DONE_ADMIN)
        else:
            await update.message.reply_text("لا يمكن معالجة رسالتك حالياً.")
    elif update.message.document:
        if update.message.document.mime_type.startswith('image/'):
            file = await update.message.document.get_file()
            file.download(os.path.join(IMAGE_SAVE_PATH, update.message.document.file_name))
            await update.message.reply_text("تم استلام الصورة بنجاح.")

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
