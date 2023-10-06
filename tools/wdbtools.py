import os
import asyncio
import aiomysql
import ssl
import wconfig

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile=wconfig.SSL_CERT_PATH)

loop = asyncio.get_event_loop()

async def connect_db():
   connection = await aiomysql.connect(
       host=wconfig.DATABASE_HOST,
       port=3306,
       user=wconfig.DATABASE_USERNAME,
       password=wconfig.DATABASE_PASSWORD,
       db=wconfig.DATABASE,
       loop=loop,
       ssl=ctx
   )
   cursor = await connection.cursor()
   await cursor.execute("select @@version")
   version = await cursor.fetchall()
   print('Running version: ', version)
   await cursor.close()
   connection.close()
loop.run_until_complete(connect_db())