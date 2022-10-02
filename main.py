import logging
from aiohttp import web


logging.basicConfig(filename='user_actions.log', level=logging.INFO,
                    format="%(asctime)s;%(message)s")
log = logging.getLogger()


def init_app() -> web.Application:
    app = web.Application()
    app['buttons_colors'] = ['red', 'blue', 'green', 'yellow']
    app.add_routes([
        web.get('/', index_handler),
        web.post('/button_handler', button_handler),
    ])
    return app


async def index_handler(_) -> web.StreamResponse:
    log.info('Пользователь зашел на страницу.')
    return web.FileResponse('./index.html')


async def button_handler(request: web.Request) -> web.Response:
    match await request.json():
        case {'action_type': 'button_click',
              'button_id': button_id}:
            background_color = request.app['buttons_colors'][button_id]
            log.info('Пользователь нажал на кнопку %d', button_id)
            log.info('Установлен цвет: %s', background_color)
            return web.json_response({'background_color': background_color})
        case _:
            raise web.HTTPBadRequest()


if __name__ == '__main__':
    web.run_app(init_app(), host='localhost', port=80, access_log=None)
