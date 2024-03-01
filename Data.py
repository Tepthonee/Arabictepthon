from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [
        InlineKeyboardButton("✨ بـدء استخـراج الجلســة .", callback_data="generate")
    ]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="🏠 العودة إلى  الصفحـة الرئيسيـة .", callback_data="home")],
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton(
                "ســورس تيبثـون .", url="https://t.me/Tepthon"
            )
        ],
        [
            InlineKeyboardButton("كيفية استخدامي ❓ .", callback_data="help"),
            InlineKeyboardButton("🌐 حول  .", callback_data="about"),
        ],
        [InlineKeyboardButton("🧑‍💻 المطـور .", url="https://t.me/Alexa_Help")],
    ]

    START = """
**مرحبًـــا  👋** {}
**أهلًا وسهلًا بـ** {}
**~ ملاحظـات هامـة ⚠️ :**
1) لا تشارك كود الجلسـة لأحـد 🚫 .
2) لا تشـارك الكـود لأحـد 🧑‍💻 .
3) احـذر أن تخلي أي شخص ينصبلك ( نصـب بنفسـك ) ‼️ .
**~ طريقـة الاستخدام :**
اضغط على بدء استخراج الجلسـة، وبعد ذلك اختر نوع الجلسـة ( تليثـون ، بايروجـرام )
من @Tepthon 🌐 .
    """

    HELP = """
**الأوامر المتاحـة**

/help

/start

/about

/Restart

/cancel

"""

    # About Message
    ABOUT = """
**حـول البـوت 🌐** 

يمكن لهذا البوت استخراج كود الجلسة لـ تنصيب سورس تيبثـون

**~ المطور** : @PPF22
**~ السـورس** : @Tepthon
    """

    # Repo Message
    REPO = """
سورس تيبثـون العربـي يقدم لكـم
بوت استخـراج جلسـات لـ تنصيب تيبثون 🧑‍💻
تيبثون : هو بوت يقوم بالدخول إلى حسابك وينفذ بعض الأوامر بدلًا عنك .    
المطـور ~ محمـد : @PPF22
   """
