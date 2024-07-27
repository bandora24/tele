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

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    keyboard = [
        [InlineKeyboardButton("💌❤️عن عرب تكنو❤️💌", callback_data='about')],
        [InlineKeyboardButton("⚡💵شحن شدات ببجي موبايل💵⚡", callback_data='recharge')],
        [InlineKeyboardButton("💕❤فيدباك الاستور❤💕", callback_data='feedback')],
#        [InlineKeyboardButton("✅💝بيع حسابات ببجي💝✅", callback_data='sell')]
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
    elif query.data == 'red_done':
        context.bot.send_message(chat_id=chat_id, text="لو سمحت ابعتلي رقم المحفظة اللي تم تحويل منها الاموال❗️❤")
        context.user_data['action'] = 'user_wallet'
        USER_CHAT_ID = chat_id
    elif query.data == 'confirm_payment':
        if USER_CHAT_ID:
            context.bot.send_message(chat_id=USER_CHAT_ID, text=MESSAGE_RECHARGE_DONE)
            context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGE_RECHARGE_DONE_ADMIN)
    elif query.data == 'cancel':
        if USER_CHAT_ID:
            context.bot.send_message(chat_id=USER_CHAT_ID, text=MESSAGE_SURE_PAY)
            context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGE_SURE_PAY_ADMIN)
    elif query.data == 'main_menu':
        start(update, context)

def handle_message(update: Update, context: CallbackContext) -> None:
    global USER_ID, USER_CHAT_ID
    chat_id = update.message.chat_id
    user_action = context.user_data.get('action')

    # التعامل مع الصور
    if update.message.photo:
        if user_action not in ['user_ipn', 'user_wallet']:
            return

        file_id = update.message.photo[-1].file_id
        if file_id in sent_photos:
            return

        new_file = context.bot.get_file(file_id)
        file_name = f"{chat_id}_{int(time.time())}.jpg"
        file_path = os.path.join(IMAGE_SAVE_PATH, file_name)

        try:
            if not os.access(IMAGE_SAVE_PATH, os.W_OK):
                context.bot.send_message(chat_id, "لا يمكن حفظ الصورة. تأكد من صلاحيات المجلد.")
                return

            os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)
            new_file.download(file_path)
            logger.info(f"Downloaded photo to: {file_path}")

            with Image.open(file_path) as img:
                img.save(file_path, optimize=True, quality=60)
                logger.info(f"Optimized photo saved to: {file_path}")

            # إعداد الأزرار
            keyboard = [
                [InlineKeyboardButton("✅تم التحويل✅", callback_data='confirm_payment')],
                [InlineKeyboardButton("❌إلغاء❌", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            with open(file_path, 'rb') as photo:
                # إرسال الصورة مع الأزرار إلى المسؤول
                context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=photo, caption=f"صوره من {update.message.from_user.first_name}\n" +
                                                                                     f"اليوزر نيم: @{update.message.from_user.username}\n" +
                                                                                     f"طريقة الدفع صوره\n" +
                                                                                     f"ID : {USER_ID}",
                                                                                     reply_markup=reply_markup)

            sent_photos.add(file_id)
            context.bot.send_message(chat_id=chat_id, text="تم إرسال الصورة بنجاح.")
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            context.bot.send_message(chat_id=chat_id, text="حدث خطأ أثناء إرسال الصورة.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            context.bot.send_message(chat_id=chat_id, text="حدث خطأ غير متوقع.")
        finally:
            os.remove(file_path)
        return

    # التعامل مع النصوص
    if context.user_data.get('waiting_for_id'):
        USER_ID = update.message.text
        context.user_data['user_id'] = USER_ID
        context.user_data['waiting_for_id'] = False
        # الانتقال إلى عرض طرق الدفع مباشرة بعد الحصول على الـ ID
        keyboard = [
            [InlineKeyboardButton("InstaPay", callback_data='insta')],
            [InlineKeyboardButton("Vodafone Cash", callback_data='red')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text="💌❤️برجاء اختيار طريقه التحويل المتاحه ❤️💌", reply_markup=reply_markup)
        USER_CHAT_ID = chat_id

    elif user_action == 'user_ipn':
        ipn_address = update.message.text
        message_text = f"اسم المستخدم: {update.message.from_user.first_name}\n" \
                       f"اليوزر نيم: @{update.message.from_user.username}\n" \
                       f"طريقة الدفع: IPN\n" \
                       f"عنوان الدفع: {ipn_address}\n" \
                       f"ID : {USER_ID}"

        if message_text not in sent_messages:
            context.user_data['ipn'] = ipn_address
            # إرسال الرسالة إلى المسؤول مع الزرار
            keyboard = [
                [InlineKeyboardButton("✅تم التحويل✅", callback_data='confirm_payment')],
                [InlineKeyboardButton("❌إلغاء❌", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text, reply_markup=reply_markup)
            sent_messages.add(message_text)

            # رسالة تأكيد للمستخدم
            context.bot.send_message(chat_id=chat_id, text=MESSAGE_PROCESSING)

    elif user_action == 'user_wallet':
        wallet_address = update.message.text
        message_text = f"اسم المستخدم: {update.message.from_user.first_name}\n" \
                       f"اليوزر نيم: @{update.message.from_user.username}\n" \
                       f"طريقة الدفع: محفظة فودافون كاش\n" \
                       f"رقم المحفظة: {wallet_address}\n" \
                       f"ID : {USER_ID}"

        if message_text not in sent_messages:
            context.user_data['wallet'] = wallet_address
            # إرسال الرسالة إلى المسؤول مع الزرار
            keyboard = [
                [InlineKeyboardButton("✅تم التحويل✅", callback_data='confirm_payment')],
                [InlineKeyboardButton("❌إلغاء❌", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text, reply_markup=reply_markup)
            sent_messages.add(message_text)

            # رسالة تأكيد للمستخدم
            context.bot.send_message(chat_id=chat_id, text=MESSAGE_PROCESSING)

    else:
        # إذا كان المستخدم في مرحلة معينة، لا يتم تنفيذ هذه الخطوة
        if user_action is None:
            start(update, context)

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
