import os
import logging
import time
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from telegram.error import TelegramError
# إعدادات البوت
TOKEN = '6726740074:AAFp8Veghav5Fmu0LDKcHObCwVdqcsVQgaw'
INSTANT_PAYMENT_ADDRESS = "mobander@instapay"
VODAFONE_CASH = "01007265599\n⚠️❗️الرقم مش للكول ولا الواتساب دا رقم كاش فقط❗️⚠️"
USER_CHAT_ID: None = None
# رسائل مختلفة
MESSAGE_ABOUT_ARAB_TECHNO = """
معاك البوت الرسمي الخاص ب عرب تكنو ستور🤖

مرحبا في عالم عرب تكنو❤️🌍

اتمنى تكون مشترك معانا ف الديسكورد
https://discord.com/invite/VAUxAtn8qn

ولو متعرفش دة الاستور الخاص ب أسوو - ASSO 
وقناة عرب تكنو

ودي صفحه الانستا بتاعنا تابعنا علشان تعرف كل الاخبار
https://www.instagram.com/asso.altorky

ودي قناة اليوتيوب
https://www.youtube.com/c/3rabtechno

دة التيك توك
https://www.tiktok.com/@assoaltorky

دة الفيس بوك
https://www.facebook.com/ASSO.ALTORKY/

متنساش تشترك وتتابعنا عليهم😍❤️
"""
MESSAGE_RECHARGE_PUBG = """
الاسعار الموجودة 🏷
ببجي العالمية فقط 🎮🔫
الشحن بالأيدي 🆔
60 UC💵 = 50 EG💷
355 UC💵 = 260 EG💷
720 UC💵 = 490 EG💷
1950 UC💵 = 1200 EG💷
4000 UC💵 = 2250 EG💷
8400 UC💵 = 4500 EG💷
16800 UC💵 = 9000 EG💷
25200 UC💵 = 13600 EG💷
اسعار عروض الايدي المره الواحدة ...
60 UC💵 = 40 EG💷
120 UC💵 = 70 EG💷
360 UC💵 = 200 EG💷
"""
MESSAGE_WELCOME = 'نورت جروب العائلة الملكية (جروب عرب تكنو) ❤️😍\nاتفضل ياحبيب قلبي قولي اقدر اساعدك ازاي.؟❤️‍🔥👌'
MESSAGE_SORRY = "برجاء العلم ان هذه الاسعار هي اقل اسعار يمكن توفيرها حاليا نتمني لك يوم سعيد❤😍"
MESSAGE_RECHARGE_DONE = "شداتك وصلت حسابك بالسلامه ياصديقي🚀❤️\nاتمني تكون تكون خدمتنا مرضيه بالنسبه ليك 💖👑\nمتسناش تقيمنا علي التيليجرام وتقول رايك ف الاستور 💞❣️\nhttps://t.me/arabtechnogroup/5020"
MESSAGE_SURE_PAY = "برجاء التاكد من تحويل الاموال بشكل كامل"
MESSAGE_REQUEST_ID = "يرجى إدخال الـ ID الخاص بك:"
MESSAGE_PROCESSING = "برجاء الانظار الشدات هتوصل ف حسابك مجرد مراجعه البيانات ياصاحبي"
MESSAGE_RECHARGE_DONE_ADMIN = "وصل ياباشا "
MESSAGE_SURE_PAY_ADMIN = "تم ابلاغ العميل "
MESSAGE_ONE_TIME_ID = "عروض الايدي للمره الواحده هي عباره عن عروض لكل اكونت بتتشحن مره واحده بس مينفعش تتشحن مرتين ,طلما اتشحنت مره مينفعش تتشحن تاني😍🫶🏻"
MESSAGE_FEEDBACK = "تقدر تشوف الفيد باك و اراء الناس ف الاستور من خلال اللينك دا ❤️\nhttps://t.me/arabtechnogroup/5020"
MESSAGE_SELL_ACCOUNT="بيع"
SURING_PAY="برجاء الانظار الشدات هتوصل ف حسابك مجرد مراجعه البيانات ياصاحبي"


# معلومات المسؤول
TARGET_CHAT_ID = 1212985250
ADMIN_CHAT_LOG = 5414032995  # استبدل هذا بالقيمة الصحيحة لمعرف المسؤول الرئيسي

