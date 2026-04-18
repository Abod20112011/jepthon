#    جميع الحقوق لمطوري سورس جـيبثون حصريا لهم فقط
#    اذا تخمط الملف اذك الحقوق وكاتبيه ومطوريه لا تحذف الحقوق وتصير فاشل 👍
#    كتابة الشسد 
import asyncio
import io
import re

from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest
from JoKeRUB import bot
from JoKeRUB.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from JoKeRUB.sql_helper.botusers_sql import add_me_in_db, his_userid
from JoKeRUB.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)
from l313l.razan.resources.assistant import *

# ==================== start ====================
@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    rehu = await tgbot.get_me()
    bot_id = rehu.first_name
    bot_username = rehu.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.users[0].first_name
    vent = event.chat_id
    starttext = f"**مـرحبا {firstname} ! انـا هـو {bot_id}, بـوت مساعـد بسيـط 🧸🤍 \n\n- [مـالك البـوت](tg://user?id={bot.uid}) \nيمكـنك مراسلـة المـالك عبـر هذا البـوت . \n\nاذا كـنت تـريد تنـصيب بـوت خـاص بـك تـاكد من الازرار بالأسفل**"
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"اهـلا يا مالكـي انـه انـا {bot_id}, مسـاعدك ! \nمـاذا تريـد ان تفعـل اليـوم ?",
            buttons=[
                [Button.inline("🟢 عرض المستخدمين 📬", data="users"),
                 Button.inline("🔵 اوامر البـوت ⚒️", data="gibcmd")],
                [Button.url("🔗 المطـور 🔗", "https://t.me/lMl10l"),
                 Button.inline("🟣 اوامر الزغـرفة", data="rozzag")],
            ]
        )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_message(
            event.chat_id,
            message=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("🐍 تنـصيب جيـبثون", data="deploy")],
                [Button.url("❓ تحتاج مسـاعدة", "https://t.me/lMl10l")],
            ],
        )

# ==================== Data ====================
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
            message="**لتـنصيب البـوت الخاص بك اتبـع الخطـوات في الاسفـل وحاول واذا لم تستطيع تفضل الى مجموعة المساعدة ليساعدوك 🧸♥**.",
            buttons=[
                [Button.url("📺 شرح التنصيب", "https://youtu.be/ATAgbLGzr7w")],
                [Button.url("❓ كروب المساعدة", "https://t.me/jepthonSupport")],
            ],
        )

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "- قـائمة مستخـدمين البـوت  : \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "JoKeRUB.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                caption="مجموع مستخدمـين بوتـك",
                allow_cache=False,
            )
    else:
        pass

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def gibcmd(event):
    await event.delete()
    rorza = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await tgbot.send_message(event.chat_id, rorza)

@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    rorza = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await event.reply(rorza)

