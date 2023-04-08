# A asyncpg for postgres connections
from RUKA import DB_URI
import asyncpg
import asyncio

MAX_CONNECTIONS = 5 # default to 5 since elephant allow only 5 connections

class Database:
    def __init__(self, uri):
        self.pool = None
        self.uri = uri

        async def connect():
            self.pool = await asyncpg.create_pool(self.uri, min_size=1, max_size=MAX_CONNECTIONS)

        asyncio.get_event_loop().run_until_complete(connect())

    async def execute(self, query, *args, commit=False):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                print(f"Executing query: {query}, with data: {args}")
                result = await conn.execute(query, *args)
                if commit:
                    return None
                else:
                    return await result.fetchall()


sql_con = Database(DB_URI)
SQLDB = sql_con.execute  # Your SQLdb object for executing with one param commit whose default value set to False

"""
Dont simply kang, please give credits and one star for this help
This method solves the `To many connections error` in elephant sql or any other free postgresql
"""