# project/server/__init__.py


import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers import DirectoryHandler
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
from threading import Thread


# import pandas as pd


BOKEH_PORTS = list()

# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


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


# def bk_worker():
#
#     # Declare the absolute path to the demo application.
#     demo_path = os.path.abspath("project/bokeh_apps/demo")
#
#     # Declare the dictionary of applications to launch.
#     apps = {
#         '/demo/': Application(DirectoryHandler(filename=demo_path)),
#     }
#     # Can't pass num_procs > 1 in this configuration. If you need to run multiple
#     # processes, see e.g. flask_gunicorn_embed.py
#     # port = os.environ.get('PORT') or "5006"
#     server = Server(
#         apps,
#         prefix='bokeh_apps',
#         io_loop=IOLoop(),
#         port=0,
#         # use_xheaders=True,
#         allow_websocket_origin=[
#             "localhost:5000",
#             "0.0.0.0:5000",
#         ]
#     )
#
#     BOKEH_PORTS.append(server.port)
#     print(BOKEH_PORTS)
#     server.start()
#     print(server.address)
#     server.io_loop.start()
#     print(server.address)
#
#
# Thread(target=bk_worker).start()
