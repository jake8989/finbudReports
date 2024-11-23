from app.db.config import database
import asyncio


async def setup_database():
    await database.connect()


asyncio.run(setup_database())


async def getAllUsers():
    # await setup_database()
    user = await database.db["users"].find({}).to_list(length=None)
    print(user)


asyncio.run(getAllUsers())
