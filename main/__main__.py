import logging

from telethon import events
from telethon.tl.custom.message import Message

from main.database import db
from main.client import bot
from main.config import Config
from main.utils import compress

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


@bot.on(events.NewMessage(incoming=True, from_users=Config.WhiteList))
async def video_handler(event: events.NewMessage.Event):
    msg: Message = event.message
    if not event.is_private or not event.media or not hasattr(msg.media, "document"):
        return
    if 'video' not in msg.media.document.mime_type:
        return
    if db.tasks >= Config.Max_Tasks:
        await bot.send_message(event.chat_id, f"💢 **Tʜᴇʀᴇ Aʀᴇ** {Config.Max_Tasks} **Tᴀѕᴋѕ Wᴏʀᴋɪɴɢ Nᴏᴡ**")
        return
    try:
        db.tasks += 1
        await compress(event)
    except Exception as e:
        print(e)
    finally:
        db.tasks -= 1


@bot.on(events.NewMessage(incoming=True, pattern="/as_video", from_users=Config.WhiteList))
async def as_video(event):
    await db.set_upload_mode(doc=False)
    await bot.send_message(event.chat_id, "✅ **I Wɪʟʟ Uᴘʟᴏᴀᴅ Tʜᴇ Fɪʟᴇѕ Aѕ Vɪᴅᴇᴏѕ**")


@bot.on(events.NewMessage(incoming=True, pattern="/as_document", from_users=Config.WhiteList))
async def as_video(event):
    await db.set_upload_mode(doc=True)
    await bot.send_message(event.chat_id, "✅ **I Wɪʟʟ Uᴘʟᴏᴀᴅ Tʜᴇ Fɪʟᴇѕ Aѕ Dᴏᴄᴜᴍᴇɴᴛѕ**")


@bot.on(events.NewMessage(incoming=True, pattern="/speed", from_users=Config.WhiteList))
async def set_crf(event):
    msg: Message = event.message
    parts = msg.text.split()
    if len(parts) != 2:
        await bot.send_message(event.chat_id, "🚀**Sᴇʟᴇᴄᴛɪᴏɴ Oғ Cᴏᴍᴘʀᴇѕѕɪᴏɴ Sᴘᴇᴇᴅ**\n\n "
                                              "`/speed veryfast` \n\n`/speed faster`\n\n`/speed ultrafast`")
    else:
        await db.set_speed(parts[1])
        await bot.send_message(event.chat_id, "✅ **Dᴏɴᴇ**")


@bot.on(events.NewMessage(incoming=True, pattern="/crf", from_users=Config.WhiteList))
async def set_crf(event):
    msg: Message = event.message
    parts = msg.text.split()
    if len(parts) != 2 or not parts[1].isnumeric():
        await bot.send_message(event.chat_id, "⚡️ **Sᴇʟᴇᴄᴛɪᴏɴ Oғ Cᴏᴍᴘʀᴇѕѕɪᴏɴ Rᴀᴛɪᴏ**\n\n `/crf 28`    ↩ ↪   `/crf 27`")
    else:
        await db.set_crf(int(parts[1]))
        await bot.send_message(event.chat_id, "✅ **Dᴏɴᴇ**")


@bot.on(events.NewMessage(incoming=True, pattern="/fps", from_users=Config.WhiteList))
async def set_fps(event):
    msg: Message = event.message
    parts = msg.text.split()
    if len(parts) != 2 or not parts[1].isnumeric():
        await bot.send_message(event.chat_id, "💢 **Iɴᴠᴀʟɪᴅ Sʏɴᴛᴀх**\n**Eхᴀᴍᴘʟᴇ**: `/fps 24`")
    else:
        await db.set_fps(int(parts[1]))
        await bot.send_message(event.chat_id, "✅ **Dᴏɴᴇ**")


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.photo, from_users=Config.WhiteList))
async def set_thumb(event):
    await bot.download_media(event.message, Config.Thumb)
    await db.set_thumb(original=False)
    await event.reply("✅ **Tʜᴜᴍʙɴᴀɪʟ Cʜᴀɴɢᴇᴅ**")


@bot.on(events.NewMessage(incoming=True, pattern="/original_thumb", from_users=Config.WhiteList))
async def original_thumb(event):
    await db.set_thumb(original=True)
    await event.reply("✅ **ɪ Wɪʟʟ Uѕᴇ Oʀɪɢɪɴᴀʟ Tʜᴜᴍʙɴᴀɪʟ**")


@bot.on(events.NewMessage(incoming=True, pattern="/original_fps", from_users=Config.WhiteList))
async def original_fps(event):
    await db.set_fps(None)
    await event.reply("✅ **I Wɪʟʟ Uѕᴇ Oʀɪɢɪɴᴀʟ FPS**")


@bot.on(events.NewMessage(incoming=True, pattern="/commands", from_users=Config.WhiteList))
async def commands(event):
    await event.reply("🤖 **Vɪᴅᴇᴏ Cᴏᴍᴘʀᴇѕѕɪᴏɴ Sᴇᴛᴛɪɴɢѕ**:\n\n/speed  **Cᴏᴍᴘʀᴇѕѕɪᴏɴ Sᴘᴇᴇᴅ**\n\n"
                      "/crf   **Cᴏᴍᴘʀᴇѕѕɪᴏɴ Rᴀᴛɪᴏ**\n\n/fps  **Fʀᴀᴍᴇѕ Pᴇʀ Sᴇᴄᴏɴᴅ**\n/original_fps   **Dᴇғᴀᴜʟᴛ FPS**\n\n"
                      "/as_video   **Uᴘʟᴏᴀᴅ Aѕ Vɪᴅᴇᴏ**\n/as_document  **Uᴘʟᴏᴀᴅ Aѕ Fɪʟᴇ**\n\n"
                      "/original_thumb **Dᴇғᴀᴜʟᴛ Tʜᴜᴍʙɴᴀɪʟ**\n\n🖼 **Sᴇɴᴅ Aɴʏ Pɪᴄᴛᴜʀᴇ Tᴏ Sᴇᴛ Iᴛ Aѕ Tʜᴜᴍʙɴᴀɪʟ**")


@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("**Sᴇɴᴅ Mᴇ Aɴʏ Vɪᴅᴇᴏ Tᴏ Cᴏᴍᴘʀᴇѕѕ**")


bot.loop.run_until_complete(db.init())
print("Bot-Started")
bot.run_until_disconnected()
