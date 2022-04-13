import uuid

from aiohttp import web

import xjsonrpc.server
from xjsonrpc.server.integration import aiohttp

methods_v1 = xjsonrpc.server.MethodRegistry()


@methods_v1.add(context='request')
async def add_user_v1(request: web.Request, user: dict):
    user_id = uuid.uuid4().hex
    request.config_dict['users'][user_id] = user

    return {'id': user_id, **user}


methods_v2 = xjsonrpc.server.MethodRegistry()


@methods_v2.add(context='request')
async def add_user_v2(request: web.Request, user: dict):
    user_id = uuid.uuid4().hex
    request.config_dict['users'][user_id] = user

    return {'id': user_id, **user}


app = web.Application()
app['users'] = {}

app_v1 = aiohttp.Application()
app_v1.dispatcher.add_methods(methods_v1)
app.add_subapp('/api/v1', app_v1.app)


app_v2 = aiohttp.Application()
app_v2.dispatcher.add_methods(methods_v2)
app.add_subapp('/api/v2', app_v2.app)

if __name__ == "__main__":
    web.run_app(app, host='localhost', port=8080)
