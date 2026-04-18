# -*- coding: utf-8 -*-
import re
import random
import json
import requests
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union

from telethon import Button, events
from telethon.errors import UserIsBlockedError
from telethon.events import CallbackQuery, StopPropagation
from telethon.utils import get_display_name

from . import Config, l313l

from ..core import check_owner, pool
from ..core.logger import logging
from ..core.session import tgbot
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from ..sql_helper.globals import delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import ban_user_from_bot

LOGS = logging.getLogger(__name__)

plugin_category = "utils"
botusername = Config.TG_BOT_USERNAME
Zel_Uid = l313l.uid
dd = []
kk = []
tt = []
arabic_decor_users = []

# إيموجي بريميوم - بدون أسماء ألوان، بأسماء الأزرار
EMOJI_CONTACT = "5258215850745275216"      # ✨ لزر التواصل
EMOJI_DECOR = "5411580731929411768"        # ✅ لزر الزخرفة
EMOJI_DELETE = "5350477112677515642"       # 🔥 لزر الحذف
EMOJI_PAID = "5408997493784467607"         # 💎 لزر المدفوع
EMOJI_CHANNEL = "5260450573768990626"      # ✨ لزر القناة
EMOJI_fatfta = "5188619457651567219"        # فضفضه

# إيموجي بريميوم للتأثيرات
EFFECT_ID = "5046509860389126442"  # التأثير الذي طلبته

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
    reply_to = await reply_id(event)
    
    # استخدام HTML للجميع
    mention = f'<a href="tg://user?id={chat.id}">{chat.first_name}</a>'
    my_mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
    
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = user.first_name
    my_last = user.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    
    if gvarstatus("START_BUTUN") is not None:
        zz_txt = "• المـطـور •"
        zz_ch = gvarstatus("START_BUTUN")
    elif user.username:
        zz_txt = "• المـطـور •"
        zz_ch = user.username
    else:
        zz_txt = "• المـطـور •"
        zz_ch = "aqhvv"
    
    zid = 5427469031
    if gvarstatus("ZThon_Vip") is None:
        zid = 5427469031
    else:
        zid = int(gvarstatus("ZThon_Vip"))
    
    custompic = gvarstatus("BOT_START_PIC") or None
  
    # أولاً: تعريف الإيموجيات الخاصة بالنص (إذا لم تكن موجودة)
    PREMIUM_EMOJI_ID = 5210763312597326700  # ✨
    EMOJI_HEART = 5258215850745275216        # 💌
    EMOJI_ART = 5411580731929411768        # 🎨
    EMOJI_WARN = 5350477112677515642
    EMOJI_Fatf = 5188619457651567219
    start_msg = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">✨</tg-emoji> <b>⌔ مـرحباً بـك عزيـزي  {mention} </b>

<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">🤖</tg-emoji> <b>انـا البـوت الخـاص بـ</b> <code>{my_fullname}</code>

