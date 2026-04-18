# -*- coding: utf-8 -*-
from JoKeRUB import l313l, bot
from ..Config import Config
from ..core.managers import edit_or_reply
from telethon import Button, events

# ========== إعدادات المطور ==========
DEV_TEXT = (
    "<b>مطورين سورس فينيكس</b>\n"
    "✛━━━━━━━━━━━━━✛\n"
    "<b>• المطور الأساسي :</b> @BD_0I\n"
    "<b>• قناة السورس :</b> @lAYAI\n"
    "✛━━━━━━━━━━━━━✛\n"
    "<b>• النظام :</b> يعمل الآن بنجاح 🚀"
)
DEV_PIC = "https://files.catbox.moe/k4fxu0.jpg"
Bot_Username = Config.TG_BOT_USERNAME
# =====================================

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def dev_inline_handler(event):  # اسم فريد
        builder = event.builder
        result = None
        query = event.text.strip()
        await bot.get_me()
        if query.startswith("المطور") and event.query.user_id == bot.uid:
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


@bot.on(admin_cmd(outgoing=True, pattern="المطور$"))
async def developer_repo(event):  # اسم فريد
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "المطور")
    if response:  # ✅ فحص لتجنب الخطأ
        await response[0].click(event.chat_id, reply_to=event.reply_to_msg_id)
        await event.delete()
    else:
        await edit_or_reply(event, "❌ لم يتم العثور على نتائج.")
