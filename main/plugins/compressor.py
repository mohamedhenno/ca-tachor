import re
import os
import time
import asyncio
import subprocess

from datetime import datetime as dt
from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata

from .. import Drone, BOT_UN, LOG_CHANNEL

from LOCAL.localisation import SUPPORT_LINK, JPG, JPG2, JPG3, Thumb
from LOCAL.utils import ffmpeg_progress
from main.plugins.actions import LOG_START, LOG_END

async def compress(event, msg, ffmpeg_cmd=0, ps_name=None):
    if ps_name is None:
        ps_name = '**Cᴏᴍᴘʀᴇѕѕɪɴɢ**'
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "**Pʀᴇᴘᴀʀᴀᴛɪᴏɴ Tᴏ Pʀᴏᴄᴇѕѕ**", reply_to=msg.id)
    new_name = "out_" + dt.now().isoformat("_", "seconds")
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    mime = msg.file.mime_type
    if 'mp4' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif msg.video:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif 'x-matroska' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
        out = new_name + ".mp4"            
    elif 'webm' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".webm" 
        out = new_name + ".mp4"
    else:
        n = msg.file.name
        ext = (n.split("."))[1]
        out = new_name + ext
    DT = time.time()
    _ps = "Cᴏᴍᴘʀᴇѕѕ"
    if ps_name != "**Cᴏᴍᴘʀᴇѕѕɪɴɢ**":
        _ps = "Cᴏᴍᴘʀᴇѕѕ"
    log = await LOG_START(event, f'**{str(_ps)} Pʀᴏᴄᴇѕѕ Sᴛᴀʀᴛᴇᴅ**\n\n[Bᴏᴛ Iѕ Bᴜѕʏ Nᴏᴡ]({SUPPORT_LINK})')
    log_end_text = f'**{_ps} Pʀᴏᴄᴇѕѕ Fɪɴɪѕʜᴇᴅ**\n\n[Bᴏᴛ Iѕ Fʀᴇᴇ Nᴏᴡ]({SUPPORT_LINK})'
    try:
        thumb = await Drone.download_media(msg, thumb=-1) if Thumb["original"] else Thumb["pic"]
        await fast_download(n, file, Drone, edit, DT, "**Dᴏᴡɴʟᴏᴀᴅɪɴɢ**")
    except Exception as e:
        os.rmdir("encodemedia")
        await log.delete()
        await LOG_END(event, log_end_text)
        print(e)
        return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Dᴏᴡɴʟᴏᴀᴅɪɴɢ**\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False) 
    name = '__' + dt.now().isoformat("_", "seconds") + ".mp4"
    os.rename(n, name)
    await edit.edit("**Eхᴛʀᴀᴄᴛɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ** . . .")
    vid = video_metadata(name)
    hgt = int(vid['height'])
    wdt = int(vid['width'])
    FT = time.time()
    progress = f"progress-{FT}.txt"
    cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" None """{out}""" -y'
    if ffmpeg_cmd == 1:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset ultrafast -vcodec libx265 -crf 28 -acodec copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 2:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset veryfast -vcodec libx265 -crf 30 -acodec copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 3:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset veryfast -vcodec libx265 -crf 28 -acodec copy -c:s copy """{out}""" -y'
    elif ffmpeg_cmd == 4:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset fast -vcodec libx265 -crf 28 -acodec copy -c:s copy """{out}""" -y'
    try:
        await ffmpeg_progress(cmd, name, progress, FT, edit, ps_name, log=log)
    except Exception as e:
        await log.delete()
        await LOG_END(event, log_end_text)
        os.rmdir("encodemedia")
        print(e)
        return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ FFMPEG Pʀᴏɢʀᴇѕѕ**\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False)  
    out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    if msg.file.name:
        out2 = msg.file.name
    else:
        out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    os.rename(out, out2)
    i_size = os.path.getsize(name)
    f_size = os.path.getsize(out2)     
    text = F'**Cᴏᴍᴘʀᴇѕѕᴇᴅ Bʏ**: @{BOT_UN}'
    if ps_name != "**Cᴏᴍᴘʀᴇѕѕɪɴɢ:**":
        text = f'**Cᴏᴍᴘʀᴇѕѕᴇᴅ Bʏ** : @{BOT_UN}\n\n**Bᴇғᴏʀᴇ Cᴏᴍᴘʀᴇѕѕɪɴɢ**: `{i_size}`\n**Aғᴛᴇʀ Cᴏᴍᴘʀᴇѕѕɪɴɢ**: `{f_size}`'
    UT = time.time()
    await log.edit("**Uᴘʟᴏᴀᴅɪɴɢ Fɪʟᴇ** 🔰")
    if 'x-matroska' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ :**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=thumb, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Uᴘʟᴏᴀᴅɪɴɢ**.\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False)
    elif 'webm' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ :**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=thumb, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("encodemedia")
            print(e)
            return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Uᴘʟᴏᴀᴅɪɴɢ**.\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False)
    else:
        metadata = video_metadata(out2)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ :**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=thumb, attributes=attributes, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ :**')
                await Drone.send_file(event.chat_id, uploader, caption=text, thumb=thumb, force_document=True)
            except Exception as e:
                await log.delete()
                await LOG_END(event, log_end_text)
                os.rmdir("encodemedia")
                print(e)
                return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Uᴘʟᴏᴀᴅɪɴɢ**.\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False)
    await edit.delete()
    os.remove(name)
    os.remove(out2)
    await log.delete()
    log_end_text2 = f'**{_ps} Pʀᴏᴄᴇѕѕ Fɪɴɪѕʜᴇᴅ**\n\n**Tɪᴍᴇ Tᴀᴋᴇɴ**: {round((time.time()-DT)/60)} Mɪɴᴜᴛᴇѕ\n**Iɴɪᴛɪᴀʟ Sɪᴢᴇ**: {i_size/1000000}ᴍʙ.\n**Fɪɴᴀʟ Sɪᴢᴇ**: {f_size/1000000}ᴍʙ.\n\n[Bᴏᴛ Iѕ Fʀᴇᴇ Nᴏᴡ.]({SUPPORT_LINK})'
    await LOG_END(event, log_end_text2)
    


