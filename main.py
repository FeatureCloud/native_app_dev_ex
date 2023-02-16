from bottle import Bottle

from FeatureCloud.app.api.http_ctrl import api_server
from FeatureCloud.app.api.http_web import web_server
from FeatureCloud.app.engine.app import app
import os
import states

server = Bottle()


def run_app():
    server.mount('/api', api_server)
    server.mount('/web', web_server)
    server.run(host='localhost', port=5000)


def is_native():
    path_prefix = os.getenv("PATH_PREFIX")
    if path_prefix:
        return False
    return True


if __name__ == '__main__':
    if is_native():
        app.register()
        app.handle_setup(client_id='1', coordinator=True, clients=['1'])
    else:
        run_app()
