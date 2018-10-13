import asyncio
import os
import logging

from aiohttp import web

from reporter import send_report
from config import Config
from log import git_log, setup_logging
from updater import updater


try:
    import uvloop
except ImportError:
    print('Warning: uvloop library not installed or not supported on your system')
    print('Warning: Using default asyncio event loop')
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

routes = web.RouteTableDef()

@web.middleware
async def middleware(req, handler):
    try:
        resp = await handler(req)
    except web.HTTPException as e:
        raise
    except Exception as e:
        log = logging.getLogger('aiohttp.server')
        log.exception('Error handling request', exc_info=e, extra={'request': req})
        return web.Response(text='Internal server error.', status=500)

    return resp

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

    git_log.info('Received update from webhook, trying to pull ...')
    asyncio.ensure_future(updater(req.app))
    return web.Response()

if __name__ == '__main__':
    app = web.Application(middlewares=[middleware])
    app.router.add_routes(routes)

    app['config'] = Config('config.yaml')

    setup_logging(app)

    web.run_app(app)
