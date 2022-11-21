import datetime
import motor.motor_asyncio
from .. import MONGODB_URI

SESSION_NAME = 'videoconvertor'

class Database:
  
#Connection--------------------------------------------------------------------

    def __init__(self, MONGODB_URI, SESSION_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.db = self._client[SESSION_NAME]
        self.col = self.db.users

 #collection handling---------------------------------------------------------

    def new_user(self, id):
        return dict(id=id, banned=False, link=None)
           
    async def add_user(self,id):
        user = self.new_user(id)
        await self.col.insert_one(user)
      
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def banning(self, id):
        await self.col.update_one({'id': id}, {'$set': {'banned': True}})
    
    async def is_banned(self, id):
        user = await self.col.find_one({'id': int(id)})
        banned = user.get('banned', False)
        return banned
      
    async def unbanning(self, id):
        await self.col.update_one({'id': id}, {'$set': {'banned': False}})
        
    async def get_users(self):
        users = self.col.find({})
        return users
    
    async def set_thumb(self, original=True):
        if original:
            await self.thumb.update_one({}, {"$set": {"original": True}})
        else:
            async with aiofiles.open(localisation.Thumb, "rb") as f:
                byt = await f.read()
            await self.thumb.update_one({}, {"$set": {"original": False, "bytes": byt}})
        self.original = original
   
    
