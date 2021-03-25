
import os
import argparse
from aiohttp import web
from backends.backends import setup_backends
from routes import setup_routes
from settings import CONFIG_PATH, get_config
from logger import setup_logger
import asyncio
import traceback


def setup_config(app, config_path=None):
    try:
        app['config'] = get_config(CONFIG_PATH)
    except Exception as e:
        app.logger.exception("config is broken.")
        return 1
    setup_logger(app)
    return 0


def setup_app(config_path=None):
    #app_middlewares = middlewares()
    app = web.Application()
    status = setup_config(app, config_path)
    if status == 1:
        app.logger.error("Cant start app")
        exit(1)
    setup_backends(app)
    setup_routes(app)
    return app


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--path')
    PARSER.add_argument('--port')
    PARSER.add_argument('--config')
    ARGS = PARSER.parse_args()

    OLD_UMASK = os.umask(0o022)
    os.umask(0)

    try:
        loop = asyncio.get_event_loop()
        app = setup_app(config_path=ARGS.config)
        web.run_app(app=app,
                    path=ARGS.path,
                    port=ARGS.port)
    except:
        print(traceback.format_exc())
    finally:
        os.umask(OLD_UMASK)