# إعدادات تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# مجموعات لتخزين معرفات الصور والرسائل المرسلة
sent_photos = set()
sent_messages = set()
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
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
    global USER_CHAT_ID
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == 'about':
        keyboard = [[InlineKeyboardButton("📜القائمة الرئيسية📜", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=MESSAGE_ABOUT_ARAB_TECHNO, reply_markup=reply_markup)
    elif query.data == 'feedback':
        message = await context.bot.send_message(chat_id=chat_id, text=MESSAGE_FEEDBACK)
        context.job_queue.run_once(delete_message, 60, context=(chat_id, message.message_id))
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
        context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))
    elif query.data == 'red':
        keyboard = [
            [InlineKeyboardButton("✅تم التحويل✅", callback_data='red_done')],
            [InlineKeyboardButton("❌الغاء❌", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=chat_id, text=VODAFONE_CASH, reply_markup=reply_markup)
        context.job_queue.run_once(delete_message, 300, context=(chat_id, message.message_id))
    elif query.data == 'insta_done':
        await context.bot.send_message(chat_id=chat_id, text="لو سمحت ابعتلي IPN (عنوان الدفع)الخاص بكم او صوره التحويل❗️❤")
        context.user_data['action'] = 'user_ipn'
        USER_CHAT_ID = chat_id
    elif query.data == 'red_done':
        await context.bot.send_message(chat_id=chat_id, text="لو سمحت ابعتلي رقم المحفظة اللي تم تحويل منها الاموال❗️❤")
        context.user_data['action'] = 'user_wallet'
        USER_CHAT_ID = chat_id
    elif query.data == 'confirm_payment':
        if USER_CHAT_ID:
            await context.bot.send_message(chat_id=USER_CHAT_ID, text=MESSAGE_RECHARGE_DONE)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGE_RECHARGE_DONE_ADMIN)
    elif query.data == 'cancel':
        if USER_CHAT_ID:
            await context.bot.send_message(chat_id=USER_CHAT_ID, text=MESSAGE_SURE_PAY)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGE_SURE_PAY_ADMIN)
    elif query.data == 'main_menu':
        await start(update, context)

