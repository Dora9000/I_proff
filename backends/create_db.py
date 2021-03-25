
import aioredis
from aioredis import Redis
#import asyncio


async def create_db(app):
    redis_conn = await aioredis.create_pool(loop=app.loop, **app['config']['redis'])
    app['redis'] = Redis(redis_conn)
    ids = [int(k) for k in await app['redis'].keys('*')]
    app['id'] = max(ids) if len(ids) > 0 else 0


async def close_db(app):
    app['redis'].close()
