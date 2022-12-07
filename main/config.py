import os


class Config:
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("BOT_TOKEN")
    Max_Tasks = int(os.environ.get("Max_Tasks", 1))
    WhiteList = [int(uid) for uid in os.environ.get("AUTH_USERS").split()]
    DB_URI = os.environ.get("MONGODB_URI")
    DB_NAME = "VideoConverter"
    Thumb = "Thumb.jpg"
    InDir = "IN"
    OutDir = "OUT"
