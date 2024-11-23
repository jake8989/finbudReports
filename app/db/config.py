import os
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            print("Pinging mongodb...")
            self.client = AsyncIOMotorClient(os.getenv("DB_URL"))
            self.db = self.client.get_database()
            print("Mongo Connected!")
        except Exception as e:
            print(e)

    async def close(self):
        if self.client:
            self.client.close()
            print("Mongo Disconnected!")


database = Database()
