from aiohttp import web

from updater import updater_task


routes = web.RouteTableDef()

@routes.get('/')
async def index(req):
    return web.Response(text="It works")

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
