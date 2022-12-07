from motor.motor_asyncio import AsyncIOMotorClient
import aiofiles

from main.config import Config


class Database:
    def __init__(self):
        self.mongo = AsyncIOMotorClient(Config.DB_URI)
        self.db = self.mongo[Config.DB_NAME]
        self.config = self.db["config2"]
        self.thumb = self.db["thumb"]
        self.doc = False
        self.speed = "ultrafast"
        self.crf = 28
        self.fps = None
        self.original = True
        self.tasks = 0

    async def init(self):
        config = await self.config.find_one({})
        if config is None:
            await self.config.insert_one({"doc": self.doc, "speed": self.speed, "crf": self.crf, "fps": self.fps})
        else:
            self.doc = config["doc"]
            self.speed = config["speed"]
            self.crf = config["crf"]
            self.fps = config["fps"]
        thumb = await self.thumb.find_one({})
        if thumb is None:
            await self.thumb.insert_one({"original": True, "bytes": None})
        elif not thumb["original"]:
            self.original = False
            async with aiofiles.open(Config.Thumb, "wb") as f:
                await f.write(thumb["bytes"])

    async def set_speed(self, speed: str):
        self.speed = speed
        await self.config.update_one({}, {"$set": {"speed": speed}})

    async def set_crf(self, crf: int):
        self.crf = crf
        await self.config.update_one({}, {"$set": {"crf": crf}})

    async def set_fps(self, fps: [int, None]):
        self.fps = fps
        await self.config.update_one({}, {"$set": {"fps": fps}})

    async def set_thumb(self, original=True):
        if original:
            await self.thumb.update_one({}, {"$set": {"original": True}})
        else:
            async with aiofiles.open(Config.Thumb, "rb") as f:
                byt = await f.read()
            await self.thumb.update_one({}, {"$set": {"original": False, "bytes": byt}})
        self.original = original

    async def set_upload_mode(self, doc=False):
        self.doc = doc
        await self.config.update_one({}, {"$set": {"doc": doc}})


db = Database()
