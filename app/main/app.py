from flask import Flask
from flask_bcrypt import Bcrypt
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask_migrate import Migrate


from .config import config_by_name
from .instances import db, ma, scheduler
from .model import Schemas

flask_bcrypt = Bcrypt()
app = Flask(__name__)
migrate = Migrate(app, db)


def init_docs(app):
    plugins = [FlaskPlugin(), MarshmallowPlugin()]
    spec = APISpec("My api docs", '1.0', "2.0", plugins=plugins)
    template = spec.to_flasgger(app, definitions=Schemas)
    Swagger(app, template=template, parse=True)


def with_context(task):
    def run():
        with app.app_context():
            return task()
    return run


def create_app(config_name):
    """
    main app
    """
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    ma.init_app(app)
    flask_bcrypt.init_app(app)
    init_docs(app)
    scheduler.init_app(app)
    scheduler.start()

    return app
