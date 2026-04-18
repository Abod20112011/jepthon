import time
import asyncio
import glob
import os
import sys
from telethon.errors.rpcerrorlist import ChannelPrivateError
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
import requests
from telethon import Button, functions, types, utils
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError
from JoKeRUB import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from aiohttp import web
from ..core import web_server
from ..core.logger import logging
from ..core.session import l313l
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

LOGS = logging.getLogger("aljoker")
logging.getLogger('telethon').setLevel(logging.WARNING)
##Reda hands here
cmdhr = Config.COMMAND_HAND_LER
Zed_Vip = (8277718687, 5427469031)
Zed_Dev = (5427469031, 6349091574)
bot = l313l
ENV = bool(os.environ.get("ENV", False))

if ENV:
    VPS_NOLOAD = ["سيرفر"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["هيروكو"]

async def save_installation_date():
    """حفظ تاريخ التثبيت تلقائياً عند تشغيل السورس"""
    # جلب التاريخ من قاعدة البيانات
    db_date = gvarstatus("KARAR_DATE_FULL")
    
    if not db_date:
        # إذا ما في تاريخ مخزن، ننشئ تاريخ ووقت جديد
        installation_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        addgvar("KARAR_DATE_FULL", installation_time)
        LOGS.info(f"✅ تم حفظ تاريخ التنصيب: {installation_time}")
    else:
        LOGS.info(f"📅 تاريخ التنصيب موجود مسبقاً: {db_date}")

async def check_dyno_type():
    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.heroku.com/apps/{Config.HEROKU_APP_NAME}/dynos", headers=headers) as resp:
            if resp.status == 200:
                dynos = await resp.json()
                for dyno in dynos:
                    if dyno["type"] != "standard-1X":
                        return False
            else:
                return False
    return True

async def setup_bot():
    """
    To set up bot for JoKeRUB
    """
    try:
        await l313l.connect()
        config = await l313l(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == l313l.session.server_address:
                if l313l.session.dc_id != option.id:
                    LOGS.warning(
                        f"⌯︙معرف ثابت في الجلسة من {l313l.session.dc_id}"
                        f"⌯︙لـ  {option.id}"
                    )
                l313l.session.set_dc(option.id, option.ip_address, option.port)
                l313l.session.save()
                break
        bot_details = await l313l.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        redaport = Config.PORT
        await web.TCPSite(app, bind_address, redaport).start()
        l313l.me = await l313l.get_me()
        l313l.uid = l313l.tgbot.uid = utils.get_peer_id(l313l.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(l313l.me)
        if not check_dyno_type:
            LOGS.error("قد تحدث مشكلة ولن يعمل السورس لان نوع الداينو ليس بيسك قم بتحويله الى basic")
        
        # حفظ تاريخ التثبيت تلقائياً
        await save_installation_date()
        
    except Exception as e:
        LOGS.error(f"كـود تيرمكس - {str(e)}")
        sys.exit()

async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            # تعريف الإيموجيات المميزة
            EMOJI_DEV = "5258215850745275216"      # 💎 للمطور
            PREMIUM_EMOJI_ID = "5258332798409783582"  # ✨ للتألق
            EMOJI_BOT = "5447242579827523388"      # 🤖 للبوت
            EMOJI_HAK = "5447242579827523388"      # 💀 للهاك
            
            # إنشاء الأزرار (زر واحد فقط للمطور)
            buttons = [
                [
                    {
                        "text": "المـطـور",
                        "url": "https://t.me/BD_0I",
                        "style": "primary",  # لون أزرق
                        "icon_custom_emoji_id": EMOJI_DEV
                    }
                ]
            ]
            
            # نص الرسالة حسب طلبك (الإيموجي بعد النص)
            caption_text = f'''\
<b>〄︙بــوت ᥲRRᥲS يعمـل بنجـاح</b> <tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">✨</tg-emoji>

◈︙أرسل ( <code>.الاوامر</code> ) لرؤية اوامر السورس <tg-emoji emoji-id="{EMOJI_BOT}">🤖</tg-emoji>

◈︙لأستعمال بوت الأختراق عبر كود التيرمكس أرسل ( <code>.هاك</code> ) <tg-emoji emoji-id="{EMOJI_HAK}">💀</tg-emoji>'''
            
            # إرسال الرسالة عبر Bot API
            import requests
            import json
            import os
            
            photo_path = "l313l/razan/resources/start/arras.JPEG"
            
            # التحقق من وجود الصورة
            if os.path.exists(photo_path):
                # إرسال الصورة مع الأزرار
                with open(photo_path, 'rb') as photo:
                    files = {
                        'photo': photo
                    }
                    data = {
                        'chat_id': BOTLOG_CHATID,
                        'caption': caption_text,
                        'parse_mode': 'HTML',
                        'reply_markup': json.dumps({"inline_keyboard": buttons})
                    }
                    
                    send_url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendPhoto"
                    response = requests.post(send_url, data=data, files=files, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('ok'):
                            Config.CATUBLOGO = result['result']['message_id']
                        else:
                            LOGS.error(f"API Error: {result}")
                            raise Exception("API request failed")
                    else:
                        LOGS.error(f"HTTP {response.status_code}: {response.text}")
                        raise Exception(f"HTTP {response.status_code}")
            else:
                # إذا الصورة غير موجودة، استخدم Telethon فقط
                LOGS.error(f"Photo not found: {photo_path}")
                raise Exception("Photo file missing")
                
    except Exception as e:
        LOGS.error(f"Error in startupmessage: {e}")
        # Fallback: استخدام Telethon بدون الألوان
        try:
            caption_text_fallback = f'''〄︙ بــوت ꪖႦ᥆᥆ᦔ  يـعـمـل بـنـجـاح ✨

◈︙ أرسل ( .الاوامر ) لرؤية اوامر السورس 🤖

◈︙ لأستعمال بوت الأختراق عبر كود التيرمكس أرسل ( .هاك ) 💀'''
            
            Config.CATUBLOGO = await l313l.tgbot.send_file(
                BOTLOG_CHATID,
                "l313l/razan/resources/start/arras.JPEG",
                caption=caption_text_fallback,
                buttons=[
                    [Button.url("المـطـور", "https://t.me/BD_0I")]
                ],
                parse_mode='html'
            )
        except Exception as fallback_error:
            LOGS.error(f"Fallback failed: {fallback_error}")
        return None
        
    # باقي الكود كما هو...
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
        
    try:
        if msg_details:
            await l313l.check_testcases()
            message = await l313l.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**تم تشغيل البوت الأن أرسل `.فحص`**"
            await l313l.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await l313l.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        if "Could not find the input entity" in str(e):
            pass  # لا تطبع الخطأ
        else:
            LOGS.error(f"خطأ في كتلة restart_update: {e}")
            return None

async def mybot():
    try:
        starkbot = await l313l.tgbot.get_me()
        joker = "عبود"
        commands_aRRaS = """start - للبدء
hack - قسم أمر الهـاك"""
        bot_name = starkbot.first_name
        botname = f"@{starkbot.username}"
        if bot_name.endswith("Assistant"):
            print("تم تشغيل البوت")
        if starkbot.bot_inline_placeholder:
            print("Source of Aras")
        else:
            try:
                await l313l.send_message("@BotFather", "/setinline")
                await asyncio.sleep(1)
                await l313l.send_message("@BotFather", botname)
                await asyncio.sleep(1)
                await l313l.send_message("@BotFather", joker)
                await asyncio.sleep(2)
                
                await l313l.send_message("@BotFather", "/setcommands")
                await asyncio.sleep(1)
                await l313l.send_message("@BotFather", botname)
                await asyncio.sleep(1)
                await l313l.send_message("@BotFather", commands_aRRaS)
                await asyncio.sleep(2)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await l313l.tgbot.get_me()
    try:
        await l313l(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await l313l(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))

                
async def load_plugins(folder, extfolder=None):
    """
    تحميل ملفات السورس
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"JoKeRUB/{folder}/*.py"
        plugin_path = f"JoKeRUB/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"لم يتم تحميل {shortname} بسبب خطأ {e}\nمسار الملف {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await l313l.tgbot.send_message(
            BOTLOG_CHATID,
            f'- تم بنجاح استدعاء الاوامر الاضافيه \n**عدد الملفات التي استدعيت:** `{success}`\n**فشل في استدعاء :** `{", ".join(failure)}`',
        )
        
async def aljoker_the_best(l313l, group_name):
    async for dialog in l313l.iter_dialogs():
        if dialog.is_group and dialog.title == group_name:
            return dialog.id
    return None

async def verifyLoggerGroup():
    """
    Will verify both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await l313l.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "᯽︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "᯽︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
        except ValueError:
            LOGS.error("᯽︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(
                "᯽︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."
            )
        except Exception as e:
            LOGS.error(
                "᯽︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "- عزيزي المستخدم هذه هي مجموعه الاشعارات يرجى عدم حذفها  - @BD_0I"
        photobt = await l313l.upload_file(file="l313l/razan/resources/start/Jepthon.JPEG")
        botlog_group_id = await aljoker_the_best(l313l, "مـجمـوعة آشـعـارات فـيـنـيـكـس")
        if botlog_group_id:
            addgvar("PRIVATE_GROUP_BOT_API_ID", botlog_group_id)
            print("᯽︙تم العثور على مجموعة المساعدة بالفعل وإضافتها إلى المتغيرات.")
        else:
            _, groupid = await create_supergroup(
                "مـجمـوعة آشـعـارات فـيـنـيـكـس", l313l, Config.TG_BOT_USERNAME, descript, photobt
            )
            addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
            print("᯽︙تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID == -100:
        descript = "✧︙ وظيفه الكروب يحفظ رسائل الخاص اذا ما تريد الامر احذف الكروب نهائي \n  - @BD_0I"
        photobt = await l313l.upload_file(file="l313l/razan/resources/start/Jepthon2.JPEG")
        pm_logger_group_id = await aljoker_the_best(l313l, "مـجمـوعة تـﺨـزين فـيـنـيـكـس")
        if pm_logger_group_id:
            addgvar("PM_LOGGER_GROUP_ID", pm_logger_group_id)
            print("تـم العثور على مجموعة الكروب التخزين بالفعل واضافة الـفارات الـيها.")
        else:
            _, groupid = await create_supergroup(
                "مـجمـوعة تـﺨـزين فـيـنـيـكـس", l313l, Config.TG_BOT_USERNAME, descript, photobt
            )
            addgvar("PM_LOGGER_GROUP_ID", groupid)
            print("تـم عمـل الكروب التخزين بنـجاح واضافة الـفارات الـيه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "JoKeRUB"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)

async def install_externalrepo(repo, branch, cfolder):
    jokerREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if jokerBRANCH := branch:
        repourl = os.path.join(jokerREPO, f"tree/{jokerBRANCH}")
        gcmd = f"git clone -b {jokerBRANCH} {jokerREPO} {cfolder}"
        errtext = f"لا يوحد فرع بأسم `{jokerBRANCH}` في الريبو الخارجي {jokerREPO}. تاكد من اسم الفرع عبر فار (`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = jokerREPO
        gcmd = f"git clone {jokerREPO} {cfolder}"
        errtext = f"الرابط ({jokerREPO}) الذي وضعته لفار `EXTERNAL_REPO` غير صحيح عليك وضع رابط صحيح"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await l313l.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error(
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا "
        )
        return await l313l.tgbot.send_message(
            BOTLOG_CHATID,
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا ",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    await load_plugins(folder="JoKeRUB", extfolder=cfolder)

