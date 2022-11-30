import heroku3 

from decouple import config
from telegraph import upload_file
from telethon import events , Button
from telethon.errors.rpcerrorlist import UserNotParticipantError, FloodWaitError
from telethon.tl.functions.channels import GetParticipantRequest

from .. import Drone, AUTH_USERS, ACCESS_CHANNEL, MONGODB_URI

from main.Database.database import Database

def mention(name, id):
    return f'[{name}](tg://user?id={id})'

#Forcesub-----------------

async def force_sub(id):
    FORCESUB = config("FORCESUB", default=None)
    if not str(FORCESUB).startswith("-100"):
        FORCESUB = int("-100" + str(FORCESUB))
    ok = False
    try:
        x = await Drone(GetParticipantRequest(channel=int(FORCESUB), participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            ok = True
        else:
            ok = False
    except UserNotParticipantError:
        ok = True 
    return ok
    
#Heroku------------------------
   
async def heroku_restart():
    HEROKU_API = config("HEROKU_API", default=None)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    x = None
    if not HEROKU_API and HEROKU_APP_NAME:
        x = None
    else:
        try:
            acc = heroku3.from_key(HEROKU_API)
            bot = acc.apps()[HEROKU_APP_NAME]
            bot.restart()
            x = True
        except Exception as e:
            print(e)
            x = False
    return x

#Logging events on tg--------------------

async def LOG_START(event, ps_name):
    LOG_ID = config("LOG_ID", default=None)
    chat = LOG_ID
    if not str(LOG_ID).startswith("-100"):
        chat = int("-100" + str(LOG_ID))
    Tag = mention(event.sender.first_name, event.sender_id)
    text = f'{ps_name}\n\n**Uѕᴇʀ :** {Tag}'
    xx = await event.client.send_message(int(chat), text, link_preview=False)
    return xx

async def LOG_END(event, ps_name):
    LOG_ID = config("LOG_ID", default=None)
    chat = LOG_ID
    if not str(LOG_ID).startswith("-100"):
        chat = int("-100" + str(LOG_ID))
    await event.client.send_message(int(chat), f'{ps_name}', link_preview=False)

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, pattern="^/msg (.*)"))
async def msg(event):
    ok = await event.get_reply_message()
    if not ok:
        await event.reply("Reply to the message you want to send!")
    user = event.pattern_match.group(1)
    if not user:
        await event.reply("Give the user id you want me to send message. ")
    await Drone.send_message(int(user) , ok )
    await event.reply("Messsage sent.")
    
#Listing---------------------------

#Not in use
def one_trial_queue(id, List1):
    if f'{id}' in List1:
        return False
    
#Not in use
def two_trial_queue(id, List1, List2):
    if not f'{id}' in List1:
        List1.append(f'{id}')
    else:
        if not f'{id}' in List2:
            List2.append(f'{id}')
        else:
            return False

#Not in use        
def ps_queue(id, media, List1, List2):
    List1.append(f'{id}')
    List2.append(media)
    if not len(List1) < 2:
        return 'EMPTY'
    if len(List1) > 2:
        return 'FULL'

    
