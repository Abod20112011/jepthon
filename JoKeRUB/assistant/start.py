# -*- coding: utf-8 -*-
import re
import json
import requests
from collections import defaultdict
from datetime import datetime

from telethon import Button, events
from telethon.utils import get_display_name

from . import Config, l313l
from ..core.logger import logging
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import add_user_to_db, get_user_id
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from ..sql_helper.globals import gvarstatus
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"
botusername = Config.TG_BOT_USERNAME
Zel_Uid = l313l.uid
kk = []
tt = []
whisper_users = []

# إيموجي بريميوم
EMOJI_CONTACT = "5258215850745275216"
EMOJI_CHANNEL = "5260450573768990626"
EMOJI_fatfta = "5188619457651567219"
EFFECT_ID = "5046509860389126442"

class FloodConfig:
    BANNED_USERS = set()
    USERS = defaultdict(list)
    MESSAGES = 3
    SECONDS = 6
    ALERT = defaultdict(dict)
    AUTOBAN = 10

async def check_bot_started_users(user, event):
    if user.id == Config.OWNER_ID:
        return
    check = get_starter_details(user.id)
    usernaam = f"@{user.username}" if user.username else "لايوجـد"
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"<b>مرحبـاً سيـدي 🧑🏻‍💻</b>\n<b>شخـص قام بالدخـول لـ البـوت المسـاعـد 💡</b>\n\n<b>الاسـم : </b>{get_display_name(user)}\n<b>الايـدي : </b><code>{user.id}</code>\n<b>اليـوزر :</b> {usernaam}"
    else:
        start_date = check.date
        notification = f"<b>مرحبـاً سيـدي 🧑🏻‍💻</b>\n<b>شخـص قام بالدخـول لـ البـوت المسـاعـد 💡</b>\n\n<b>الاسـم : </b>{get_display_name(user)}\n<b>الايـدي : </b><code>{user.id}</code>\n<b>اليـوزر :</b> {usernaam}"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, notification, parse_mode='html')

