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

from main.plugins.actions import LOG_START, LOG_END
from LOCAL.localisation import SUPPORT_LINK, JPG, JPG2, JPG3, Thumb
from LOCAL.utils import ffmpeg_progress

async def encode(event, msg, scale=0):
    ps_name = str(f"**{scale}p x265 Eɴᴄᴏᴅɪɴɢ**")
    _ps = str(f"{scale}p x265 Eɴᴄᴏᴅᴇ")
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
    log = await LOG_START(event, f'**{_ps} Pʀᴏᴄᴇѕѕ Sᴛᴀʀᴛᴇᴅ**\n\n[Bᴏᴛ Iѕ Bᴜѕʏ Nᴏᴡ]({SUPPORT_LINK})')
    log_end_text = f'**{_ps} Pʀᴏᴄᴇѕѕ Fɪɴɪѕʜᴇᴅ**\n\n[Bᴏᴛ Iѕ Fʀᴇᴇ Nᴏᴡ]({SUPPORT_LINK})'
    try:
        thumb = await Drone.download_media(msg, thumb=-1) if Thumb["original"] else Thumb["pic"]
        await fast_download(n, file, Drone, edit, DT, "**Dᴏᴡɴʟᴏᴀᴅɪɴɢ**")
    except Exception as e:
        os.rmdir("encodemedia")
        await log.delete()
        await LOG_END(event, log_end_text)
        print(e)
        return await edit.edit(f"**Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ Wʜɪʟᴇ Dᴏᴡɴʟᴏᴀᴅɪɴɢ**.\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})", link_preview=False) 
    name = '__' + dt.now().isoformat("_", "seconds") + ".mp4"
    os.rename(n, name)
    await edit.edit("**Eхᴛʀᴀᴄᴛɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ**. . .")
    vid = video_metadata(name)
    hgt = int(vid['height'])
    wdt = int(vid['width'])
    if scale == hgt:
        os.rmdir("encodemedia")
        return await edit.edit(f"Tʜᴇ Vɪᴅᴇᴏ Iѕ Aʟʀᴇᴀᴅʏ Iɴ {scale}ᴘ Rᴇѕᴏʟᴜᴛɪᴏɴ")
    if scale == 240:
        if 426 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"Tʜᴇ Vɪᴅᴇᴏ Iѕ Aʟʀᴇᴀᴅʏ Iɴ {scale}ᴘ Rᴇѕᴏʟᴜᴛɪᴏɴ")
    if scale == 360:
        if 640 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"Tʜᴇ Vɪᴅᴇᴏ Iѕ Aʟʀᴇᴀᴅʏ Iɴ {scale}ᴘ Rᴇѕᴏʟᴜᴛɪᴏɴ")
    if scale == 480:
        if 854 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"Tʜᴇ Vɪᴅᴇᴏ Iѕ Aʟʀᴇᴀᴅʏ Iɴ {scale}ᴘ Rᴇѕᴏʟᴜᴛɪᴏɴ")
    if scale == 720:
        if 1280 == wdt:
            os.rmdir("encodemedia")
            return await edit.edit(f"Tʜᴇ Vɪᴅᴇᴏ Iѕ Aʟʀᴇᴀᴅʏ Iɴ {scale}ᴘ Rᴇѕᴏʟᴜᴛɪᴏɴ")
    FT = time.time()
    progress = f"progress-{FT}.txt"
    cmd = ''
    if scale == 240:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx265 -crf 20 -preset faster -s 440x240 -c:a copy -c:s copy """{out}""" -y'
    elif scale == 360:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx265 -crf 22 -preset faster -s 640x360 -c:a copy -c:s copy """{out}""" -y'
    elif scale == 480:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx265 -crf 22 -preset faster -s 854x480 -c:a copy -c:s copy """{out}""" -y'
    elif scale == 720:
        cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -c:v libx265 -crf 28 -preset faster -s 1280x720 -c:a copy -c:s copy """{out}""" -y'
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
    text = f'**{_ps}ᴅ Bʏ** : @{BOT_UN}'
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
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ:**')
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
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ:**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=thumb, attributes=attributes, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Uᴘʟᴏᴀᴅɪɴɢ:**')
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
    
