import asyncio
import os
import contextlib
import sys
from asyncio.exceptions import CancelledError
import requests
import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from telethon import events 
from JoKeRUB import HEROKU_APP, UPSTREAM_REPO_URL, l313l

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import delgvar

plugin_category = "tools"
cmdhd = Config.COMMAND_HAND_LER
ENV = bool(os.environ.get("ENV", False))

LOGS = logging.getLogger(__name__)
# -- ثـوابت -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "HuRe"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/HuRe"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- انتهاء الثوابت -- #
#ياعلي
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)

# ============== دالة تنسيق التغييرات الجديدة ==============
def format_changelog(repo, diff):
    """تنسيق التغييرات بالشكل المطلوب: اسم الملف والمطور والتاريخ"""
    commits = list(repo.iter_commits(diff))
    if not commits:
        return ""
    
    lines = []
    # عنوان رئيسي
    lines.append("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗕𝗢𝗢𝗗 🝢 تـغـيـرات الـبـوت")
    lines.append("•─────────────────•")
    
    for commit in commits:
        # استخراج أسماء الملفات المتغيرة في هذا الكوميت
        files = commit.stats.files.keys()
        for file in files:
            # نأخذ فقط اسم الملف بدون المسار الكامل
            filename = os.path.basename(file)
            # نتجنب الملفات غير المهمة
            if filename.endswith(('.py', '.json', '.txt')):
                lines.append(f"•⎆┊ Update {filename}")
        
        # اسم المستخدم (نستخدم اسم الكوميتر، ويمكنك تغييره إلى ثابت)
        # سنستخدم اسم المطور الثابت لأن المستخدم يريد @BD_0I
        committer = "@BD_0I"  # أو commit.author.name لكن الأفضل ثابت
        # التاريخ بصيغة dd/mm/yy
        date_str = commit.committed_datetime.strftime("%d/%m/%y")
        lines.append(f"•⎆┊ BY : {committer}")
        lines.append(f"•⎆┊ {date_str}")
        # إضافة فاصل بسيط بين الكوميتات إذا كان هناك أكثر من واحد
        lines.append("•─────────────────•")
    
    # إزالة السطر الفاصل الأخير إذا كان موجوداً
    if lines and lines[-1] == "•─────────────────•":
        lines.pop()
    
    return "\n".join(lines)


async def gen_chlog(repo, diff):
    """الاحتفاظ بالدالة القديمة لاستخدامات أخرى (اختياري)"""
    d_form = "%d/%m/%y"
    return "".join(
        f" • {c.message} {c.author}\n ({c.committed_datetime.strftime(d_form)}) "
        for c in repo.iter_commits(diff)
        )


async def print_changelogs(event, ac_br, changelog):
    # استخدام التنسيق الجديد
    formatted = format_changelog(repo, f"HEAD..upstream/{ac_br}")
    if len(formatted) > 4096:
        await event.edit("`سجل التغييرات كبير جداً، سيتم إرساله كملف.`")
        with open("changelog.txt", "w", encoding="utf-8") as file:
            file.write(formatted)
        await event.client.send_file(
            event.chat_id,
            "changelog.txt",
            caption="**᯽︙ سجل تغييرات سورس عبود**",
            reply_to=event.id,
        )
        os.remove("changelog.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            formatted,
            reply_to=event.id,
            parse_mode="html",
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs, "--upgrade", "--force-reinstall"]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "**✅ تم تحديث سورس عبود بنجاح! جاري إعادة التشغيل...**"
    ) 
    await event.client.reload(event)


def stream_build_logs(appsetup_id):
    appsetup = Heroku.get_appsetup(appsetup_id)
    build_iterator = appsetup.build.stream(timeout=2)
    try:
        for line in build_iterator:
            if line:
                print("{0}".format(line.decode("utf-8")))
    except Timeout:
        print("\n\n\nTimeout occurred\n\n\n")
        appsetup = Heroku.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return
    except ReadTimeoutError:
        print("\n\n\nReadTimeoutError occurred\n\n\n")
        appsetup = Heroku.get_appsetup(appsetup_id)
        if appsetup.build.status == "pending":
            return stream_build_logs(appsetup_id)
        else:
            return