@l313l.bot_cmd(
    pattern=f"^/start({botusername})?([\\s]+)?$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start(event):
    chat = await event.get_chat()
    user = await l313l.get_me()
    if check_is_black_list(chat.id):
        return
    if int(chat.id) in kk:
        kk.remove(int(chat.id))
    reply_to = await event.get_reply_message()
    reply_to_id = reply_to.id if reply_to else None

    mention = f'<a href="tg://user?id={chat.id}">{chat.first_name}</a>'
    my_fullname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name

    zz_txt = "• المـطـور •"
    zz_ch = gvarstatus("START_BUTUN") or (user.username if user.username else "aqhvv")
    custompic = gvarstatus("BOT_START_PIC") or None

    PREMIUM_EMOJI_ID = 5210763312597326700
    EMOJI_HEART = 5258215850745275216
    EMOJI_WARN = 5350477112677515642
    EMOJI_Fatf = 5188619457651567219

    start_msg = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">✨</tg-emoji> <b>⌔ مـرحباً بـك عزيـزي  {mention} </b>

<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">🤖</tg-emoji> <b>انـا البـوت الخـاص بـ</b> <code>{my_fullname}</code>

❶ <b>التواصـل مـع مـالكـي مـن هنـا</b> <tg-emoji emoji-id="{EMOJI_HEART}">💌</tg-emoji>
❷ <b>فَضفـضه بَهوية مجهولـة</b> <tg-emoji emoji-id="{EMOJI_Fatf}">✉️</tg-emoji>
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👇</tg-emoji> <b>لـ البـدء إستخـدم الازرار بالاسفـل</b>'''

    # الأزرار الرئيسية (بدون زر الحذف)
    buttons = [
        [{"text": "اضغـط لـ التواصـل", "callback_data": "contact_menu", "style": "primary", "icon_custom_emoji_id": EMOJI_CONTACT}],
        [{"text": "فَضفضة بَهوية مجهولـة", "callback_data": "whisper_menu", "style": "success", "icon_custom_emoji_id": EMOJI_fatfta}],
        [{"text": zz_txt, "url": f"https://t.me/{zz_ch}", "style": "primary", "icon_custom_emoji_id": EMOJI_CHANNEL}]
    ]

    try:
        if custompic:
            await event.client.send_file(
                chat.id,
                file=custompic,
                caption='<b>🎉 مرحباً بك في البوت المساعد</b>',
                link_preview=False,
                reply_to=reply_to_id,
                parse_mode='html'
            )
        send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendMessage"
        send_data = {
            "chat_id": chat.id,
            "text": start_msg,
            "parse_mode": "HTML",
            "reply_markup": json.dumps({"inline_keyboard": buttons}),
            "disable_web_page_preview": True,
            "message_effect_id": EFFECT_ID
        }
        response = requests.post(send_url, json=send_data, timeout=3)
        if response.status_code != 200:
            fallback_buttons = []
            for row in buttons:
                btn_row = []
                for btn in row:
                    if "url" in btn:
                        btn_row.append(Button.url(btn["text"], btn["url"]))
                    else:
                        btn_row.append(Button.inline(btn["text"], data=btn["callback_data"]))
                fallback_buttons.append(btn_row)
            await event.reply(start_msg, buttons=fallback_buttons, parse_mode='html', link_preview=False)
    except Exception as e:
        LOGS.error(f"خطأ في إرسال رسالة البداية: {str(e)}")

    await check_bot_started_users(chat, event)

@l313l.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):
    chat = await event.get_chat()
    reply_to = await event.get_reply_message()
    reply_to_id = reply_to.id if reply_to else None
    if check_is_black_list(chat.id) or event.contact or int(chat.id) in kk:
        return
    if event.text and event.text.startswith("/start"):
        if chat.id in tt or chat.id in whisper_users:
            return
    if chat.id != Config.OWNER_ID:
        if event.text and event.text.startswith("/cancle"):
            for lst in [kk, tt, whisper_users]:
                if chat.id in lst:
                    lst.remove(chat.id)
            return await event.client.send_message(chat.id, "**- تم الالغـاء .. بنجـاح**", reply_to=reply_to_id)

        # وضع الفضفضة
        if chat.id in whisper_users:
            sent_msg = await event.client.send_message(
                Config.OWNER_ID,
                f"**💭 رسالة فضفضة:**\n\n{event.text}",
                parse_mode='md'
            )
            try:
                add_user_to_db(sent_msg.id, get_display_name(chat), chat.id, event.id, 0)
            except Exception as e:
                LOGS.error(str(e))
            user = await l313l.get_me()
            my_mention = f"[{user.first_name}](tg://user?id={user.id})"
            mention = f"[{chat.first_name}](tg://user?id={chat.id})"
            whisper_msg = f"""**⌔ عـزيـزي  {mention} **                            
**⌔ تم ارسـال رسالتـك لـ {my_mention} 💌**                            
**⌔ دون اضهار هويتك .**"""
            buttons = [[Button.inline("❌ تعطيل وضع الفضفضة", data="whisper_off")]]
            await event.client.send_message(chat.id, whisper_msg, buttons=buttons, reply_to=reply_to_id, link_preview=False)
            return

        # وضع التواصل العادي
        if chat.id in tt:
            msg = await event.forward_to(Config.OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0)
            except Exception as e:
                LOGS.error(str(e))
            user = await l313l.get_me()
            mention = f"[{chat.first_name}](tg://user?id={chat.id})"
            my_fullname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            tas_msg = f"""**⌔ عـزيـزي  {mention} **                            
**⌔ تم ارسـال رسالتـك لـ {my_fullname} 💌**                            
**⌔ تحلى بالصبـر وانتظـر الـرد 📨.**"""
            buttons = [[Button.inline("تعطيـل التواصـل", data="ttk_bot-off")]]
            await event.client.send_message(chat.id, tas_msg, buttons=buttons, reply_to=reply_to_id, link_preview=False)
            return

@l313l.tgbot.on(events.CallbackQuery())
async def callback_handler(event):
    data = event.data.decode()
    chat_id = event.chat_id

    # --- القائمة الفرعية للتواصل ---
    if data == "contact_menu":
        buttons = [
            [Button.inline("✅ تفعيل التواصل", data="contact_on", style="primary")],
            [Button.inline("❌ تعطيل التواصل", data="contact_off", style="danger")],
            [Button.inline("↩️ رجوع", data="back_to_start", style="secondary")]
        ]
        await event.edit("**اختر خياراً للتواصل:**", buttons=buttons)

    elif data == "contact_on":
        if chat_id not in tt:
            tt.append(chat_id)
            await event.answer("✅ تم تفعيل وضع التواصل. أرسل رسالتك.", alert=True)
        else:
            await event.answer("✅ وضع التواصل مفعل بالفعل.", alert=True)
        await event.delete()

    elif data == "contact_off":
        if chat_id in tt:
            tt.remove(chat_id)
            await event.answer("❌ تم تعطيل وضع التواصل.", alert=True)
        else:
            await event.answer("❌ وضع التواصل غير مفعل أصلاً.", alert=True)
        await event.delete()

    # --- القائمة الفرعية للفضفضة ---
    elif data == "whisper_menu":
        buttons = [
            [Button.inline("✅ تفعيل الفضفضة", data="whisper_on", style="primary")],
            [Button.inline("❌ تعطيل الفضفضة", data="whisper_off", style="danger")],
            [Button.inline("↩️ رجوع", data="back_to_start", style="secondary")]
        ]
        await event.edit("**اختر خياراً للفضفضة:**", buttons=buttons)

    elif data == "whisper_on":
        if chat_id not in whisper_users:
            whisper_users.append(chat_id)
            await event.answer("✅ تم تفعيل وضع الفضفضة. أرسل رسالتك.", alert=True)
        else:
            await event.answer("✅ وضع الفضفضة مفعل بالفعل.", alert=True)
        await event.delete()

    elif data == "whisper_off":
        if chat_id in whisper_users:
            whisper_users.remove(chat_id)
            await event.answer("❌ تم تعطيل وضع الفضفضة.", alert=True)
        else:
            await event.answer("❌ وضع الفضفضة غير مفعل أصلاً.", alert=True)
        await event.delete()

    # --- رجوع إلى الرسالة الرئيسية ---
    elif data == "back_to_start":
        await event.delete()
        # إعادة إرسال /start (يمكن استدعاء الأمر مباشرة)
        await event.client.send_message(chat_id, "/start")

    # --- الأزرار القديمة للتعطيل من داخل المحادثة (تبقى كما هي) ---
    elif data == "ttk_bot-off":
        if chat_id in tt:
            tt.remove(chat_id)
            await event.answer("❌ تم تعطيل وضع التواصل.", alert=True)
        else:
            await event.answer("❌ وضع التواصل غير مفعل.", alert=True)
        await event.delete()

    elif data == "whisper_off":
        if chat_id in whisper_users:
            whisper_users.remove(chat_id)
            await event.answer("❌ تم تعطيل وضع الفضفضة.", alert=True)
        else:
            await event.answer("❌ وضع الفضفضة غير مفعل.", alert=True)
        await event.delete()
