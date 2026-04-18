# JoKeRUB
# - - - - - - - - - - - - -
# Hussein : @lMl10l
# @jepthon
# - - - - - - - - - - - - -

import os
import requests
from datetime import datetime
from PIL import Image
from telethon.utils import get_display_name
from JoKeRUB import l313l
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "utils"

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

# --- دالة الرفع الشاملة (تليجراف + جراف + كاتبوكس) ---
def upload_to_cloud(file_path):
    # 1. المحاولة الأولى: Telegra.ph
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://telegra.ph/upload",
                files={'file': ('file', f, 'image/jpeg')},
                headers=headers,
                timeout=5
            )
        if response.status_code == 200 and isinstance(response.json(), list):
            return "https://telegra.ph" + response.json()[0]['src']
    except Exception:
        pass # فشل تليجراف، ننتقل للتالي

    # 2. المحاولة الثانية: Graph.org (احتياطي)
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://graph.org/upload",
                files={'file': ('file', f, 'image/jpeg')},
                timeout=5
            )
        if response.status_code == 200 and isinstance(response.json(), list):
            return "https://graph.org" + response.json()[0]['src']
    except Exception:
        pass # فشل جراف، ننتقل للأقوى

    # 3. المحاولة الثالثة والمنقذة: Catbox.moe (يعمل دائماً)
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f},
                timeout=20
            )
        if response.status_code == 200:
            return response.text.strip() # يرجع رابط مباشر
    except Exception as e:
        LOGS.error(f"All Upload Methods Failed: {e}")
    
    return None

@l313l.ar_cmd(
    pattern="(ت(ل)?ك(راف)?) ?(m|t|ميديا|نص)(?:\s|$)([\s\S]*)",
    command=("تلكراف", plugin_category),
    info={
        "header": "رفع الصور والحصول على رابط مباشر",
        "description": "يرفع الصور إلى سيرفرات متعددة لضمان الحصول على رابط.",
        "usage": "{tr}تلكراف ميديا",
    },
)
async def _(event):
    "للحصول على رابط مباشر للصورة"
    jokevent = await edit_or_reply(event, "` ⌔︙جـار الرفـع (محاولة عدة سيرفرات)...`")
    optional_title = event.pattern_match.group(5)
    
    if not event.reply_to_msg_id:
        return await jokevent.edit("` ⌔︙قـم بالـرد عـلى صـورة`")

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()

    if input_str in ["ميديا", "m"]:
        if not r_message.media:
            return await jokevent.edit("` ⌔︙الرد يجب أن يكون على صورة أو فيديو.`")

        downloaded_file_name = await event.client.download_media(r_message, Config.TEMP_DIR)
        
        if downloaded_file_name.endswith(".webp"):
            resize_image(downloaded_file_name)
        
        # استخدام الدالة الذكية
        media_url = upload_to_cloud(downloaded_file_name)
        
        if media_url:
            end = datetime.now()
            ms = (end - start).seconds
            await jokevent.edit(
                f"** ⌔︙الـرابـط : **[إضـغط هنـا]({media_url})\n"
                f"** ⌔︙الرابط الخام : ** `{media_url}`\n"
                f"** ⌔︙الوقـت : **`{ms} ثـانيـة.`",
                link_preview=False,
            )
        else:
            await jokevent.edit(
                "** ⌔︙فشل الرفع نهائياً!**\n"
                "يبدو أن السيرفر الخاص بك محظور من جميع مواقع الرفع."
            )
        
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)

    elif input_str in ["نص", "t"]:
        await jokevent.edit("`⌔︙الرفع النصي متوقف حالياً، استخدم رفع الصور.`")
