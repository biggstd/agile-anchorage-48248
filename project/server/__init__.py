# project/server/__init__.py


import os
from threading import Thread
from tornado.ioloop import IOLoop

from bokeh.application import Application
from bokeh.application.handlers import DirectoryHandler
from tornado.httpserver import HTTPServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from bokeh.server.server import BaseServer

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()

print('APP CREATION ---------------------------------------------------')
# Declare the absolute path to the demo application.
demo_path = os.path.abspath("bokeh_apps/bokehDemo")

# Declare the dictionary of applications to launch.
apps = {
    '/bokehDemo': Application(DirectoryHandler(filename=demo_path)),
}

# Instantiate the Bokeh server.
# Allow connections from the Flask application.
bokeh_tornado = BokehTornado(
    applications=apps,
    extra_websocket_origins=[
        "127.0.0.1:5000",
        "localhost:8000",
        "http://localhost:8000",
        "0.0.0.0",
        "https://agile-anchorage-48248.herokuapp.com/",
    ],
    # port=5006
)

bokeh_http = HTTPServer(bokeh_tornado)
# server.start()
# server.io_loop.start()

# This is so that if this app is run using something like "gunicorn -w 4" then
# each process will listen on its own port
sockets, port = bind_sockets("localhost", 0)
bokeh_http.add_sockets(sockets)


def bk_worker():
    io_loop = IOLoop.current()
    server = BaseServer(io_loop, bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.server.user.views import user_blueprint
    from project.server.main.views import main_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)

    # flask login
    from project.server.models import User
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
