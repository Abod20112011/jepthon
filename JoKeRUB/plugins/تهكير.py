# Copyright (C) 2021 JoKeRUB TEAM
# FILES WRITTEN BY  @lMl10l

import asyncio
from telethon import events
from JoKeRUB import l313l
import random
from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@l313l.ar_cmd(
    pattern="تهكير$",
    command=("تهكير", plugin_category),
    info={
        "header": "Fun hack animation.",
        "description": "Reply to user to show hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    "Fun hack animation."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 6373993992:
            await edit_or_reply(
                event, "**᯽︙ عـذرا لا استـطيع اخـتراق مـطوري اعـتذر او سيقـوم بتهـكيرك**"
            )
        else:
            event = await edit_or_reply(event, "يتـم الاختـراق ..")
            animation_chars = [
                "᯽︙ تـم الربـط بسـيرفرات الـتهكير الخـاصة",
                "تـم تحـديد الضحـية",
                "**تهكيـر**... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 84%\n█████████████████████▒▒▒▒ ",
                "**تهكيـر**... 100%\n████████████████████████ ",
                f"᯽︙ ** تـم اخـتراق الضـحية**..\n\nقـم بالـدفع الى {ALIVE_NAME} لعـدم نشـر معلوماتك وصـورك",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "᯽︙ لم يتـم التعـرف على المستـخدم",
            parse_mode=_format.parse_pre,
        )
@l313l.ar_cmd(
    pattern="تهكير2$",
    command=("تهكير2", plugin_category),
    info={
        "header": "Fun hack animation.",
        "description": "Reply to user to show hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    if event.fwd_from:
        return

    animation_interval = 3

    animation_ttl = range(11)

    
    await event.edit("**جارِ الاختراق الضحية..**")

    animation_chars = [
        
            "**جار تحديد الضحية...**",
            "**تم تحديد الضحية بنجاح ✓**",
            "`يتم الاختراق... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`يتم الاختراق... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`يتم الاختراق... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`يتم الاختراق... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`يتم الاختراق... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`يتم الاختراق... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`يتم الاختراق... 84%\n█████████████████████▒▒▒▒ `",
            "`يتم الاختراق... 100%\n████████████████████████ `",
            "` تم رفع معلومات الشخص...\n\nسيتم ربط المعلومات بسيرفرات التهكير الخاصه..`"
        ]
  
    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
# Made for Hussein
        await event.edit(animation_chars[i % 11])

    await asyncio.sleep(2)

    animation_interval = 1
    animation_ttl = range(0,14)
    await event.edit("**يتم الاتصال لسحب التوكن الخاص به عبر موقع.telegram.org**")
    await asyncio.sleep(1)
    animation_chars = [
            "`root@anon:~#` ",
            "`root@anon:~# ls`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~#`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# `",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami\n\nwhoami=user`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected in ghost ...`",
            "`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected in ghost ...\n\nتم اكتمال العملية ✓!`",
            "root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# touch setup.py\n\nsetup.py deployed ...\nيتم الان الرفع عبر CMD تلقائياً ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected  in ghost ...\n\nتم اكتمال العملية ✓!\nيتم الان استخراج توكن الضحية!\nToken=`DJ65gulO90P90nlkm65dRfc8I`",
         ]
            

    for i in animation_ttl:
# Made for Hussein        
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 14])
    
    await asyncio.sleep(2)

    await event.edit("`starting telegram hack`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات...\n 0%completed.\nTERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (1.3) kB`")#credit to legendx22,sawan
    await asyncio.sleep(2)
    await event.edit(" `يتم سحب الصور والمعلومات...\n 4% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package`")
    await asyncio.sleep(1)
    await event.edit("`يتم سحب الصور والمعلومات...\n 6% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات....\n 8%completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished\n creating pdf of chat`")
    await asyncio.sleep(1)
    await event.edit("`يتم سحب الصور والمعلومات...\n 15%completed\n Terminal:chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installing`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات...\n 24%completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished\nerminal:chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installed\n creting data into pdf`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات...\n 32%completed\n looking for use history \n downloading-telegram -id prtggtgf . gfr (12.99 mb)\n collecting data starting imprute attack to user account\n chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installed\n creted data into pdf\nDownload sucessful Bruteforce-Telegram-0.1.tar.gz (1.3)`")
    await asyncio.sleep(1)
    await event.edit("يتم سحب الصور والمعلومات...\n 38%completed\n\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات...\n 52%completed\nexterting data from telegram private server\ndone with status 36748hdeg \n checking for more data in device`")
    await asyncio.sleep(1)
    await event.edit("`يتم سحب الصور والمعلومات...\n 60%completed\nmore data found im target device\npreparing to download data\n process started with status 7y75hsgdt365ege56es \n status changed to up`")
    await asyncio.sleep(1)
    await event.edit("`يتم سحب الصور والمعلومات....\n 73% completed\n downloading data from device\n process completed with status 884hfhjh\nDownloading-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target\n lding chat tg-bot bruteforce finished\n creating pdf of chat`")
    await asyncio.sleep(2)
    await event.edit("`يتم سحب الصور والمعلومات...\n 88%completed\nall data from telegram private server downloaded\nterminal download sucessfull--with status jh3233fdg66y yr4vv.irh\n data collected from tg-bot\nTERMINAL:\n Bruteforce-Telegram-0.1.tar.gz (1.3)downloaded`")
    await asyncio.sleep(5)
    await event.edit("`100%\n█████████████████████████ `\n\n\n  TERMINAL:\nيتم تنزيل Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  يتم تنزيل Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: `")
    await asyncio.sleep(5)
    await event.edit(f"`تم سحب جميع معلومات الحساب\n قم بلدفع الى {ALIVE_NAME} 100$ \n حتى لا يقم بنشر صورك ومحادثاتك !`")
    await asyncio.sleep(5)
    h=(random.randrange(1,5)) 
    if h==1:
        await event.edit("`تم رفع جميع الصور المخزونة والمحادثات وجهات اتصال المستخدم عبر مجلد pdf \n\n😂 لا تقلق انا فقط من ارئ معلوماتك 😎😎.. اذا لم تصدق ادخل الى هذا الرابط وانظر بنفسك` 🙂\n\nhttps://drive.google.com/file/d/1EHJSkt64RZEw7a2h8xkRqZSv_4dWhB02/view?usp=sharing")
    if h==2:
        await event.edit("`تم رفع جميع الصور المخزونة والمحادثات وجهات اتصال المستخدم عبر مجلد pdf \n\n😂 لا تقلق انا فقط من ارئ معلوماتك 😎😎.. اذا لم تصدق ادخل الى هذا الرابط وانظر بنفسك` 🙂\n\nhttps://drive.google.com/file/d/1YaUfNVrHU7zSolTuFN3HyHJuTWQtdL2r/view?usp=sharing")
    if h==3:
        await event.edit("`تم رفع جميع الصور المخزونة والمحادثات وجهات اتصال المستخدم عبر مجلد pdf \n\n😂 لا تقلق انا فقط من ارئ معلوماتك 😎😎.. اذا لم تصدق ادخل الى هذا الرابط وانظر بنفسك` 🙂\n\nhttps://drive.google.com/file/d/1o2wXirqy1RZqnUMgsoM8qX4j4iyse26X/view?usp=sharing")
    if h==4:
        await event.edit("`تم رفع جميع الصور المخزونة والمحادثات وجهات اتصال المستخدم عبر مجلد pdf \n\n😂 لا تقلق انا فقط من ارئ معلوماتك 😎😎.. اذا لم تصدق ادخل الى هذا الرابط وانظر بنفسك` 🙂\n\nhttps://drive.google.com/file/d/15-zZVyEkCFA14mFfD-2DKN-by1YOWf49/view?usp=sharing")
    if h==5:
        await event.edit("`تم رفع جميع الصور المخزونة والمحادثات وجهات اتصال المستخدم عبر مجلد pdf \n\n😂 لا تقلق انا فقط من ارئ معلوماتك 😎😎.. اذا لم تصدق ادخل الى هذا الرابط وانظر بنفسك` 🙂\n\nhttps://drive.google.com/file/d/1hPUfr27UtU0XjtC20lXjY9G3D9jR5imj/view?usp=sharing")