@tgbot.on(events.NewMessage(pattern="^/alive", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    razan = "**𝘑𝘌𝘗𝘛𝘏𝘖𝘕 𝘜𝘚𝘌𝘙𝘉𝘖𝘛**\n•━═━═━═━═━━═━═━═━═━•‌‌\n**- حالة البوت **  يعمـل بنجـاح\n**- اصدار التليثون  **: 1.23.0\n**- اصدار البايثون **: 3.9.6\n**- يوزرك ** {mention}\n**- CH : @jepthon\n•━═━═━═━═━━═━═━═━═━•‌‌\n"
    await event.reply(razan)

# ==================== أوامر الزغرفة (ملونة) ====================
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozzag")))
async def settings(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ اختر احد خيارات الزغرفه : **",
                                 buttons=[
                                     [Button.inline("🔴 اسماء انكلش", data="rozname")],
                                     [Button.inline("🔵 البايو", data="rozpio1")],
                                     [Button.inline("🟣 الاشهر", data="rozmonth")],
                                     [Button.inline("🟡 اسماء القنوات", data="chanlan")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozname")))
async def rozname(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ اختر احد الخيارات الاتيه. **",
                                 buttons=[
                                     [Button.inline("🟢 اسماء شباب", data="razan")],
                                     [Button.inline("🔴 اسماء بنات", data="RR7PP")],
                                     [Button.inline("🔵 رجوع", data="rozzag")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"razan")))
async def razan(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ اختر احد الخيارات الاتيه. **",
                                 buttons=[
                                     [Button.inline("🟢 القائمه الاولى", data="rzan1")],
                                     [Button.inline("🔵 القائمه الثانيه", data="raza2")],
                                     [Button.inline("🔴 رجوع", data="rozname")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rzan1")))
async def rzan1(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Boyroz1,
                                 buttons=[[Button.inline("🔵 رجوع", data="razan")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"raza2")))
async def raza2(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Boyroz2,
                                 buttons=[[Button.inline("🔵 رجوع", data="razan")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP")))
async def RR7PP(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ اختر احد الخيارات الاتيه. **",
                                 buttons=[
                                     [Button.inline("🟢 القائمه الاولى", data="RR7PP1")],
                                     [Button.inline("🔵 القائمه الثانيه", data="RR7PP2")],
                                     [Button.inline("🔴 رجوع", data="rozname")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP1")))
async def RR7PP1(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Girlan1,
                                 buttons=[[Button.inline("🔵 رجوع", data="RR7PP")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP2")))
async def RR7PP2(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Girlan2,
                                 buttons=[[Button.inline("🔵 رجوع", data="RR7PP")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio1")))
async def rozpio1(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO1,
                                 buttons=[
                                     [Button.inline("🟢 السابق", data="rozpio5")],
                                     [Button.inline("🔴 خروج", data="rozzag")],
                                     [Button.inline("🔵 التالي", data="rozpio2")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio2")))
async def rozpio2(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO2,
                                 buttons=[
                                     [Button.inline("🟢 السابق", data="rozpio1")],
                                     [Button.inline("🔴 خروج", data="rozzag")],
                                     [Button.inline("🔵 التالي", data="rozpio3")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio3")))
async def rozpio3(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO3,
                                 buttons=[
                                     [Button.inline("🟢 السابق", data="rozpio2")],
                                     [Button.inline("🔴 خروج", data="rozzag")],
                                     [Button.inline("🔵 التالي", data="rozpio4")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio4")))
async def rozpio4(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO4,
                                 buttons=[
                                     [Button.inline("🟢 السابق", data="rozpio3")],
                                     [Button.inline("🔴 خروج", data="rozzag")],
                                     [Button.inline("🔵 التالي", data="rozpio5")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio5")))
async def rozpio5(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO5,
                                 buttons=[
                                     [Button.inline("🟢 السابق", data="rozpio4")],
                                     [Button.inline("🔴 خروج", data="rozzag")],
                                     [Button.inline("🔵 التالي", data="rozpio1")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozmonth")))
async def rozmonth(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ اختر احد الخيارات الاتيه. **",
                                 buttons=[
                                     [Button.inline("🟢 المواليـد", data="rozyear")],
                                     [Button.inline("🔵 الأشـهر", data="months")],
                                     [Button.inline("🔴 رجوع", data="rozzag")],
                                 ])
    else:
        await event.answer("انت لا تستطيع استخدام البوت احصل على بوتك من @jepthon", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"months")))
async def months(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 JMTHSH,
                                 buttons=[[Button.inline("🔵 رجوع", data="rozzag")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozyear")))
async def rozyear(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 JEPYEAR,
                                 buttons=[[Button.inline("🔵 رجوع", data="rozmonth")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"chanlan")))
async def chanlan(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 CHANLAN,
                                 buttons=[[Button.inline("🔵 رجوع", data="rozzag")]])
    else:
        await event.answer("انت لا تستطيع استخدام هذا البوت.", alert=True)
