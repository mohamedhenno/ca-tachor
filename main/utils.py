from time import time
import asyncio
import math
import os
import re
import ffmpeg

from telethon.tl.types import Message, DocumentAttributeFilename, DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata, total_frames as tf

from main.client import bot
from main.config import Config
from main.database import db


async def compress(event):
    msg: Message = event.message
    attributes = msg.media.document.attributes
    mime_type = msg.media.document.mime_type
    edit = await bot.send_message(event.chat_id, "**Pʀᴇᴘᴀʀᴀᴛɪᴏɴ Tᴏ Pʀᴏᴄᴇѕѕ**", reply_to=msg.id)

    for attr in attributes:
        if isinstance(attr, DocumentAttributeFilename):
            file_name = attr.file_name
            break
    else:
        ext = mime_type.split("/")[1]
        file_name = f"video.{ext}"

    if not os.path.isdir(Config.InDir):
        os.mkdir(Config.InDir)
    in_path = os.path.join(Config.InDir, file_name)

    try:
        await fast_download(in_path, msg.media.document, bot, edit, time(), "**Dᴏᴡɴʟᴏᴀᴅɪɴɢ**...")
    except Exception as e:
        print(e)
        return await edit.edit(f"💢 **Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Dᴏᴡɴʟᴏᴀᴅɪɴɢ**", link_preview=False)
    if not os.path.isdir(Config.OutDir):
        os.mkdir(Config.OutDir)
    out_path = os.path.join(Config.OutDir, file_name)

    FT = time()
    progress = f"progress-{FT}.txt"
    fps = f" -r {db.fps}" if db.fps else ""
    cmd = (f'ffmpeg -hide_banner -loglevel quiet'
           f' -progress {progress} -i """{in_path}"""'
           f' -preset {db.speed} -vcodec libx265 -crf {db.crf}'
           f'{fps} -acodec copy -c:s copy """{out_path}""" -y')
    try:
        await ffmpeg_progress(cmd, in_path, progress, FT, edit)
    except Exception as e:
        os.rmdir("encodemedia")
        print(e)
        return await edit.edit(f"💢***Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ FFMPEG Pʀᴏɢʀᴇѕѕ**", link_preview=False)

    in_size = humanbytes(os.path.getsize(in_path))
    out_size = humanbytes(os.path.getsize(out_path))
    text = f'**Bᴇғᴏʀᴇ Cᴏᴍᴘʀᴇѕѕɪɴɢ**: `{in_size}`\n**Aғᴛᴇʀ Cᴏᴍᴘʀᴇѕѕɪɴɢ**: `{out_size}`\n\n**POWERED BY  @A7_SYR**'
    if db.original:
        thumb = await bot.download_media(msg, thumb=-1)
    else:
        thumb = Config.Thumb
    try:
        uploader = await fast_upload(out_path, file_name, time(), bot, edit, '**Uᴘʟᴏᴀᴅɪɴɢ**')
        if db.doc:
            await bot.send_file(event.chat_id, uploader, thumb=thumb, force_document=True)
        else:
            try:
                metadata = video_metadata(out_path)
                width = metadata["width"]
                height = metadata["height"]
                duration = metadata["duration"]
                attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
                await bot.send_file(event.chat_id, uploader, thumb=thumb, attributes=attributes, force_document=False)
            except Exception as e:
                print(e)
                await bot.send_file(event.chat_id, uploader, thumb=thumb, force_document=True)
        await bot.send_message(event.chat_id, text)
    except Exception as e:
        print(e)
        return await edit.edit(f"💢 **Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Uᴘʟᴏᴀᴅɪɴɢ**", link_preview=False)

    await edit.delete()
    os.remove(in_path)
    os.remove(out_path)


async def ffmpeg_progress(cmd, file, progress, now, event):
    total_frames = tf(file)
    with open(progress, "w"):
        pass
    proce = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while proce.returncode != 0:
        await asyncio.sleep(3)
        with open(progress, "r+") as fil:
            text = fil.read()
            frames = re.findall("frame=(\\d+)", text)
            size = re.findall("total_size=(\\d+)", text)
            speed = 0
            if len(frames):
                elapse = int(frames[-1])
            if len(size):
                size = int(size[-1])
                per = elapse * 100 / int(total_frames)
                time_diff = time() - int(now)
                speed = round(elapse / time_diff, 2)
            if int(speed) != 0:
                some_eta = int(((int(total_frames) - elapse) / speed) * 1000)
                progress_str = "**[{0}{1}]** `| {2}%\n\n`".format(
                    "".join("▩" for _ in range(math.floor(per / 5))),
                    "".join("▢" for _ in range(20 - math.floor(per / 5))),
                    round(per, 2),
                )
                e_size = humanbytes(size) + " ᴏғ " + humanbytes((size / per) * 100)
                eta = time_formatter(some_eta)
                await event.edit(f'🗜 **Cᴏᴍᴘʀᴇѕѕɪɴɢ HEVC**\n\n{progress_str}' + f'**Gʀᴏѕѕ**: {e_size}\n\n⏰ **Tɪᴍᴇ Lᴇғᴛ :** {eta}')


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s:") if seconds else "")
    )
    if tmp.endswith(":"):
        return tmp[:-1]
    else:
        return tmp


def humanbytes(size):
    if size in [None, ""]:
        return "0 B"
    for unit in ["ʙ", "ᴋʙ", "ᴍʙ", "ɢʙ", "TB", "PB", "EB", "ZB", "YB"]:
        if size < 1024:
            break
        size /= 1024
    return f"{size:.2f} {unit}"
