from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(
        "« يرجى اختيـار الجلسـة التي تريد استخراجهــا من الجلسات المذكورة أدناه :",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بايروجـرام 🌐", callback_data="pyrogram"),
                    InlineKeyboardButton("تليثــون ✨", callback_data="telethon"),
                ]
            ]
        ),
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply(
        "جـاري {} استخـراج جلسـة...".format(
            "تليثون" if telethon else "بايروجرام"
        )
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "**« يرجى إرسـال الأيبـي أيـدي ...**", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "**« الأيبي أيدي الخـاص بك غير صحيـح**",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "**« يرجى إرسال الأيبي هـاش ...**", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "**« يرجـى إرسال رقم الهاتف الخـاص بـك مع رمز الدولة 📱 \n**مثـال** : `+970**********`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("** « جـاري إرسـال الكود....** ✉️")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "**« الأيبـي أيـدي و الأيبـي هـاش الذي أرسلتـه خاطئ**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "**« رقم الهاتــف الخـاص بـك خاطـئ** 🚫 .",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "يرجى إرسال الرمز الذي أرسلته تليجرام مثال :\nمثال : `**12345**`, **يرجى إرسال الكود بين كل رقم ورقم مسافة** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "**انقضت مهلـة الاستخـراج ⏳** : لقد منحت مدة (5) دقائق ولم تستخرج فيها الجلسة إذا كنت تريد الاستخراج مرة أخرى أعد الاستخراج .",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "**« الكـود خاطـئ يرجى إعادة الاستخراج** .",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "**« انتهـت صلاحيـة الكـود 🚫**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "**« حسابك مفعل بالتحقق بخطوتين يرجى إرسال التحقق بخطوتين الخاص بحسابك ⚠️** .",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "**انقضت مهلـة الاستخـراج ⏳** : لقد منحت مدة (5) دقائق ولم تستخرج فيها الجلسة إذا كنت تريد الاستخراج مرة أخرى أعد الاستخراج .",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "التحقق بخطوتين خاطـئ أعد الاستخراج مرة أخرى ..",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
        text = "**{}  تم استخراج جلسـة** \n\n`{}` \n\تم الاستخراج من @Tepthon 🇵🇸/n **ملاحظة** : لا تشارك الكود لأي أحد وأرجو منكم الدعاء لأهلنا في فلسطين 🇵🇸".format(
        "تليثـون" if telethon else "بايروجـرام", string_session
    )
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        "تم استخراج جلسة {}. \n\يرجى تفقد الرسائل المحفوظة \n\nمن 🇵🇸 @Tepthon".format(
            "تليثون" if telethon else "بايروجرام"
        )
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "تم",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "تم",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم الإلغاء", quote=True)
        return True
    else:
        return False