async def handle_message(update: Update, context: CallbackContext) -> None:
    global USER_ID, USER_CHAT_ID
    chat_id = update.message.chat_id
    user_action = context.user_data.get('action')

    # إرسال نسخة من الرسالة إلى المسؤول
    log_message = f"Message From :{update.message.from_user.full_name} \n(@{update.message.from_user.username})\n Chat ID:{chat_id} \n Message:                     \n {update.message.text}"

    if chat_id != ADMIN_CHAT_LOG:  # تجنب إرسال الرسائل إلى المسؤول نفسه
        await context.bot.send_message(chat_id=ADMIN_CHAT_LOG, text=log_message)


    # التعامل مع الصور
    if update.message.photo:
        if user_action not in ['user_ipn', 'user_wallet']:
            return

        file_id = update.message.photo[-1].file_id
        if file_id in sent_photos:
            return

        new_file = await context.bot.get_file(file_id)
        file_name = f"{chat_id}_{int(time.time())}.jpg"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

        try:
            if not os.access(os.path.dirname(os.path.abspath(__file__)), os.W_OK):
                await context.bot.send_message(chat_id, "لا يمكن حفظ الصورة. تأكد من صلاحيات المجلد.")
                return

            await new_file.download_to_drive(file_path)
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
                await context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=photo,
                                             caption=f"NickName {update.message.from_user.full_name}\n" +
                                                     f"UserName: @{update.message.from_user.username}\n"  +
                                                     f"ChatID: {chat_id}\n"+
                                                     f"طريقة الدفع Photo\n" +
                                                     f"PUBG Name: {context.user_data.get('pubg_name')}\n"
                                                     f"PUBG ID:\n {context.user_data.get('PUBG_ID')}",
                                             reply_markup=reply_markup)

            sent_photos.add(file_id)
            await context.bot.send_message(chat_id=chat_id, text=SURING_PAY)
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            await context.bot.send_message(chat_id=chat_id, text="حدث خطأ أثناء إرسال الصورة.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await context.bot.send_message(chat_id=chat_id, text="حدث خطأ غير متوقع.")
        finally:
            os.remove(file_path)
        return







    # التعامل مع النصوص
    if context.user_data.get('waiting_for_id'):
        PUBG_ID = update.message.text
        context.user_data['PUBG_ID'] = PUBG_ID
        context.user_data['waiting_for_id'] = False

        # طلب اسم PUBG بعد استلام الـ ID
        await context.bot.send_message(chat_id=chat_id, text="اسمك اي ف ببجي؟")
        context.user_data['waiting_for_pn'] = True  # تعيين حالة الانتظار لاسم PUBG
        USER_CHAT_ID = chat_id
        return


    elif context.user_data.get('waiting_for_pn'):
        pubg_name = update.message.text
        context.user_data['pubg_name'] = pubg_name
        context.user_data['waiting_for_pn'] = False

        # الانتقال إلى عرض طرق الدفع بعد الحصول على اسم PUBG
        keyboard = [
            [InlineKeyboardButton("InstaPay", callback_data='insta')],
            [InlineKeyboardButton("Vodafone Cash", callback_data='red')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text="💌❤️برجاء اختيار طريقه التحويل المتاحه ❤️💌",
                                       reply_markup=reply_markup)
        USER_CHAT_ID = chat_id
        return

    elif user_action == 'user_ipn':
        ipn_address = update.message.text
        message_text = f"NickName {update.message.from_user.full_name}\n" \
                       f"UserName: @{update.message.from_user.username}\n" \
                       f"ChatID: {chat_id}\n" \
                       f"طريقة الدفع: IPN\n" \
                       f"IPN: {ipn_address}\n" \
                       f"PUBG Name: {context.user_data.get('pubg_name')}\n"\
                       f"PUBG ID:\n {context.user_data.get('PUBG_ID')}"\

        if message_text not in sent_messages:
            context.user_data['ipn'] = ipn_address
            # إرسال الرسالة إلى المسؤول مع الزرار
            keyboard = [
                [InlineKeyboardButton("✅تم التحويل✅", callback_data='confirm_payment')],
                [InlineKeyboardButton("❌إلغاء❌", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text, reply_markup=reply_markup)
            sent_messages.add(message_text)

            # رسالة تأكيد للمستخدم
            await context.bot.send_message(chat_id=chat_id, text=MESSAGE_PROCESSING)
            context.user_data['action'] = None  # إعادة تعيين الحالة
        else:
            # إذا كانت الرسالة بعد إدخال الـ IPN، تحويل إلى القائمة الرئيسية
            await start(update, context)
        return

    elif user_action == 'user_wallet':
        wallet_address = update.message.text
        message_text = f"NickName {update.message.from_user.full_name}\n" \
                       f"UserName: @{update.message.from_user.username}\n" \
                       f"ChatID: {chat_id}\n" \
                       f"طريقة الدفع: محفظة فودافون كاش\n" \
                       f"Cash Number {wallet_address}\n" \
                       f"PUBG Name: {context.user_data.get('pubg_name')}\n"\
                       f"PUBG ID:\n {context.user_data.get('PUBG_ID')}"\

        if message_text not in sent_messages:
            context.user_data['wallet'] = wallet_address
            # إرسال الرسالة إلى المسؤول مع الزرار
            keyboard = [
                [InlineKeyboardButton("✅تم التحويل✅", callback_data='confirm_payment')],
                [InlineKeyboardButton("❌إلغاء❌", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text, reply_markup=reply_markup)
            sent_messages.add(message_text)

            # رسالة تأكيد للمستخدم
            await context.bot.send_message(chat_id=chat_id, text=MESSAGE_PROCESSING)
            context.user_data['action'] = None  # إعادة تعيين الحالة
        else:
            # إذا كانت الرسالة بعد إدخال رقم المحفظة، تحويل إلى القائمة الرئيسية
            await start(update, context)
        return

    # إذا كان المستخدم في مرحلة معينة، لا يتم تنفيذ هذه الخطوة
    if user_action is None:
        await start(update, context)














async def admin_send_message(update: Update, context: CallbackContext) -> None:
    """يرسل رسالة إلى أي مستخدم من قبل المسؤول"""
    if update.message.chat_id != ADMIN_CHAT_LOG:
        await update.message.reply_text("ليس لديك إذن لإرسال رسائل.")
        return

    # تقسيم النص إلى أجزاء
    if len(context.args) < 2:
        await update.message.reply_text("يرجى إدخال تنسيق الرسالة بشكل صحيح:\n/send_message <chat_id> <الرسالة>")
        return

    chat_id = context.args[0].strip()
    message = " ".join(context.args[1:]).strip()

    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
        await update.message.reply_text(f"تم إرسال الرسالة إلى {chat_id}.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")



def main():
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
