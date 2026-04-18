import asyncio
import os
from pathlib import Path
from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import MessageEntityCustomEmoji
from . import l313l

# ==================================================================
# 🎯 الإعدادات الأساسية
# ==================================================================
BOT_USERNAME = "@GoldnB7Rbot"           # ✅ بوت التحميل
PREMIUM_EMOJI_ID = 5159115433214739591  # ⭐ أيدي النجمة المميزة (غيّر إلى 0 إن لم ترد مميز)
MY_RIGHTS = "@BD_0I"                   # توقيعك في الكابشن
CHANNEL_URL = "https://t.me/B_a_r"      # ✅ رابط القناة

CMD_SONG = "يوت"  # أمر البوت (يجب أن يفهمه البوت)

# ==================================================================
# ⚙️ دوال مساعدة
# ==================================================================

async def unblock_bot(client):
    try:
        await client(UnblockRequest(id=BOT_USERNAME))
        return True
    except:
        return False

def get_premium_caption(text):
    emoji_char = "⭐"
    caption = f"• {text} {MY_RIGHTS} {emoji_char}"
    offset = caption.find(emoji_char)
    entity = MessageEntityCustomEmoji(
        offset=offset,
        length=len(emoji_char),
        document_id=PREMIUM_EMOJI_ID
    )
    return caption, [entity]

def get_status_message():
    return "╮ جـارِ البحث عـن الإغـنيةة ... 🎧♥️ ╰"

async def download_thumbnail(client, media_msg):
    """تحميل الصورة المصغرة فقط (إن وجدت)"""
    temp_dir = Path("temp_thumbs")
    temp_dir.mkdir(exist_ok=True)
    
    doc = media_msg.media.document
    if doc and doc.thumbs:
        thumb_size = doc.thumbs[0]
        thumb_path = await client.download_media(media_msg, thumb=thumb_size, file=temp_dir)
        return thumb_path
    return None

# ==================================================================
# 🔍 دالة البحث الأساسية – إرسال مباشر (تم إصلاح الخطأ)
# ==================================================================

async def run_and_clean(client, chat_id, query, status_msg, original_msg=None, is_owner=True):
    try:
        await unblock_bot(client)

        sent = await client.send_message(BOT_USERNAME, f"{CMD_SONG} {query}")
        
        media_msg = None
        thumb_path = None
        
        # انتظار الملف لمدة 30 ثانية
        for _ in range(15):
            await asyncio.sleep(2)
            messages = await client.get_messages(BOT_USERNAME, limit=5)
            for msg in messages:
                if msg.id > sent.id and msg.media:
                    media_msg = msg
                    break
            if media_msg:
                break

        if media_msg:
            # ✅ تحميل الصورة المصغرة فقط
            thumb_path = await download_thumbnail(client, media_msg)
            
            cap, ent = get_premium_caption("uploader")
            
            # ✅ ✅ ✅ إرسال الميديا مباشرة (لا InputMediaDocument ولا أخطاء)
            if not is_owner and original_msg:
                await client.send_file(
                    chat_id,
                    media_msg.media,        # 🔥 الميديا مباشرة من رسالة البوت
                    caption=cap,
                    formatting_entities=ent,
                    thumb=thumb_path,       # الصورة المصغرة (إن وجدت)
                    supports_streaming=True,
                    reply_to=original_msg.id
                )
                # 🗑️ حذف رسالة الحالة بعد الإرسال
                await status_msg.delete()
            
            # ✅ للمالك: إرسال عادي وحذف رسالة الأمر
            else:
                await client.send_file(
                    chat_id,
                    media_msg.media,        # 🔥 مباشرة
                    caption=cap,
                    formatting_entities=ent,
                    thumb=thumb_path,
                    supports_streaming=True,
                    reply_to=None
                )
                if original_msg:
                    await original_msg.delete()
        else:
            await status_msg.edit("**❌ لم يتم العثور على نتائج، تأكد من الاسم.**")
    
    except Exception as e:
        await status_msg.edit(f"**❌ حدث خطأ:** `{str(e)[:50]}...`")
    
    finally:
        # 🧹 حذف الصورة المصغرة المؤقتة
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
        
        # 🧹 حذف سجل المحادثة مع البوت المساعد
        try:
            await client(DeleteHistoryRequest(
                peer=BOT_USERNAME,
                max_id=0,
                just_clear=True,
                revoke=True
            ))
        except:
            pass

# ==================================================================
# 👑 أوامر المالك
# ==================================================================

@l313l.ar_cmd(pattern="بحث ([\s\S]*)")
async def owner_search_song(event):
    query = event.pattern_match.group(1)
    status_msg = await event.edit(get_status_message())
    await run_and_clean(
        event.client,
        event.chat_id,
        query,
        status_msg,
        original_msg=event,
        is_owner=True
    )

# ==================================================================
# 👥 أوامر الآخرين (الخاص)
# ==================================================================

@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def users_search_handler(event):
    if event.sender_id == event.client.uid:
        return

    text = event.raw_text.strip()
    
    if text.startswith("بحث "):
        query = text.replace("بحث ", "", 1).strip()
        if not query:
            await event.reply("❌ يرجى كتابة اسم الأغنية بعد الأمر.")
            return
        
        status_msg = await event.reply(get_status_message())
        await run_and_clean(
            event.client,
            event.chat_id,
            query,
            status_msg,
            original_msg=event.message,
            is_owner=False
        )