❶ <b>التواصـل مـع مـالكـي مـن هنـا</b> <tg-emoji emoji-id="{EMOJI_HEART}">💌</tg-emoji>
من خـلال زر <b>اضغـط لـ التواصـل</b>
❷ <b>زخـرفـة النصـوص والأسمـاء</b> <tg-emoji emoji-id="{EMOJI_ART}">🎨</tg-emoji>
❸ <b>حـذف الحسـابات نهـائياً</b> <tg-emoji emoji-id="{EMOJI_WARN}">⚠️</tg-emoji>
❹ <b>فَضفـضه بَهوية مجهولـة</b> <tg-emoji emoji-id="{EMOJI_Fatf}">✉️</tg-emoji>
﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👇</tg-emoji> <b>لـ البـدء إستخـدم الازرار بالاسفـل</b>'''


    # ============================================
    # ✅ الأزرار حسب نوع المستخدم
    # ============================================
    
    # 1️⃣ أزرار المالك الأساسي
    if chat.id == Config.OWNER_ID and chat.id != zid:
        buttons = [
            [
                {
                    "text": "زخـارف تمبلـر",  # بدون إيموجي في النص
                    "callback_data": "decor_main_menu",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_DECOR  # ✅ الإيموجي داخل الزر
                }
            ],
            [
                {
                    "text": "لـ حـذف حسـابك",  # بدون إيموجي في النص
                    "callback_data": "zzk_bot-5",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_DELETE  # 🔥 الإيموجي داخل الزر
                }
            ]
        ]
    
    # 2️⃣ أزرار المطورين المميزين
    elif chat.id == Config.OWNER_ID and chat.id == zid:
        buttons = [
            [
                {
                    "text": "زخـارف تمبلـر",
                    "callback_data": "decor_main_menu",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_DECOR
                }
            ],
            [
                {
                    "text": "لـ حـذف حسـابك",
                    "callback_data": "zzk_bot-5",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_DELETE
                }
            ],
            [
                {
                    "text": zz_txt,
                    "url": f"https://t.me/{zz_ch}",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_CHANNEL
                }
            ]
        ]
    
    # 3️⃣ أزرار العامة (المستخدمين العاديين)
    else:
        buttons = [
            [
                {
                    "text": "اضغـط لـ التواصـل",
                    "callback_data": "ttk_bot-1",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_CONTACT
                }
            ],
            [
                {
                    "text": "فَضفضة بَهوية مجهولـة",
                    "callback_data": "whisper_menu",
                    "style": "success",
                    "icon_custom_emoji_id": EMOJI_fatfta
                }
            ],
            [
                {
                    "text": "لـ حـ.ـذف حسـابك",
                    "callback_data": "zzk_bot-5",
                    "style": "Danger",
                    "icon_custom_emoji_id": EMOJI_DELETE
                }
            ],
            [
                {
                    "text": "زخـارف تمبلـر",
                    "callback_data": "decor_main_menu",
                    "style": "success",
                    "icon_custom_emoji_id": EMOJI_DECOR
                }
            ],
            [
                {
                    "text": zz_txt,
                    "url": f"https://t.me/{zz_ch}",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_CHANNEL
                }
            ]
        ]
    
    # إرسال الرسالة عبر Bot API
    try:
        if custompic:
            await event.client.send_file(
                chat.id,
                file=custompic,
                caption='<b>🎉 مرحباً بك في البوت المساعد</b>',
                link_preview=False,
                reply_to=reply_to,
                parse_mode='html'
            )
            
        send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendMessage"
        send_data = {
            "chat_id": chat.id,
            "text": start_msg,
            "parse_mode": "HTML",
            "reply_markup": json.dumps({"inline_keyboard": buttons}),
            "disable_web_page_preview": True,
            "message_effect_id": EFFECT_ID  # ✅ استخدام المتغير
        }
        
        response = requests.post(send_url, json=send_data, timeout=3)
        if response.status_code == 200:
            pass
        else:
            # Fallback
            fallback_buttons = []
            for row in buttons:
                btn_row = []
                for btn in row:
                    if "url" in btn:
                        btn_row.append(Button.url(btn["text"], btn["url"]))
                    else:
                        btn_row.append(Button.inline(btn["text"], data=btn["callback_data"]))
                fallback_buttons.append(btn_row)
            
            await event.reply(
                start_msg,
                buttons=fallback_buttons,
                parse_mode='html',
                link_preview=False
            )
            
    except Exception as e:
        LOGS.error(f"❌ خطأ في إرسال رسالة البداية: {str(e)}")
        # Fallback
        fallback_buttons = []
        for row in buttons:
            btn_row = []
            for btn in row:
                if "url" in btn:
                    btn_row.append(Button.url(btn["text"], btn["url"]))
                else:
                    btn_row.append(Button.inline(btn["text"], data=btn["callback_data"]))
            fallback_buttons.append(btn_row)
        
        await event.reply(
            start_msg,
            buttons=fallback_buttons,
            parse_mode='html',
            link_preview=False
        )

    await check_bot_started_users(chat, event)

@l313l.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):  # sourcery no-metrics
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    if check_is_black_list(chat.id):
        return
    if event.contact or int(chat.id) in kk:
        return

    if event.text and event.text.startswith("/start"):
        if chat.id in tt or chat.id in whisper_users:
            return
    if chat.id != Config.OWNER_ID:
        if event.text.startswith("/cancle"):
            if int(chat.id) in dd:
                dd.remove(int(chat.id))
            if int(chat.id) in kk:
                kk.remove(int(chat.id))
            zzc = "**- تم الالغـاء .. بنجـاح**"
            return await event.client.send_message(
                chat.id,
                zzc,
                link_preview=False,
                reply_to=reply_to,
            )
        
        # ========== وضع الفضفضة (مع تخزين) ==========
        if chat.id in whisper_users:
            # إرسال للمالك كرسالة عادية (مش محولة)
            sent_msg = await event.client.send_message(
                Config.OWNER_ID,
                f"**💭 رسالة فضفضة:**\n\n{event.text}",
                parse_mode='md'
            )
            
            # تخزين المعلومات في قاعدة البيانات (زي التواصل)
            try:
                add_user_to_db(
                    sent_msg.id,           # message_id
                    get_display_name(chat), # first_name
                    chat.id,                # chat_id
                    event.id,               # logger_id (الرسالة الأصلية)
                    0,                      # result_id (مبدئي)
                    0                       # نضيفها بعد الرد
                )
            except Exception as e:
                LOGS.error(str(e))
            
            # رسالة التأكيد للمستخدم
            user = await l313l.get_me()
            my_mention = f"[{user.first_name}](tg://user?id={user.id})"
            mention = f"[{chat.first_name}](tg://user?id={chat.id})"
            
            whisper_msg = f"""**⌔ عـزيـزي  {mention} **                            
**⌔ تم ارسـال رسالتـك لـ {my_mention} 💌**                            
**⌔ دون اضهار هويتك .**"""

            buttons = [
                [Button.inline("❌ تعطيل وضع الفضفضة", data="whisper_off")]
            ]
            
            await event.client.send_message(
                chat.id,
                whisper_msg,
                buttons=buttons,
                reply_to=reply_to,
                link_preview=False
            )
            return
        # ===========================================
        
        # ========== وضع التواصل العادي ==========
        if int(chat.id) in tt:
            msg = await event.forward_to(Config.OWNER_ID)
            chat = await event.get_chat()
            user = await l313l.get_me()
            mention = f"[{chat.first_name}](tg://user?id={chat.id})"
            my_mention = f"[{user.first_name}](tg://user?id={user.id})"
            first = chat.first_name
            last = chat.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{chat.username}" if chat.username else mention
            userid = chat.id
            my_first = user.first_name
            my_last = user.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{user.username}" if user.username else my_mention
            if gvarstatus("START_BUTUN") is not None:
                zz_txt = "⌔ قنـاتـي ⌔"
                zz_ch = gvarstatus("START_BUTUN")
            elif user.username:
                zz_txt = "⌔ لـ التواصـل خـاص ⌔"
                zz_ch = user.username
            else:
                zz_txt = "⌔ قنـاة المـطور ⌔"
                zz_ch = "aqhvv"
            customtasmsg = gvarstatus("TAS_TEXT") or None
            if customtasmsg is not None:
                tas_msg = customtasmsg.format(
                    zz_mention=mention,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_zname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                )
            else:
                tas_msg = f"""**⌔ عـزيـزي  {mention} **                            
**⌔ تم ارسـال رسالتـك لـ {my_fullname} 💌**                            
**⌔ تحلى بالصبـر وانتظـر الـرد 📨.**"""
            buttons = [
                [
                    Button.inline("تعطيـل التواصـل", data="ttk_bot-off")
                ]
            ]
            await event.client.send_message(
                chat.id,
                tas_msg,
                link_preview=False,
                buttons=buttons,
                reply_to=reply_to,
            )
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
            return
        # ======================================
        
        # ========== وضع الزخرفة ==========
        if chat.id in dd:
            text = event.text
            iitems = ['࿐', '𖣳', '𓃠', '𖡟', '𖠜', '‌♡⁩', '‌༗', '‌𖢖', '❥', '‌ঌ', '𝆹𝅥𝅮', '𖠜', '𖠲', '𖤍', '𖠛', ' 𝅘𝅥𝅮', '‌༒', '‌ㇱ', '߷', 'メ', '〠', '𓃬', '𖠄']
            smiile1 = random.choice(iitems)
            smiile2 = random.choice(iitems)
            smiile3 = random.choice(iitems)
            smiile4 = random.choice(iitems)
            smiile5 = random.choice(iitems)
            smiile6 = random.choice(iitems)
            smiile7 = random.choice(iitems)
            smiile8 = random.choice(iitems)
            smiile9 = random.choice(iitems)
            smiile10 = random.choice(iitems)
            smiile11 = random.choice(iitems)
            smiile12 = random.choice(iitems)
            smiile13 = random.choice(iitems)
            smiile14 = random.choice(iitems)
            smiile15 = random.choice(iitems)
            smiile16 = random.choice(iitems)
            smiile17 = random.choice(iitems)
            smiile18 = random.choice(iitems)
            smiile19 = random.choice(iitems)
            smiile20 = random.choice(iitems)
            smiile21 = random.choice(iitems)
            smiile22 = random.choice(iitems)
            smiile23 = random.choice(iitems)
            smiile24 = random.choice(iitems)
            smiile25 = random.choice(iitems)
            smiile26 = random.choice(iitems)
            smiile27 = random.choice(iitems)
            smiile28 = random.choice(iitems)
            smiile29 = random.choice(iitems)
            smiile30 = random.choice(iitems)
            smiile31 = random.choice(iitems)
            smiile32 = random.choice(iitems)
            smiile33 = random.choice(iitems)
            smiile34 = random.choice(iitems)
            smiile35 = random.choice(iitems)
            smiile36 = random.choice(iitems)
            smiile37 = random.choice(iitems)
            smiile38 = random.choice(iitems)
            smiile39 = random.choice(iitems)
            smiile40 = random.choice(iitems)
            

            WA1 = text.replace('a', 'ᵃ').replace('A', 'ᴬ').replace('b', 'ᵇ').replace('B', 'ᴮ').replace('c', 'ᶜ').replace('C', 'ᶜ').replace('d', 'ᵈ').replace('D', 'ᴰ').replace('e', 'ᵉ').replace('E', 'ᴱ').replace('f', 'ᶠ').replace('F', 'ᶠ').replace('g', 'ᵍ').replace('G', 'ᴳ').replace('h', 'ʰ').replace('H', 'ᴴ').replace('i', 'ⁱ').replace('I', 'ᴵ').replace('j', 'ʲ').replace('J', 'ᴶ').replace('k', 'ᵏ').replace('K', 'ᴷ').replace('l', 'ˡ').replace('L', 'ᴸ').replace('m', 'ᵐ').replace('M', 'ᴹ').replace('n', 'ⁿ').replace('N', 'ᴺ').replace('o', 'ᵒ').replace('O', 'ᴼ').replace('p', 'ᵖ').replace('P', 'ᴾ').replace('q', '۩').replace('Q', 'Q').replace('r', 'ʳ').replace('R', 'ᴿ').replace('s', 'ˢ').replace('S', 'ˢ').replace('t', 'ᵗ').replace('T', 'ᵀ').replace('u', 'ᵘ').replace('U', 'ᵁ').replace('v', 'ⱽ').replace('V', 'ⱽ').replace('w', 'ʷ').replace('W', 'ᵂ').replace('x', 'ˣ').replace('X', 'ˣ').replace('y', 'ʸ').replace('Y', 'ʸ').replace('z', 'ᶻ').replace('Z', 'ᶻ')
            WA2 = text.replace('a', 'ᴀ').replace('b', 'ʙ').replace('c', 'ᴄ').replace('d', 'ᴅ').replace('e', 'ᴇ').replace('f', 'ғ').replace('g', 'ɢ').replace('h', 'ʜ').replace('i', 'ɪ').replace('j', 'ᴊ').replace('k', 'ᴋ').replace('l', 'ʟ').replace('m', 'ᴍ').replace('n', 'ɴ').replace('o', 'ᴏ').replace('p', 'ᴘ').replace('q', 'ǫ').replace('r', 'ʀ').replace('s', 's').replace('t', 'ᴛ').replace('u', 'ᴜ').replace('v', 'ᴠ').replace('w', 'ᴡ').replace('x', 'x').replace('y', 'ʏ').replace('z', 'ᴢ').replace('A', 'ᴀ').replace('B', 'ʙ').replace('C', 'ᴄ').replace('D', 'ᴅ').replace('E', 'ᴇ').replace('F', 'ғ').replace('G', 'ɢ').replace('H', 'ʜ').replace('I', 'ɪ').replace('J', 'ᴊ').replace('K', 'ᴋ').replace('L', 'ʟ').replace('M', 'ᴍ').replace('N', 'ɴ').replace('O', 'ᴏ').replace('P', 'ᴘ').replace('Q', 'ǫ').replace('R', 'ʀ').replace('S', 'S').replace('T', 'ᴛ').replace('U', 'ᴜ').replace('V', 'ᴠ').replace('W', 'ᴡ').replace('X', 'X').replace('Y', 'ʏ').replace('Z', 'ᴢ')
            WA3 = text.replace('a','α').replace("b","в").replace("c","c").replace("d","∂").replace("e","ε").replace("E","ғ").replace("g","g").replace("h","н").replace("i","ι").replace("j","נ").replace("k","к").replace("l","ℓ").replace("m","м").replace("n","η").replace("o","σ").replace("p","ρ").replace("q","q").replace("r","я").replace("s","s").replace("t","т").replace("u","υ").replace("v","v").replace("w","ω").replace("x","x").replace("y","ү").replace("z","z").replace("A","α").replace("B","в").replace("C","c").replace("D","∂").replace("E","ε").replace("E","ғ").replace("G","g").replace("H","н").replace("I","ι").replace("J","נ").replace("K","к").replace("L","ℓ").replace("M","м").replace("N","η").replace("O","σ").replace("P","ρ").replace("Q","q").replace("R","я").replace("S","s").replace("T","т").replace("U","υ").replace("V","v").replace("W","ω").replace("X","X").replace("Y","ү").replace("Z","z")
            WA4 = text.replace('a','ᥲ').replace('b','ხ').replace('c','ᥴ').replace('d','ძ').replace('e','ᥱ').replace('f','ƒ').replace('g','ᘜ').replace('h','ɦ').replace('i','Ꭵ').replace('j','᧒').replace('k','ƙ').replace('l','ᥣ').replace('m','ꪔ').replace('n','ꪀ').replace('o','᥆').replace('p','ρ').replace('q','ᑫ').replace('r','ᖇ').replace('s','᥉').replace('t','ƚ').replace('u','ᥙ').replace('v','᥎').replace('w','᭙').replace('x','ꪎ').replace('y','ᥡ').replace('z','ᤁ').replace('A','ᥲ').replace('B','ხ').replace('C','ᥴ').replace('D','ძ').replace('E','ᥱ').replace('F','ƒ').replace('G','ᘜ').replace('H','ɦ').replace('I','Ꭵ').replace('J','᧒').replace('K','ƙ').replace('L','ᥣ').replace('M','ꪔ').replace('N','ꪀ').replace('O','᥆').replace('P','ρ').replace('Q','ᑫ').replace('R','ᖇ').replace('S','᥉').replace('T','ƚ').replace('U','ᥙ').replace('V','᥎').replace('W','᭙').replace('X','ꪎ').replace('Y','ᥡ').replace('Z','ᤁ')
            WA5 = text.replace('a','ُِᥲ').replace('b','َِხ').replace('c','ُِᥴ').replace('d','ُძ').replace('e','ُِᥱ').replace('f','َِƒ').replace('g','ᘜ').replace('h','َِɦ').replace('i','َِᎥ').replace('j','َِ᧒').replace('k','َِƙ').replace('l','َِᥣ').replace('m','ُِꪔ').replace('n','َِꪀ').replace('o','ُِ᥆').replace('p','ُِρ').replace('q','ُᑫ').replace('r','َِᖇ').replace('s','َِ᥉').replace('t','َِƚ').replace('u','ُِᥙ').replace('v','ُِ᥎').replace('w','ِ᭙').replace('x','َِꪎ').replace('y','ِᥡ').replace('z','ُِᤁ').replace('A','ُِᥲ').replace('B','َِხ').replace('C','ُِᥴ').replace('D','ُძ').replace('E','ُِᥱ').replace('F','َِƒ').replace('G','ᘜ').replace('H','َِɦ').replace('I','َِᎥ').replace('J','َِ᧒').replace('K','َِƙ').replace('L','َِᥣ').replace('M','ُِꪔ').replace('N','َِꪀ').replace('O','ُِ᥆').replace('P','ُِρ').replace('Q','ُᑫ').replace('R','َِᖇ').replace('S','َِ᥉').replace('T','َِƚ').replace('U','ُِᥙ').replace('V','ُِ᥎').replace('W','ِ᭙').replace('X','َِꪎ').replace('Y','ِᥡ').replace('Z','ُِᤁ')
            WA6 = text.replace('a','ꪖ').replace('b','Ⴆ').replace('c','ᥴ').replace('d','ᦔ').replace('e','꧖').replace('f','ƒ').replace('g','ᧁ').replace('h','ꫝ').replace('i','Ꭵ').replace('j','᧒').replace('k','ƙ').replace('l','ᥣ').replace('m','᧗').replace('n','ᥒ').replace('o','᥆').replace('p','ρ').replace('q','ᑫ').replace('r','ᖇ').replace('s','᥉').replace('t','ﾋ').replace('u','ꪊ').replace('v','ꪜ').replace('w','ꪝ').replace('x','ꪎ').replace('y','ꪗ').replace('z','ᤁ').replace('A','ꪖ').replace('B','Ⴆ').replace('C','ᥴ').replace('D','ᦔ').replace('E','꧖').replace('F','ƒ').replace('G','ᧁ').replace('H','ꫝ').replace('I','Ꭵ').replace('J','᧒').replace('K','ƙ').replace('L','ᥣ').replace('M','᧗').replace('N','ᥒ').replace('O','᥆').replace('P','ρ').replace('Q','ᑫ').replace('R','ᖇ').replace('S','᥉').replace('T','ﾋ').replace('U','ꪊ').replace('V','ꪜ').replace('W','ꪝ').replace('X','ꪎ').replace('Y','ꪗ').replace('Z','ᤁ')
            WA7 = text.replace('a','ُِꪖ').replace('b','َِႦ').replace('c','َِᥴ').replace('d','ُِᦔ').replace('e','ُِ꧖').replace('f','َِƒ').replace('g','ُِᧁ').replace('h','َِꫝ').replace('i','ُِᎥ').replace('j','َِ᧒').replace('k','ُِƙ').replace('l','َِᥣ').replace('m','َِ᧗').replace('n','َِᥒ').replace('o','َِ᥆').replace('p','َِρ').replace('q','ُِᑫ').replace('r','َِᖇ').replace('s','َِ᥉').replace('t','َِﾋ').replace('u','َِꪊ').replace('v','ُِꪜ').replace('w','ُِꪝ').replace('x','َِꪎ').replace('y','ُِꪗ').replace('z','ُِᤁ').replace('A','ُِꪖ').replace('B','َِႦ').replace('C','َِᥴ').replace('D','ُِᦔ').replace('E','ُِ꧖').replace('F','َِƒ').replace('G','ُِᧁ').replace('H','َِꫝ').replace('I','ُِᎥ').replace('J','َِ᧒').replace('K','ُِƙ').replace('L','َِᥣ').replace('M','َِ᧗').replace('N','َِᥒ').replace('O','َِ᥆').replace('P','َِρ').replace('Q','ُِᑫ').replace('R','َِᖇ').replace('S','َِ᥉').replace('T','َِﾋ').replace('U','َِꪊ').replace('V','ُِꪜ').replace('W','ُِꪝ').replace('X','َِꪎ').replace('Y','ُِꪗ').replace('Z','ُِᤁ')
            WA8 = text.replace('a','ᗩ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗪ').replace('e','ᗴ').replace('f','ᖴ').replace('g','ᘜ').replace('h','ᕼ').replace('i','I').replace('j','ᒍ').replace('k','K').replace('l','ᒪ').replace('m','ᗰ').replace('n','ᑎ').replace('o','O').replace('p','ᑭ').replace('q','ᑫ').replace('r','ᖇ').replace('s','Տ').replace('t','T').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Y').replace('z','ᘔ').replace('A','ᗩ').replace('B','ᗷ').replace('C','ᑕ').replace('D','ᗪ').replace('E','ᗴ').replace('F','ᖴ').replace('G','ᘜ').replace('H','ᕼ').replace('I','I').replace('J','ᒍ').replace('K','K').replace('L','ᒪ').replace('M','ᗰ').replace('N','ᑎ').replace('O','O').replace('P','ᑭ').replace('Q','ᑫ').replace('R','ᖇ').replace('S','Տ').replace('T','T').replace('U','ᑌ').replace('V','ᐯ').replace('W','ᗯ').replace('X','᙭').replace('Y','Y').replace('Z','ᘔ')
            WA9 = text.replace('a','𝚊').replace('b','𝚋').replace('c','𝚌').replace('d','𝚍').replace('e','𝚎').replace('f','𝚏').replace('g','𝚐').replace('h','𝚑').replace('i','𝚒').replace('j','𝚓').replace('k','𝚔').replace('l','𝚕').replace('m','𝚖').replace('n','𝚗').replace('o','𝚘').replace('p','𝚙').replace('q','𝚚').replace('r','𝚛').replace('s','𝚜').replace('t','𝚝').replace('u','𝚞').replace('v','𝚟').replace('w','𝚠').replace('x','𝚡').replace('y','𝚢').replace('z','𝚣').replace('A','𝙰').replace('B','𝙱').replace('C','𝙲').replace('D','𝙳').replace('E','𝙴').replace('F','𝙵').replace('G','𝙶').replace('H','𝙷').replace('I','𝙸').replace('J','𝙹').replace('K','𝙺').replace('L','𝙻').replace('M','𝙼').replace('N','𝙽').replace('O','𝙾').replace('P','𝙿').replace('Q','𝚀').replace('R','𝚁').replace('S','𝚂').replace('T','𝚃').replace('U','𝚄').replace('V','𝚅').replace('W','𝚆').replace('X','𝚇').replace('Y','𝚈').replace('Z','𝚉')
            WA10 = text.replace('a','α').replace('b','𝖻').replace('c','ᥴ').replace('d','ძ').replace('e','𝖾').replace('f','𝖿').replace('g','𝗀').replace('h','h').replace('i','Ꭵ').replace('j','𝖩').replace('k','𝗄').replace('l','𝗅').replace('m','𝗆').replace('n','ᥒ').replace('o','᥆').replace('p','𝗉').replace('q','𝗊').replace('r','𝗋').replace('s','𝗌').replace('t','𝗍').replace('u','ᥙ').replace('v','᥎').replace('w','ᥕ').replace('x','ꪎ').replace('y','𝗒').replace('z','ᤁ').replace('A','α').replace('B','𝖻').replace('C','ᥴ').replace('D','ძ').replace('E','𝖾').replace('F','𝖿').replace('G','𝗀').replace('H','h').replace('I','Ꭵ').replace('J','𝖩').replace('K','𝗄').replace('L','𝗅').replace('M','𝗆').replace('N','ᥒ').replace('O','᥆').replace('P','𝗉').replace('Q','𝗊').replace('R','𝗋').replace('S','𝗌').replace('T','𝗍').replace('U','ᥙ').replace('V','᥎').replace('W','ᥕ').replace('X','ꪎ').replace('Y','𝗒').replace('Z','ᤁ')
            WA11 = text.replace('a','𝖺').replace('b','𝖻').replace('c','𝖼').replace('d','𝖽').replace('e','𝖾').replace('f','𝖿').replace('g','𝗀').replace('h','𝗁').replace('i','𝗂').replace('j','𝗃').replace('k','𝗄').replace('l','𝗅').replace('m','𝗆').replace('n','𝗇').replace('o','𝗈').replace('p','𝗉').replace('q','𝗊').replace('r','𝗋').replace('s','𝗌').replace('t','𝗍').replace('u','𝗎').replace('v','𝗏').replace('w','𝗐').replace('x','x').replace('y','𝗒').replace('z','ᴢ').replace('A','𝖠').replace('B','𝖡').replace('C','𝖢').replace('D','𝖣').replace('E','𝖤').replace('F','𝖥').replace('G','𝖦').replace('H','𝖧').replace('I','𝖨').replace('J','𝖩').replace('K','𝖪').replace('L','𝖫').replace('M','𝖬').replace('N','𝖭').replace('O','𝖮').replace('P','𝖯').replace('Q','𝖰').replace('R','𝖱').replace('S','𝖲').replace('T','𝖳').replace('U','𝖴').replace('V','𝖵').replace('W','𝖶').replace('X','𝖷').replace('Y','𝖸').replace('Z','𝖹')
            WA12 = text.replace('a','𝙰').replace('b','𝙱').replace('c','𝙲').replace('d','𝙳').replace('e','𝙴').replace('f','𝙵').replace('g','𝙶').replace('h','𝙷').replace('i','𝙸').replace('j','𝚓').replace('k','𝙺').replace('l','𝙻').replace('m','𝙼').replace('n','𝙽').replace('o','𝙾').replace('p','𝙿').replace('q','𝚀').replace('r','𝚁').replace('s','𝚂').replace('t','𝚃').replace('u','𝚄').replace('v','??').replace('w','𝚆').replace('x','𝚇').replace('y','𝚈').replace('z','𝚉').replace('A','𝙰').replace('B','𝙱').replace('C','𝙲').replace('D','𝙳').replace('E','𝙴').replace('F','𝙵').replace('G','𝙶').replace('H','𝙷').replace('I','𝙸').replace('J','𝚓').replace('K','𝙺').replace('L','𝙻').replace('M','𝙼').replace('N','𝙽').replace('O','𝙾').replace('P','𝙿').replace('Q','𝚀').replace('R','𝚁').replace('S','𝚂').replace('T','𝚃').replace('U','𝚄').replace('V','𝚅').replace('W','𝚆').replace('X','𝚇').replace('Y','𝚈').replace('Z','𝚉')
            WA13 = text.replace('a','🇦 ').replace("b","🇧 ").replace("c","🇨 ").replace("d","🇩 ").replace("e","🇪 ").replace("f","🇫 ").replace("g","🇬 ").replace("h","🇭 ").replace("i","🇮 ").replace("j","🇯 ").replace("k","🇰 ").replace("l","🇱 ").replace("m","🇲 ").replace("n","🇳 ").replace("o","🇴 ").replace("p","🇵 ").replace("q","🇶 ").replace("r","🇷 ").replace("s","🇸 ").replace("t","🇹 ").replace("u","🇻 ").replace("v","🇺 ").replace("w","🇼 ").replace("x","🇽 ").replace("y","🇾 ").replace("z","🇿 ").replace("A","🇦 ").replace("B","🇧 ").replace("C","🇨 ").replace("D","🇩 ").replace("E","🇪 ").replace("F","🇫 ").replace("G","🇬 ").replace("H","🇭 ").replace("I","🇮 ").replace("J","🇯 ").replace("K","🇰 ").replace("L","🇱 ").replace("M","🇲 ").replace("N","🇳 ").replace("O","🇴 ").replace("P","🇵 ").replace("Q","🇶 ").replace("R","🇷 ").replace("S","🇸 ").replace("T","🇹 ").replace("U","🇻 ").replace("V","🇺 ").replace("W","🇼 ").replace("X","🇽 ").replace("Y","🇾 ").replace("Z","🇿 ")
            WA14 = text.replace('a','ⓐ').replace("b","ⓑ").replace("c","ⓒ").replace("d","ⓓ").replace("e","ⓔ").replace("f","ⓕ").replace("g","ⓖ").replace("h","ⓗ").replace("i","ⓘ").replace("j","ⓙ").replace("k","ⓚ").replace("l","ⓛ").replace("m","ⓜ").replace("n","ⓝ").replace("o","ⓞ").replace("p","ⓟ").replace("q","ⓠ").replace("r","ⓡ").replace("s","ⓢ").replace("t","ⓣ").replace("u","ⓤ").replace("v","ⓥ").replace("w","ⓦ").replace("x","ⓧ").replace("y","ⓨ").replace("z","ⓩ").replace("A","Ⓐ").replace("B","Ⓑ").replace("C","Ⓒ").replace("D","Ⓓ").replace("E","Ⓔ").replace("F","Ⓕ").replace("G","Ⓖ").replace("H","Ⓗ").replace("I","Ⓘ").replace("J","Ⓙ").replace("K","Ⓚ").replace("L","Ⓛ").replace("M","🄼").replace("N","Ⓝ").replace("O","Ⓞ").replace("P","Ⓟ").replace("Q","Ⓠ").replace("R","Ⓡ").replace("S","Ⓢ").replace("T","Ⓣ").replace("U","Ⓤ").replace("V","Ⓥ").replace("W","Ⓦ").replace("X","Ⓧ").replace("Y","Ⓨ").replace("Z","Ⓩ")
            WA14 = text.replace('a','ⓐ').replace("b","ⓑ").replace("c","ⓒ").replace("d","ⓓ").replace("e","ⓔ").replace("f","ⓕ").replace("g","ⓖ").replace("h","ⓗ").replace("i","ⓘ").replace("j","ⓙ").replace("k","ⓚ").replace("l","ⓛ").replace("m","ⓜ").replace("n","ⓝ").replace("o","ⓞ").replace("p","ⓟ").replace("q","ⓠ").replace("r","ⓡ").replace("s","ⓢ").replace("t","ⓣ").replace("u","ⓤ").replace("v","ⓥ").replace("w","ⓦ").replace("x","ⓧ").replace("y","ⓨ").replace("z","ⓩ").replace("A","Ⓐ").replace("B","Ⓑ").replace("C","Ⓒ").replace("D","Ⓓ").replace("E","Ⓔ").replace("F","Ⓕ").replace("G","Ⓖ").replace("H","Ⓗ").replace("I","Ⓘ").replace("J","Ⓙ").replace("K","Ⓚ").replace("L","Ⓛ").replace("M","🄼").replace("N","Ⓝ").replace("O","Ⓞ").replace("P","Ⓟ").replace("Q","Ⓠ").replace("R","Ⓡ").replace("S","Ⓢ").replace("T","Ⓣ").replace("U","Ⓤ").replace("V","Ⓥ").replace("W","Ⓦ").replace("X","Ⓧ").replace("Y","Ⓨ").replace("Z","Ⓩ")
            WA15 = text.replace('a','🅐').replace("b","🅑").replace("c","🅒").replace("d","🅓").replace("e","🅔").replace("f","🅕").replace("g","🅖").replace("h","🅗").replace("i","🅘").replace("j","🅙").replace("k","🅚").replace("l","🅛").replace("m","🅜").replace("n","🅝").replace("o","🅞").replace("p","🅟").replace("q","🅠").replace("r","🅡").replace("s","🅢").replace("t","🅣").replace("u","🅤").replace("v","🅥").replace("w","🅦").replace("x","🅧").replace("y","🅨").replace("z","🅩").replace("A","🅐").replace("B","🅑").replace("C","🅒").replace("D","🅓").replace("E","🅔").replace("F","🅕").replace("G","🅖").replace("H","🅗").replace("I","🅘").replace("J","🅙").replace("K","🅚").replace("L","🅛").replace("M","🅜").replace("N","🅝").replace("O","🅞").replace("P","🅟").replace("Q","🅠").replace("R","🅡").replace("S","🅢").replace("T","🅣").replace("U","🅤").replace("V","🅥").replace("W","🅦").replace("X","🅧").replace("Y","🅨").replace("Z","🅩")
            WA16 = text.replace('a','🄰').replace("b","🄱").replace("c","🄲").replace("d","🄳").replace("e","🄴").replace("f","🄵").replace("g","🄶").replace("h","🄷").replace("i","🄸").replace("j","🄹").replace("k","🄺").replace("l","🄻").replace("m","🄼").replace("n","🄽").replace("o","🄾").replace("p","🄿").replace("q","🅀").replace("r","🅁").replace("s","🅂").replace("t","🅃").replace("u","🅄").replace("v","🅅").replace("w","🅆").replace("x","🅇").replace("y","🅈").replace("z","🅉").replace("A","🄰").replace("B","🄱").replace("C","🄲").replace("D","🄳").replace("E","🄴").replace("F","🄵").replace("G","🄶").replace("H","🄷").replace("I","🄸").replace("J","🄹").replace("K","🄺").replace("L","🄻").replace("M","🄼").replace("N","🄽").replace("O","🄾").replace("P","🄿").replace("Q","🅀").replace("R","🅁").replace("S","🅂").replace("T","🅃").replace("U","🅄").replace("V","🅅").replace("W","🅆").replace("X","🅇").replace("Y","🅈").replace("Z","🅉")
            WA17 = text.replace('a','🅐').replace("b","🅑").replace("c","🅲").replace("d","🅳").replace("e","🅴").replace("f","🅵").replace("g","🅶").replace("h","🅷").replace("i","🅸").replace("j","🅹").replace("k","🅺").replace("l","🅻").replace("m","🅼").replace("n","🅽").replace("o","🅞").replace("p","🅟").replace("q","🆀").replace("r","🆁").replace("s","🆂").replace("t","🆃").replace("u","🆄").replace("v","🆅").replace("w","🆆").replace("x","🆇").replace("y","🆈").replace("z","🆉").replace("A","🅐").replace("B","🅑").replace("C","🅲").replace("D","🅳").replace("E","🅴").replace("F","🅵").replace("G","🅶").replace("H","🅷").replace("I","🅸").replace("J","🅹").replace("K","🅺").replace("L","🅻").replace("M","🅼").replace("N","🅽").replace("O","🅞").replace("P","🅟").replace("Q","🆀").replace("R","🆁").replace("S","🆂").replace("T","🆃").replace("U","🆄").replace("V","🆅").replace("W","🆆").replace("X","🆇").replace("Y","🆈").replace("Z","🆉")
            WA18 = text.replace('a','𝘢').replace('b','𝘣').replace('c','𝘤').replace('d','𝘥').replace('e','𝘦').replace('f','𝘧').replace('g','𝘨').replace('h','𝘩').replace('i','𝘪').replace('j','𝘫').replace('k','𝘬').replace('l','𝘭').replace('m','𝘮').replace('n','𝘯').replace('o','𝘰').replace('p','𝘱').replace('q','𝘲').replace('r','𝘳').replace('s','𝘴').replace('t','𝘵').replace('u','𝘶').replace('v','𝘷').replace('w','𝘸').replace('x','𝘹').replace('y','𝘺').replace('z','𝘻').replace('A','𝘈').replace('B','𝘉').replace('C','𝘊').replace('D','𝘋').replace('E','𝘌').replace('F','𝘍').replace('G','𝘎').replace('H','𝘏').replace('I','𝘐').replace('J','𝘑').replace('K','𝘒').replace('L','𝘓').replace('M','𝘔').replace('N','𝘕').replace('O','𝘖').replace('P','𝘗').replace('Q','𝘘').replace('R','𝘙').replace('S','𝘚').replace('T','𝘛').replace('U','𝘜').replace('V','𝘝').replace('W','𝘞').replace('X','𝘟').replace('Y','𝘠').replace('Z','𝘡')
            WA19 = text.replace('a','Ａ').replace('b','Ｂ').replace('c','Ｃ').replace('d','Ｄ').replace('e','Ｅ').replace('f','Ｆ').replace('g','Ｇ').replace('h','Ｈ').replace('i','Ｉ').replace('j','Ｊ').replace('k','Ｋ').replace('l','Ｌ').replace('m','Ｍ').replace('n','Ｎ').replace('o','Ｏ').replace('p','Ｐ').replace('q','Ｑ').replace('r','Ｒ').replace('s','Ｓ').replace('t','Ｔ').replace('u','Ｕ').replace('v','Ｖ').replace('w','Ｗ').replace('x','Ｘ').replace('y','Ｙ').replace('z','Ｚ')
            WA20 = text.replace('a','ًٍَُِّA').replace("b","ًٍَُِّB").replace("c","ًٍَُِّC").replace("d","ًٍَُِّD").replace("e","ًٍَُِّE").replace("f","ًٍَُِّF").replace("g","ًٍَُِّG").replace("h","ًٍَُِّH").replace("i","ًٍَُِّI").replace("j","ًٍَُِّJ").replace("k","ًٍَُِّK").replace("l","ًٍَُِّL").replace("m","ًٍَُِّM").replace("n","ًٍَُِّN").replace("o","ًٍَُِّO").replace("p","ًٍَُِّP").replace("q","ًٍَُِّQ").replace("r","ًٍَُِّR").replace("s","ًٍَُِّS").replace("t","ًٍَُِّT").replace("u","ًٍَُِّU").replace("v","ًٍَُِّV").replace("w","ًٍَُِّW").replace("x","ًٍَُِّX").replace("y","ًٍَُِّY").replace("z","ًٍَُِّZ")
            WA21= text.replace('a','ᥲ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗞ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ꮐ').replace('h','ᕼ').replace('i','Ꭵ').replace('j','ᒍ').replace('k','Ꮶ').replace('l','ᥣ').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᝪ').replace('p','ᑭ').replace('q','ᑫ').replace('r','ᖇ').replace('s','ᔑ').replace('t','Ꭲ').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ꭹ').replace('z','𝖹')
            WA22 = text.replace('a','ᗩ').replace('b','ᗷ').replace('c','ᑕ').replace('d','ᗪ').replace('e','ᗴ').replace('f','ᖴ').replace('g','Ǥ').replace('h','ᕼ').replace('i','Ꮖ').replace('j','ᒎ').replace('k','ᛕ').replace('l','し').replace('m','ᗰ').replace('n','ᑎ').replace('o','ᗝ').replace('p','ᑭ').replace('q','Ɋ').replace('r','ᖇ').replace('s','Տ').replace('t','丅').replace('u','ᑌ').replace('v','ᐯ').replace('w','ᗯ').replace('x','᙭').replace('y','Ƴ').replace('z','乙').replace('A','ᗩ').replace('B','ᗷ').replace('C','ᑕ').replace('D','ᗪ').replace('E','ᗴ').replace('F','ᖴ').replace('G','Ǥ').replace('H','ᕼ').replace('I','Ꮖ').replace('J','ᒎ').replace('L','ᛕ').replace('L','し').replace('M','ᗰ').replace('N','ᑎ').replace('O','ᗝ').replace('P','ᑭ').replace('Q','Ɋ').replace('R','ᖇ').replace('S','Տ').replace('T','丅').replace('U','ᑌ').replace('V','ᐯ').replace('W','ᗯ').replace('X','᙭').replace('Y','Ƴ').replace('Z','乙')
            WA23 = text.replace('a','A̶').replace('b','B̶').replace('c','C̶').replace('d','D̶').replace('e','E̶').replace('f','F̶').replace('g','G̶').replace('h','H̶').replace('i','I̶').replace('j','J̶').replace('k','K̶').replace('l','L̶').replace('m','M̶').replace('n','N̶').replace('o','O̶').replace('p','P̶').replace('q','Q̶').replace('r','R̶').replace('s','S̶').replace('t','T̶').replace('u','U̶').replace('v','V̶').replace('w','W̶').replace('x','X̶').replace('y','Y̶').replace('z','Z̶').replace('A','A̶').replace('B','B̶').replace('C','C̶').replace('D','D̶').replace('E','E̶').replace('F','F̶').replace('G','G̶').replace('H','H̶').replace('I','I̶').replace('J','J̶').replace('K','K̶').replace('L','L̶').replace('M','M̶').replace('N','N̶').replace('O','O̶').replace('P','P̶').replace('Q','Q̶').replace('R','R̶').replace('S','S̶').replace('T','T̶').replace('U','U̶').replace('V','V̶').replace('W','W̶').replace('X','X̶').replace('Y','Y̶').replace('Z','Z̶')
            WA24 = text.replace('a','𝖆').replace('b','𝖉').replace('c','𝖈').replace('d','𝖉').replace('e','𝖊').replace('f','𝖋').replace('g','𝖌').replace('h','𝖍').replace('i','𝖎').replace('j','𝖏').replace('k','𝖐').replace('l','𝖑').replace('m','𝖒').replace('n','𝖓').replace('o','𝖔').replace('p','𝖕').replace('q','𝖖').replace('r','𝖗').replace('s','𝖘').replace('t','𝖙').replace('u','𝖚').replace('v','𝒗').replace('w','𝒘').replace('x','𝖝').replace('y','𝒚').replace('z','𝒛').replace('A','𝖆').replace('B','𝖉').replace('C','𝖈').replace('D','𝖉').replace('E','𝖊').replace('F','𝖋').replace('G','𝖌').replace('H','𝖍').replace('I','𝖎').replace('J','𝖏').replace('K','𝖐').replace('L','𝖑').replace('M','𝖒').replace('N','𝖓').replace('O','𝖔').replace('P','𝖕').replace('Q','𝖖').replace('R','𝖗').replace('S','𝖘').replace('T','𝖙').replace('U','𝖚').replace('V','𝒗').replace('W','𝒘').replace('X','𝖝').replace('Y','𝒚').replace('Z','𝒛')
            WA25 = text.replace('a','𝒂').replace('b','𝒃').replace('c','𝒄').replace('d','𝒅').replace('e','𝒆').replace('f','𝒇').replace('g','𝒈').replace('h','𝒉').replace('i','𝒊').replace('j','𝒋').replace('k','𝒌').replace('l','𝒍').replace('m','𝒎').replace('n','𝒏').replace('o','𝒐').replace('p','𝒑').replace('q','𝒒').replace('r','𝒓').replace('s','𝒔').replace('t','𝒕').replace('u','𝒖').replace('v','𝒗').replace('w','𝒘').replace('x','𝒙').replace('y','𝒚').replace('z','𝒛')
            WA26 = text.replace('a','𝑎').replace('b','𝑏').replace('c','𝑐').replace('d','𝑑').replace('e','𝑒').replace('f','𝑓').replace('g','𝑔').replace('h','ℎ').replace('i','𝑖').replace('j','𝑗').replace('k','𝑘').replace('l','𝑙').replace('m','𝑚').replace('n','𝑛').replace('o','𝑜').replace('p','𝑝').replace('q','𝑞').replace('r','𝑟').replace('s','𝑠').replace('t','𝑡').replace('u','𝑢').replace('v','𝑣').replace('w','𝑤').replace('x','𝑥').replace('y','𝑦').replace('z','𝑧')
            WA27 = text.replace('a','ꪖ').replace('b','᥇').replace('c','ᥴ').replace('d','ᦔ').replace('e','ꫀ').replace('f','ᠻ').replace('g','ᧁ').replace('h','ꫝ').replace('i','𝓲').replace('j','𝓳').replace('k','𝘬').replace('l','ꪶ').replace('m','ꪑ').replace('n','ꪀ').replace('o','ꪮ').replace('p','ρ').replace('q','𝘲').replace('r','𝘳').replace('s','𝘴').replace('t','𝓽').replace('u','ꪊ').replace('v','ꪜ').replace('w','᭙').replace('x','᥊').replace('y','ꪗ').replace('z','ɀ').replace('A','ꪖ').replace('B','᥇').replace('C','ᥴ').replace('D','ᦔ').replace('E','ꫀ').replace('F','ᠻ').replace('G','ᧁ').replace('H','ꫝ').replace('I','𝓲').replace('J','𝓳').replace('K','𝘬').replace('L','ꪶ').replace('M','ꪑ').replace('N','ꪀ').replace('O','ꪮ').replace('P','ρ').replace('Q','𝘲').replace('R','𝘳').replace('S','𝘴').replace('T','𝓽').replace('U','ꪊ').replace('V','ꪜ').replace('W','᭙').replace('X','᥊').replace('Y','ꪗ').replace('Z','ɀ')
            WA28 = text.replace('a','ą').replace('b','ც').replace('c','ƈ').replace('d','ɖ').replace('e','ɛ').replace('f','ʄ').replace('g','ɠ').replace('h','ɧ').replace('i','ı').replace('j','ʝ').replace('k','ƙ').replace('l','Ɩ').replace('m','ɱ').replace('n','ŋ').replace('o','ơ').replace('p','℘').replace('q','զ').replace('r','r').replace('s','ʂ').replace('t','ɬ').replace('u','ų').replace('v','v').replace('w','ῳ').replace('x','ҳ').replace('y','ყ').replace('z','ʑ')
            WA29 = text.replace('a','Δ').replace("b","β").replace("c","૮").replace("d","ᴅ").replace("e","૯").replace("f","ƒ").replace("g","ɢ").replace("h","み").replace("i","เ").replace("j","ʝ").replace("k","ҡ").replace("l","ɭ").replace("m","ണ").replace("n","ท").replace("o","๏").replace("p","ρ").replace("q","ǫ").replace("r","ʀ").replace("s","ઽ").replace("t","τ").replace("u","υ").replace("v","ѵ").replace("w","ω").replace("x","ﾒ").replace("y","ყ").replace("z","ʑ")
            WA30 = text.replace('a','ᕱ').replace("b","β").replace("c","૮").replace("d","Ɗ").replace("e","ξ").replace("f","ƒ").replace("g","Ǥ").replace("h","ƕ").replace("i","Ĩ").replace("j","ʝ").replace("k","Ƙ").replace("l","Ꮭ").replace("m","ണ").replace("n","ท").replace("o","♡").replace("p","Ƥ").replace("q","𝑄").replace("r","Ꮢ").replace("s","Ƨ").replace("t","Ƭ").replace("u","Ꮜ").replace("v","ѵ").replace("w","ẁ́̀́").replace("x","ﾒ").replace("y","ɣ").replace("z","ʑ")
            WA31 = text.replace('a','A꯭').replace("b","B꯭").replace("c","C꯭").replace("d","D꯭").replace("e","E꯭").replace("f","F꯭").replace("g","G꯭").replace("h","H꯭").replace("i","I꯭").replace("j","J꯭").replace("k","K꯭").replace("l","L꯭").replace("m","M꯭").replace("n","N꯭").replace("o","O꯭").replace("p","P꯭").replace("q","Q꯭").replace("r","R꯭").replace("s","S꯭").replace("t","T꯭").replace("u","U꯭").replace("v","V꯭").replace("w","W꯭").replace("x","X꯭").replace("y","Y꯭").replace("z","Z꯭").replace('A','A꯭').replace("B","B꯭").replace("C","C꯭").replace("D","D꯭").replace("E","E꯭").replace("F","F꯭").replace("G","G꯭").replace("H","H꯭").replace("I","I꯭").replace("J","J꯭").replace("K","K꯭").replace("L","L꯭").replace("M","M꯭").replace("N","N꯭").replace("O","O꯭").replace("P","P꯭").replace("Q","Q꯭").replace("R","R꯭").replace("S","S꯭").replace("T","T꯭").replace("U","U꯭").replace("V","V꯭").replace("W","W꯭").replace("X","X꯭").replace("Y","Y꯭").replace("Z","Z꯭")
            WA32 = text.replace('a','𝔸').replace("b","𝔹").replace("c","ℂ").replace("d","𝔻").replace("e","𝔼").replace("f","𝔽").replace("g","𝔾").replace("h","ℍ").replace("i","𝕀").replace("j","𝕁").replace("k","𝕂").replace("l","𝕃").replace("m","𝕄").replace("n","ℕ").replace("o","𝕆").replace("p","ℙ").replace("q","ℚ").replace("r","ℝ").replace("s","𝕊").replace("t","𝕋").replace("u","𝕌").replace("v","𝕍").replace("w","𝕎").replace("x","𝕏").replace("y","𝕐").replace("z","ℤ").replace("A","𝔸").replace("B","𝔹").replace("C","ℂ").replace("D","𝔻").replace("E","𝔼").replace("F","𝔽").replace("G","𝔾").replace("H","ℍ").replace("I","𝕀").replace("J","𝕁").replace("K","𝕂").replace("L","𝕃").replace("M","𝕄").replace("N","ℕ").replace("O","𝕆").replace("P","ℙ").replace("Q","ℚ").replace("R","ℝ").replace("S","𝕊").replace("T","𝕋").replace("U","𝕌").replace("V","𝕍").replace("W","𝕎").replace("X","𝕏").replace("Y","𝕐").replace("Z","ℤ")
            WA33 = text.replace('a','𝐚').replace("b","𝐛").replace("c","𝐜").replace("d","𝐝").replace("e","𝐞").replace("f","𝐟").replace("g","𝐠").replace("h","𝐡").replace("i","𝐢").replace("j","𝐣").replace("k","𝐤").replace("l","𝐥").replace("m","𝐦").replace("n","𝐧").replace("o","𝐨").replace("p","𝐩").replace("q","𝐪").replace("r","𝐫").replace("s","𝐬").replace("t","𝐭").replace("u","𝐮").replace("v","𝐯").replace("w","𝐰").replace("x","𝐱").replace("y","𝐲").replace("z","𝐳").replace("A","𝐚").replace("B","𝐛").replace("C","𝐜").replace("D","𝐝").replace("E","𝐞").replace("F","𝐟").replace("G","𝐠").replace("H","𝐡").replace("I","𝐢").replace("J","𝐣").replace("K","𝐤").replace("L","𝐥").replace("M","𝐦").replace("N","𝐧").replace("O","𝐨").replace("P","𝐩").replace("Q","𝐪").replace("R","𝐫").replace("S","𝐬").replace("T","𝐭").replace("U","𝐮").replace("V","𝐯").replace("W","𝐰").replace("X","𝐱").replace("Y","𝐲").replace("Z","𝐳")
            WA34 = text.replace('a','𝒂').replace("b","𝒃").replace("c","𝒄").replace("d","𝒅").replace("e","𝒆").replace("f","𝒇").replace("g","𝒈").replace("h","𝒉").replace("i","𝒊").replace("j","𝒋").replace("k","𝒌").replace("l","𝒍").replace("m","𝒎").replace("n","𝒏").replace("o","𝒐").replace("p","𝒑").replace("q","𝒒").replace("r","𝒓").replace("s","𝒔").replace("t","𝒕").replace("u","𝒖").replace("v","𝒗").replace("w","𝒘").replace("x","𝒙").replace("y","𝒚").replace("z","𝒛").replace("A","𝒂").replace("B","𝒃").replace("C","𝒄").replace("D","𝒅").replace("E","𝒆").replace("F","𝒇").replace("G","𝒈").replace("H","𝒉").replace("I","𝒊").replace("J","𝒋").replace("K","𝒌").replace("L","𝒍").replace("M","𝒎").replace("N","𝒏").replace("O","𝒐").replace("P","𝒑").replace("Q","𝒒").replace("R","𝒓").replace("S","𝒔").replace("T","𝒕").replace("U","𝒖").replace("V","𝒗").replace("W","𝒘").replace("X","𝒙").replace("Y","𝒚").replace("Z","𝒛")
            WA35 = text.replace('a','𝗮').replace("b","𝗯").replace("c","𝗰").replace("d","𝗱").replace("e","𝗲").replace("f","𝗳").replace("g","𝗴").replace("h","𝗵").replace("i","𝗶").replace("j","𝗷").replace("k","𝗸").replace("l","𝗹").replace("m","𝗺").replace("n","𝗻").replace("o","𝗼").replace("p","𝗽").replace("q","𝗾").replace("r","𝗿").replace("s","𝘀").replace("t","𝘁").replace("u","𝘂").replace("v","𝘃").replace("w","𝘄").replace("x","𝘅").replace("y","𝘆").replace("z","𝘇").replace("A","𝗔").replace("B","𝗕").replace("C","𝗖").replace("D","𝗗").replace("E","𝗘").replace("F","𝗙").replace("G","𝗚").replace("H","𝗛").replace("I","𝗜").replace("J","𝗝").replace("K","𝗞").replace("L","𝗟").replace("M","𝗠").replace("N","𝗡").replace("O","𝗢").replace("P","𝗣").replace("Q","𝗤").replace("R","𝗥").replace("S","𝗦").replace("T","𝗧").replace("U","𝗨").replace("V","𝗩").replace("W","𝗪").replace("X","𝗫").replace("Y","𝗬").replace("Z","𝗭")
            WA36 = text.replace('a','𝙖').replace("b","𝙗").replace("c","𝙘").replace("d","𝙙").replace("e","𝙚").replace("f","𝙛").replace("g","𝙜").replace("h","𝙝").replace("i","𝙞").replace("j","𝙟").replace("k","𝙠").replace("l","𝙡").replace("m","𝙢").replace("n","𝙣").replace("o","𝙤").replace("p","𝙥").replace("q","𝙦").replace("r","𝙧").replace("s","𝙨").replace("t","𝙩").replace("u","𝙪").replace("v","𝙫").replace("w","𝙬").replace("x","𝙭").replace("y","𝙮").replace("z","𝙯").replace("A","𝙖").replace("B","𝙗").replace("C","𝙘").replace("D","𝙙").replace("E","𝙚").replace("F","𝙛").replace("G","𝙜").replace("H","𝙝").replace("I","𝙞").replace("J","𝙟").replace("K","𝙠").replace("L","𝙡").replace("M","𝙢").replace("N","𝙣").replace("O","𝙤").replace("P","𝙥").replace("Q","𝙦").replace("R","𝙧").replace("S","𝙨").replace("T","𝙩").replace("U","𝙪").replace("V","𝙫").replace("W","𝙬").replace("X","𝙭").replace("Y","𝙮").replace("Z","𝙯")
            WA37 = text.replace('a','𝐀').replace("b","𝐁").replace("c","𝐂").replace("d","𝐃").replace("e","𝐄").replace("f","𝐅").replace("g","𝐆").replace("h","𝐇").replace("i","𝐈").replace("j","𝐉").replace("k","𝐊").replace("l","𝐋").replace("m","𝐌").replace("n","𝐍").replace("o","𝐎").replace("p","𝐏").replace("q","𝐐").replace("r","𝐑").replace("s","𝐒").replace("t","𝐓").replace("u","𝐔").replace("v","𝐕").replace("w","𝐖").replace("x","𝐗").replace("y","𝐘").replace("z","𝐙").replace("A","𝐀").replace("B","𝐁").replace("C","𝐂").replace("D","𝐃").replace("E","𝐄").replace("F","𝐅").replace("G","𝐆").replace
