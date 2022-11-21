import os
import time
import asyncio

from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata

from .. import Drone, ACCESS_CHANNEL, LOG_CHANNEL, MONGODB_URI, FORCESUB_UN

from main.plugins.compressor import compress
from main.plugins.encoder import encode
from main.Database.database import Database
from main.plugins.actions import force_sub
from LOCAL.localisation import SUPPORT_LINK

#Don't be a MF by stealing someone's hardwork.
forcesubtext = f"**Tʜɪѕ Bᴏᴛ Fᴏʀ Pᴇʀѕᴏɴᴀʟ Uѕᴇ !!**\n\n**Tᴏ Uѕᴇ Tʜɪѕ Bᴏᴛ Yᴏᴜ'ᴠᴇ Tᴏ Jᴏɪɴ**👇 {FORCESUB_UN}\n\n**Aʟѕᴏ Jᴏɪɴ**\nhttps://t.me/+uPg3TPNFuckwMDU0"


@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def compin(event):
    db = Database(MONGODB_URI, 'videoconvertor')
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.reply(f'**Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ Tᴏ Usᴇ Mᴇ!**\n\n**Cᴏɴᴛᴀᴄᴛ** [SUPPORT]({SUPPORT_LINK})', link_preview=False)
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("**Vɪᴅᴇᴏ Cᴏɴᴠᴇʀᴛᴏʀ**",
                            buttons=[
                                [Button.inline("Eɴᴄᴏᴅᴇ x265", data="encode"),
                                 Button.inline("Cᴏᴍᴘʀᴇѕѕ HEVC", data="compress")]
                            ])

    await event.forward_to(int(ACCESS_CHANNEL))
    
@Drone.on(events.callbackquery.CallbackQuery(data="encode"))
async def _encode(event):
    await event.edit("**Cᴏᴍᴘʀᴇѕѕ & Cʜᴀɴɢᴇ Vɪᴅᴇᴏ Rᴇѕᴏʟᴜᴛɪᴏɴ**",
                    buttons=[
                        [Button.inline("240p", data="240"),
                         Button.inline("360p", data="360")],
                        [Button.inline("480p", data="480"),
                         Button.inline("720p", data="720")],
                        [Button.inline("Bᴀᴄᴋ", data="back")]])
     
@Drone.on(events.callbackquery.CallbackQuery(data="compress"))
async def _compress(event):
    await event.edit("**Cᴏᴍᴘʀᴇѕѕ HEVC**",
                    buttons=[
                        [Button.inline("🚀 Fᴀѕᴛ", data="hcomp"),
                          Button.inline("🚀 Mᴇᴅɪᴜᴍ", data="265")],
                          [Button.inline("🚀 Sʟᴏᴡ", data="264"),
                          Button.inline("Hɪɢʜ Cᴏᴍᴘʀᴇѕѕ", data="fcomp")],
                         [Button.inline("Bᴀᴄᴋ", data="back")]])


@Drone.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("**Vɪᴅᴇᴏ Cᴏɴᴠᴇʀᴛᴏʀ**", buttons=[
                    [Button.inline("Eɴᴄᴏᴅᴇ x265", data="encode"),
                     Button.inline("Cᴏᴍᴘʀᴇѕѕ HEVC", data="compress")]])
    
#-----------------------------------------------------------------------------------------

process1 = []
timer = []

#Set timer to avoid spam
async def set_timer(event, list1, list2):
    now = time.time()
    list2.append(f'{now}')
    list1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, '**Yᴏᴜ Cᴀɴ Sᴛᴀʀᴛ A Nᴇᴡ Pʀᴏᴄᴇѕѕ Aɢᴀɪɴ Aғᴛᴇʀ 1 Mɪɴᴜᴛᴇ**')
    await asyncio.sleep(60)
    list2.pop(int(timer.index(f'{now}')))
    list1.pop(int(process1.index(f'{event.sender_id}')))
    
#check time left in timer
async def check_timer(event, list1, list2):
    if f'{event.sender_id}' in list1:
        index = list1.index(f'{event.sender_id}')
        last = list2[int(index)]
        present = time.time()
        return False, f"Yᴏᴜ Hᴀᴠᴇ Tᴏ Wᴀɪᴛ {60-round(present-float(last))} Sᴇᴄᴏɴᴅѕ Mᴏʀᴇ Tᴏ Sᴛᴀʀᴛ ᴀ Nᴇᴡ Pʀᴏᴄᴇѕѕ!"
    else:
        return True, None
    
    
@Drone.on(events.callbackquery.CallbackQuery(data="fcomp"))
async def fcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Yᴏᴜ Hᴀᴠᴇ Tᴏ Wᴀɪᴛ {60-round(present-float(last))} Sᴇᴄᴏɴᴅѕ Mᴏʀᴇ Tᴏ Sᴛᴀʀᴛ ᴀ Nᴇᴡ Pʀᴏᴄᴇѕѕ!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=2, ps_name="**Hɪɢʜ Cᴏᴍᴘʀᴇѕѕ ⚡ Mᴇᴅɪᴜᴍ Sᴘᴇᴇᴅ**")
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, '**Yᴏᴜ Cᴀɴ Sᴛᴀʀᴛ A Nᴇᴡ Pʀᴏᴄᴇѕѕ Aɢᴀɪɴ Aғᴛᴇʀ 1 Mɪɴᴜᴛᴇ**')
        await asyncio.sleep(60)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
                       
@Drone.on(events.callbackquery.CallbackQuery(data="hcomp"))
async def hcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Yᴏᴜ Hᴀᴠᴇ Tᴏ Wᴀɪᴛ {60-round(present-float(last))} Sᴇᴄᴏɴᴅѕ Mᴏʀᴇ Tᴏ Sᴛᴀʀᴛ ᴀ Nᴇᴡ Pʀᴏᴄᴇѕѕ!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=1, ps_name="**Hɪɢʜ Sᴘᴇᴇᴅ Cᴏᴍᴘʀᴇѕѕ**")
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, '**Yᴏᴜ Cᴀɴ Sᴛᴀʀᴛ A Nᴇᴡ Pʀᴏᴄᴇѕѕ Aɢᴀɪɴ Aғᴛᴇʀ 1 Mɪɴᴜᴛᴇ**.')
        await asyncio.sleep(60)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)

@Drone.on(events.callbackquery.CallbackQuery(data="264"))
async def _264(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=4, ps_name="**Sʟᴏᴡ Sᴘᴇᴇᴅ Cᴏᴍᴘʀᴇѕѕ**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
      
@Drone.on(events.callbackquery.CallbackQuery(data="265"))
async def _265(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=3, ps_name="**Mᴇᴅɪᴜᴍ Sᴘᴇᴇᴅ Cᴏᴍᴘʀᴇѕѕ**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
        
@Drone.on(events.callbackquery.CallbackQuery(data="240"))
async def _240(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=240)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
        
@Drone.on(events.callbackquery.CallbackQuery(data="360"))
async def _360(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=360)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
        
@Drone.on(events.callbackquery.CallbackQuery(data="480"))
async def _480(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=480)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)
        
@Drone.on(events.callbackquery.CallbackQuery(data="720"))
async def _720(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=720)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"**Aɴᴏᴛʜᴇʀ Pʀᴏᴄᴇѕѕ Iɴ Pʀᴏɢʀᴇѕѕ**!\n\n[Lᴏɢ Cʜᴀɴɴᴇʟ](https://t.me/{LOG_CHANNEL})", link_preview=False)

