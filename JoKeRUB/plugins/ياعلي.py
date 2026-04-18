from JoKeRUB import l313l, bot
import time
from telethon.tl import types
from JoKeRUB import BOTLOG_CHATID
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import asyncio
from ..Config import Config
import requests
from telethon import Button, events
from telethon.tl.functions.messages import ExportChatInviteRequest
from ..core.managers import edit_delete, edit_or_reply
#ياعلي
#اخ اخ اخ اخ اخ اخ اخممممممط ياطويل العمر اخمطط 😂
#Reda
REH = "**᯽︙ لأستخدام بوت اختراق الحساب عن طريق كود التيرمكس أضغط على الزر**"
JOKER_PIC = "https://files.catbox.moe/unov55.jpg"
Bot_Username = Config.TG_BOT_USERNAME
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        if query.startswith("هاك") and event.query.user_id == bot.uid:
            buttons = Button.url("• اضغط هنا عزيزي •", f"https://t.me/{joker}")
            if JOKER_PIC and JOKER_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    JOKER_PIC, text=REH, buttons=buttons, link_preview=False
                )
            elif JOKER_PIC:
                result = builder.document(
                    JOKER_PIC,
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
        await event.answer([result] if result else None)

@bot.on(admin_cmd(outgoing=True, pattern="هاك"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    await bot.send_message(lMl10l, "/hack")
    response = await bot.inline_query(lMl10l, "هاك")
    await response[0].click(event.chat_id)
    await event.delete()

#####################
###
#
'''
@l313l.ar_cmd(pattern="اشتراك")
async def reda(event):
    ty = event.text
    ty = ty.replace(".اشتراك", "")
    ty = ty.replace(" ", "")
    if len (ty) < 2:
        return await edit_delete(event, "**᯽︙ قم بكتابة نوع الاشتراك الاجباري كروب او خاص 🤔**")
    if ty == "كروب":
        if not event.is_group:
            return await edit_delete("**᯽︙ استعمل الأمر في الجروب المراد تفعيل الاشتراك الاجباري به**")
        if event.is_group:
            if gvarstatus ("subgroup") == event.chat_id:
                return await edit_delete(event, "**᯽︙ الاشتراك الاجباري مفعل لهذا الكروب**")
            if gvarstatus("subgroup"):
                return await edit_or_reply(event, "**᯽︙ الاشتراك الاجباري مفعل لكروب اخر قم بالغائه لتفعيله في كروب اخر**")
            addgvar("subgroup", f"{event.chat_id}")
            return await edit_or_reply(event, "**᯽︙ تم تفعيل الاشتراك الاجباري لهذه المجموعة ✓**")
    if ty == "خاص":
        if gvarstatus ("subprivate"):
            return await edit_delete(event, "**᯽︙ الاشتراك الاجباري للخاص مُفعل بالفعل ✓**")
        if not gvarstatus ("subprivate"):
            addgvar ("subprivate", True)
            await edit_or_reply(event, "**᯽︙ تم تفعيل الاشتراك الاجباري للخاص ✓**")
    if ty not in ["خاص", "كروب"]:
        return await edit_delete(event, "**᯽︙ قم بكتابة نوع الاشتراك الاجباري خاص او كروب 🤔**")
@l313l.ar_cmd(pattern="تعطيل")
async def reda (event):
    cc = event.text.replace(".تعطيل", "")
    cc = cc.replace(" ", "")
    if len (cc) < 2:
        return await edit_delete(event, "**᯽︙ قم بكتابة نوع الاشتراك الاجباري لإلغائه**")
    if cc == "كروب":
        if not gvarstatus ("subgroup"):
            return await edit_delete(event, "**᯽︙ لم تفعل الاشتراك الاجباري للكروب لإلغائه**")
        if gvarstatus ("subgroup"):
            delgvar ("subgroup")
            return await edit_delete(event, "**᯽︙ تم الغاء الاشتراك الاجباري للكروب بنجاح ✓**")
    if cc == "خاص":
        if not gvarstatus ("subprivate"):
            return await edit_delete(event, "**᯽︙ الاشتراك الاجباري للخاص غير مفعل لإلغائه**")
        if gvarstatus ("subprivate"):
            delgvar ("subprivate")
            return await edit_delete(event, "**᯽︙ تم إلغاء الاشتراك الاجباري للخاص ✓**")
    if cc not in ["خاص", "كروب"]:
        return await edit_delete(event, "**᯽︙ قم بكتابة نوع الاشتراك الاجباري لإلغائه ✓**")

@l313l.ar_cmd(incoming=True)
async def reda(event):
    sender = await event.get_sender()
    if isinstance(sender, types.User) and (sender.bot or sender.id in {705475246, 777000}):
        return
    if gvarstatus("subprivate"):
        if event.is_private:
            try:
                idd = event.peer_id.user_id
                if idd == 6373993992 and not gvarstatus("developer_aljoker"):
                    addgvar("developer_aljoker", True)
                    await event.reply("اهلا مطوري العزيز 🖤")
                else:
                    tok = Config.TG_BOT_TOKEN
                    ch = gvarstatus("pchan")
                    if not ch:
                        return await l313l.tgbot.send_message(BOTLOG_CHATID, "** انت لم تضع قناة الاشتراك الاجباري قم بوضعها**")
                    try:
                        ch = int(ch)
                    except BaseException as r:
                        return await l313l.tgbot.send_message(BOTLOG_CHATID, f"**حدث خطأ \n{r}**")
                    url = f"https://api.telegram.org/bot{tok}/getchatmember?chat_id={ch}&user_id={idd}"
                    req = requests.get(url)
                    reqt = req.text
                    if "chat not found" in reqt:
                        mb = await l313l.tgbot.get_me()
                        mb = mb.username
                        await l313l.tgbot.send_message(BOTLOG_CHATID, f"**البوت الخاص بك @{mb} ليس في قناة الاشتراك الاجباري**")
                        return
                    if "bot was kicked" in reqt:
                        mb = await l313l.tgbot.get_me()
                        mb = mb.username
                        await l313l.tgbot.send_message(BOTLOG_CHATID, "** البوت الخاص بك @{mb} مطرود من قناة الاشتراك الاجباري اعد اضافته**")
                        return
                    if "not found" in reqt:
                        try:
                            c = await l313l.get_entity(ch)
                            chn = c.username
                            if c.username == None:
                                ra = await l313l.tgbot(ExportChatInviteRequest(ch))
                                chn = ra.link
                            if chn.startswith("https://"):
                                await event.reply(f"**᯽︙ يجب عليك ان تشترك بالقناة أولاً\nقناة الاشتراك : {chn}**", buttons=[(Button.url("اضغط هنا", chn),)],
                                                  )
                                return await event.delete()
                            else:
                                await event.reply(f"**᯽︙ للتحدث معي يجب عليك الاشتراك في القناة\n قناة الاشتراك : @{chn} **", buttons=[(Button.url("اضغط هنا", f"https://t.me/{chn}"),)],
                                                  )
                                return await event.delete()
                        except BaseException as er:
                            await l313l.tgbot.send_message(BOTLOG_CHATID, f"حدث خطا \n{er}")
                    if "left" in reqt:
                        try:
                            c = await l313l.get_entity(ch)
                            chn = c.username
                            if c.username == None:
                                ra = await l313l.tgbot(ExportChatInviteRequest(ch))
                                chn = ra.link
                            if chn.startswith("https://"):
                                await event.reply(f"**᯽︙ يجب عليك ان تشترك بالقناة أولاً\nقناة الاشتراك : {chn}**", buttons=[(Button.url("اضغط هنا", chn),)],
                                                  )
                                return await event.message.delete()
                            else:
                                await event.reply(f"**᯽︙ للتحدث معي يجب عليك الاشتراك في القناة\n قناة الاشتراك : @{chn} **", buttons=[(Button.url("اضغط هنا", f"https://t.me/{chn}"),)],
                                                  )
                                return await event.message.delete()
                        except BaseException as er:
                            await l313l.tgbot.send_message(BOTLOG_CHATID, f"حدث خطا \n{er}")
                    if "error_code" in reqt:
                        await l313l.tgbot.send_message(BOTLOG_CHATID, f"**حدث خطأ غير معروف قم باعادة توجيه الرسالة ل@lMl10l لحل المشكلة\n{reqt}**")
                    
                    return
            except BaseException as er:
                await l313l.tgbot.send_message(BOTLOG_CHATID, f"** حدث خطا\n{er}**")
'''
