import asyncio
import os

from aiohttp import web

from config import Config
from updater import updater_task


routes = web.RouteTableDef()

@routes.get('/')
async def index(req):
    return web.Response(text="It works")

@routes.get('/version')
async def version(req):
    loop = asyncio.get_event_loop()
    program = 'git show -s HEAD --format="Currently on commit made %cr by %cn: %s (%H)"'
    output = await loop.run_in_executor(None, os.popen, program)
    return web.Response(text=output.read())

async def start_background_tasks(app):
    app['updater'] = app.loop.create_task(updater_task(app))

async def cleanup_background_tasks(app):
    app['updater'].cancel()
    await app['updater']


if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.router.add_routes(routes)

    web.run_app(app)
