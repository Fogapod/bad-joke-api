import asyncio
import os

from aiohttp import web

from config import Config
from updater import updater


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

@routes.post('/gitlab-webhook')
async def gitlab_webhook(req):
    if req.headers.get('X-Gitlab-Token') != req.app['config']['gitlab-webhook-token']:
        return web.Response(text='', status=401)

    # TODO: use logger
    print('[GIT] Recieved update from webhook, trying to pull ...')
    asyncio.ensure_future(updater(req.app))
    return web.Response()

if __name__ == '__main__':
    app = web.Application()
    app['config'] = Config('config.yaml')
    app.router.add_routes(routes)

    web.run_app(app)
