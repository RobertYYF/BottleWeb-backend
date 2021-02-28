import bottle

from api import register, test, login
from config import db_config, cors_config

app = application = bottle.default_app()
# Load Database Plugin
app.install(db_config.plugin)

# Use 'paste' server to utilize performance for multi-threaded machine
if __name__ == '__main__':
    # run in docker
    bottle.run(server = 'paste', host = '0.0.0.0', port = 8080, debug=True, reloader=True)

    # run on host
    # bottle.run(server = 'paste', host = 'localhost', port = 8080, debug=True, reloader=True)