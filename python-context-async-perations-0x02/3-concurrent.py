import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        # this allows me to access data by the column name
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users")as cursor:
            print("Retrieving all users")
            async for row in cursor:
                print(f"{row['user_id']}: {row['name']} - {row['age']}")
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            print("Retrieving users above 40")
            async for row in cursor:
                print(f"{row['user_id']}: {row['name']} - {row['age']}")
            return await cursor.fetchall()


async def fetch_concurrently():
    fetch_tasks = await asyncio.gather(async_fetch_users(), async_fetch_older_users())


# runs coroutines by running the entry point
asyncio.run(fetch_concurrently())