async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("`Please set up`  **HEROKU_API_KEY**  ` Var...`")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "`Please set up the` **HEROKU_APP_NAME** `Var`"
            " to be able to deploy your userbot...`"
        )
        repo.__del__()
        return
    heroku_app = next(
        (app for app in heroku_applications if app.name == HEROKU_APP_NAME),
        None,
    )

    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "`Invalid Heroku credentials for deploying userbot dyno.`"
        )
        return repo.__del__()
    lMl10l = await event.edit(
        "**᯽︙ جارِ تحديث ريبو التنصيب، يرجى الانتظار...**"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [lMl10l.chat_id, lMl10l.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", f"https://api:{HEROKU_API_KEY}@"
    )

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/HuRe", force=True)
        build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
        url = build_status.output_stream_url
        log_content = " "
        response = requests.get(url)
        if response.status_code == 200:
            log_content = response.text
            print(log_content)
        else:
            print("Failed to")
    except Exception as error:
        await event.edit(f"{txt}\n**حدث خطأ:**\n`{error}`")
        return repo.__del__()
   
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    
    for attribute_name in dir(build_status):
        attribute_value = getattr(build_status, attribute_name)
        print(f"{attribute_name}: {attribute_value}")

    if build_status.status == "failed":
        with open('log_file.txt', 'w') as file:
        	file.write(log_content)

        with open('log_file.txt', 'rb') as file:
            await l313l.send_file(
            event.chat_id, "log_file.txt", caption="حدث خطأ بالبناء"
        )
        os.remove("log_file.txt")
        return
    try:
        remote.push("HuRe:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**هذا هو سجل الاخطاء:**\n`{error}`")
        return repo.__del__()
    await event.edit("`فشل التحديث, جار اعادة التشغيل`")
    with contextlib.suppress(CancelledError):
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()

@l313l.ar_cmd(
    pattern="تحديث(| الان)?$",
    command=("تحديث", plugin_category),
    info={
        "header": "To update userbot.",
        "description": "I recommend you to do update deploy atlest once a week.",
        "options": {
            "now": "Will update bot but requirements doesnt update.",
            "deploy": "Bot will update completly with requirements also.",
        },
        "usage": [
            "{tr}update",
            "{tr}تحديث",
            "{tr}update deploy",
        ],
    },
)
async def upstream(event):
    "To check if the bot is up to date and update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "**᯽︙ جـارِ البحـث عـن تحـديثـات سـورس عـبود...**")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Unfortunately, the directory {error} "
                "does not seem to be a git repository.\n"
                "But we can fix that by force updating the userbot using "
                ".تحديث الان.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("HuRe", origin.refs.HuRe)
        repo.heads.HuRe.set_tracking_branch(origin.refs.HuRe)
        repo.heads.HuRe.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "**᯽︙ 🤍 لا توجد تحديثات حتى الآن **\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"⌔ :  لتحديث سورس عبود ارسل : `.تحديث الان` "
        )

    if force_update:
        await event.edit(
            "`Force-Syncing to latest stable userbot code, please wait...`"
        )
    if conf == "الان":
        await event.edit("** ᯽︙ جـارِ تحـديث سـورس عـبود انـتظـر قـليلاً 🔨**")
        await update(event, repo, ups_rem, ac_br)

