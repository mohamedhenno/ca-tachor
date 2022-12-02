
from telethon import events, Button
from ethon.teleutils import mention
from ethon.mystarts import vc_menu

from .. import Drone, ACCESS_CHANNEL, AUTH_USERS

from main.plugins.actions import heroku_restart
from LOCAL.localisation import START_TEXT as st
from LOCAL.localisation import info_text, spam_notice, help_text, DEV, SUPPORT_LINK

@Drone.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("Mᴇɴᴜ ⚙", data="menu")]
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await Drone.send_message(int(ACCESS_CHANNEL), f'{tag} Started The BOT')
    
@Drone.on(events.callbackquery.CallbackQuery(data="menu"))
async def menu(event):
    await event.edit("**Vɪᴅᴇᴏ Cᴏᴍᴘʀᴇѕѕ**", 
                    buttons=[
                        [Button.inline("Rᴇѕᴛᴀʀᴛ", data="restart"),
                         Button.inline("Nᴏᴛɪᴄᴇ", data="notice"),
                         Button.inline("Mᴀɪɴ", data="help")],
                        [Button.url("Dᴇᴠᴇʟᴏᴘᴇʀ", url="t.me/A7_SYR")]
                        ])
    
@Drone.on(events.callbackquery.CallbackQuery(data="info"))
async def info(event):
    await event.edit(f'**IɴFᴏ**\n\n{info_text}',
                    buttons=[[
                         Button.inline("Mᴇɴᴜ", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="notice"))
async def notice(event):
    await event.answer(f'{spam_notice}', alert=True)
    
                    
@Drone.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit('**👥   Hᴇʟᴘ**',
                    buttons=[[
                         Button.inline("Pʟᴜɢɪɴѕ", data="plugins"),
                         Button.inline("Iɴғᴏ", data="info")],
                         [Button.url("Sᴜᴘᴘᴏʀᴛ", url=f"{SUPPORT_LINK}")],
                         [
                         Button.inline("Bᴀᴄᴋ", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="plugins"))
async def plugins(event):
    await event.edit(f'{help_text}',
                    buttons=[[Button.inline("Mᴇɴᴜ", data="menu")]])
                   
 #----------------------------
    
@Drone.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("❌ **Oɴʟʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ Uѕᴇʀ Cᴀɴ Rᴇѕᴛᴀʀᴛ ‼️** 🚫")
    result = await heroku_restart()
    if result is None:
        await event.edit("You have not filled `HEROKU_API` and `HEROKU_APP_NAME` vars.")
    elif result is False:
        await event.edit("Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ!")
    elif result is True:
        await event.edit("**Rᴇѕᴛᴀʀᴛɪɴɢ Aᴘᴘ ♻️ ... Wᴀɪᴛ Fᴏʀ A Mɪɴᴜᴛᴇ** ⏳")
