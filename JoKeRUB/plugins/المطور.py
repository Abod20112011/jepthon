# -*- coding: utf-8 -*-
import re
from telethon import Button, events
from JoKeRUB import l313l, bot
from ..Config import Config
from ..core.managers import edit_or_reply
from . import tgbot

# ========== إعدادات المطور ==========
DEV_PIC = "https://files.catbox.moe/k4fxu0.jpg"  # صورة المطور
DEV_TEXT = (
    "**مطورين سورس فينيكس**\n"
    "✛━━━━━━━━━━━━━✛\n"
    "**• المطور الأساسي :** @BD_0I\n"
    "**• قناة السورس :** @lAYAI\n"
    "✛━━━━━━━━━━━━━✛\n"
    "**• النظام :** يعمل الآن بنجاح 🚀"
)
# =====================================

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text.strip()
        if query.startswith("المطور") and event.query.user_id == l313l.uid:
            # بناء الأزرار
            buttons = [
                [Button.url("👨‍💻 المطور: BD_0I", "https://t.me/BD_0I")],
                [Button.url("📢 قناة السورس", "https://t.me/lAYAI")]
            ]
            if DEV_PIC and DEV_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    DEV_PIC,
                    text=DEV_TEXT,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html"
                )
            elif DEV_PIC:
                result = builder.document(
                    DEV_PIC,
                    title="معلومات المطور",
                    text=DEV_TEXT,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html"
                )
            else:
                result = builder.article(
                    title="معلومات المطور",
                    text=DEV_TEXT,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html"
                )
        await event.answer([result] if result else None)


@l313l.ar_cmd(
    pattern="المطور$",
    command=("المطور", "utils"),
    info={
        "header": "لإظهار معلومات المطور مع أزرار أونلاين",
        "usage": "{tr}المطور",
    },
)
async def developer_cmd(event):
    """إرسال رسالة المطور بأزرار أونلاين"""
    if event.fwd_from:
        return
    bot_username = Config.TG_BOT_USERNAME
    if not bot_username:
        return await edit_or_reply(event, "❌ لم يتم تعيين توكن البوت المساعد.")

    # استدعاء inline query من البوت
    try:
        response = await bot.inline_query(bot_username, "المطور")
        if response:
            await response[0].click(event.chat_id, reply_to=event.reply_to_msg_id)
            await event.delete()
        else:
            await edit_or_reply(event, "❌ لم يتم العثور على نتائج.")
    except Exception as e:
        await edit_or_reply(event, f"❌ حدث خطأ: {e}")