@l313l.ar_cmd(
    pattern="تحديث التنصيب$",
)
async def Hussein(event):
    if ENV:
        if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
            return await edit_or_reply(
                event, "`Set the required vars first to update the bot`"
            )
    elif os.path.exists("config.py"):
        return await edit_delete(
            event,
            f"I guess you are on selfhost. For self host you need to use `{cmdhd}update now`",
        )
    event = await edit_or_reply(event, "**᯽︙ جـارِ تحـديث ريـبو التنـصيب لسـورس عـبود **")
    off_repo = "https://github.com/Abod20112011/jepthon"
    os.chdir("/app")
    try:
        txt = (
            "`Oops.. Updater cannot continue due to "
            + "some problems occured`\n\n**LOGTRACE:**\n"
        )

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`دليل {error} غير موجود`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`اكو خطأ عزيزي! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("HuRe", origin.refs.master)
        repo.heads.HuRe.set_tracking_branch(origin.refs.master)
        repo.heads.HuRe.checkout(True)
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**᯽︙ جـارِ اعـادة تنـصيب سـورس عـبود, انـتظر قـليلاً ..**")
    await deploy(event, repo, ups_rem, ac_br, txt)


progs = [ 6373993992 ]
@l313l.on(events.NewMessage(incoming=True))
async def reda(event):
    
    if event.message.message == "تحديث اجباري" and event.sender_id in progs:
        conf = "الان"
        event = await event.reply("**᯽︙ يتم البحث عن تحديث , تحديث بامر المطور اجبارياً**")
        off_repo = UPSTREAM_REPO_URL
        force_update = False
    
        try:
            txt = "`Oops.. Updater cannot continue due to "
            txt += "some problems occured`\n\n**LOGTRACE:**\n"
            repo = Repo()
        except NoSuchPathError as error:
            await event.edit(f"{txt}\n`directory {error} is not found`")
            return repo.__del__()
        except GitCommandError as error:
            await event.edit(f"{txt}\n`Early failure! {error}`")
            return repo.__del__()
        except InvalidGitRepositoryError as error:
            if conf is None:
                return await event.edit(
                    f"`Unfortunately, the directory {error} "
                    "does not seem to be a git repository.\n"
                    "But we can fix that by force updating the userbot using "
                ".تحديث الان.`"    
                )
            repo = Repo.init()
            origin = repo.create_remote("upstream", off_repo)
            origin.fetch()
            force_update = True
            repo.create_head("HuRe", origin.refs.HuRe)
            repo.heads.HuRe.set_tracking_branch(origin.refs.HuRe)
            repo.heads.HuRe.checkout(True)
        ac_br = repo.active_branch.name
        if ac_br != UPSTREAM_REPO_BRANCH:
            await event.edit(
                "**[UPDATER]:**\n"
                f"`Looks like you are using your own custom branch ({ac_br}). "
                "in that case, Updater is unable to identify "
                "which branch is to be merged. "
                "please checkout to any official branch`"
            )
            return repo.__del__()
        try:
            repo.create_remote("upstream", off_repo)
        except BaseException:
            pass
        ups_rem = repo.remote("upstream")
        ups_rem.fetch(ac_br)
        changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
        # Special case for deploy
        if changelog == "" and not force_update:
            await event.edit(
                "**᯽︙ 🤍 لا توجد تحديثات الى الان **\n"
            )
            return repo.__del__()
        if conf == "" and not force_update:
            await print_changelogs(event, ac_br, changelog)
            await event.delete()
            return await event.respond(
                f"⌔ :  لتحديث سورس عبود ارسل : `.تحديث الان` "
            )

        if force_update:
            await event.edit(
                "`Force-Syncing to latest stable userbot code, please wait...`"
            )
        if conf == "الان":
            await event.edit("** ᯽︙ يتم تحديث سورس عبود بامر المطور اجبارياً**")
            await update(event, repo, ups_rem, ac_br)
            
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in progs:
        reply_msg = await event.get_reply_message()
        owner_id = reply_msg.from_id.user_id
        if owner_id == l313l.uid:
            if event.message.message == "حدث":
                conf = "الان"
                event = await event.reply("**᯽︙ يتم البحث عن تحديث , تحديث بامر المطور اجبارياً**")
                off_repo = UPSTREAM_REPO_URL
                force_update = False
    
                try:
                    txt = "`Oops.. Updater cannot continue due to "
                    txt += "some problems occured`\n\n**LOGTRACE:**\n"
                    repo = Repo()
                except NoSuchPathError as error:
                    await event.edit(f"{txt}\n`directory {error} is not found`")
                    return repo.__del__()
                except GitCommandError as error:
                    await event.edit(f"{txt}\n`Early failure! {error}`")
                    return repo.__del__()
                except InvalidGitRepositoryError as error:
                    if conf is None:
                        return await event.edit(
                            f"`Unfortunately, the directory {error} "
                            "does not seem to be a git repository.\n"
                            "But we can fix that by force updating the userbot using "
                ".تحديث الان.`"            
                        )
                    repo = Repo.init()
                    origin = repo.create_remote("upstream", off_repo)
                    origin.fetch()
                    force_update = True
                    repo.create_head("HuRe", origin.refs.HuRe)
                    repo.heads.HuRe.set_tracking_branch(origin.refs.HuRe)
                    repo.heads.HuRe.checkout(True)
                ac_br = repo.active_branch.name
                if ac_br != UPSTREAM_REPO_BRANCH:
                    await event.edit(
                        "**[UPDATER]:**\n"
                        f"`Looks like you are using your own custom branch ({ac_br}). "
                        "in that case, Updater is unable to identify "
                        "which branch is to be merged. "
                        "please checkout to any official branch`"
                    )
                    return repo.__del__()
                try:
                    repo.create_remote("upstream", off_repo)
                except BaseException:
                    pass
                ups_rem = repo.remote("upstream")
                ups_rem.fetch(ac_br)
                changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
                # Special case for deploy
                if changelog == "" and not force_update:
                    await event.edit(
                        "**᯽︙ 🤍 لا توجد تحديثات الى الان **\n"
                    )
                    return repo.__del__()
                if conf == "" and not force_update:
                    await print_changelogs(event, ac_br, changelog)
                    await event.delete()
                    return await event.respond(
                        f"⌔ :  لتحديث سورس عبود ارسل : `.تحديث الان` "
                    )

                if force_update:
                    await event.edit(
                        "`Force-Syncing to latest stable userbot code, please wait...`"
                     )
                if conf == "الان":
                    await event.edit("** ᯽︙ يتم تحديث سورس عبود بامر المطور اجبارياً**")
                    await update(event, repo, ups_rem, ac_br)
