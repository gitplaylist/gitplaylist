from flask import Flask
from flask_restful import Api, Resource
from flask.ext.assets import Environment, Bundle
from webassets.filter import register_filter
from webassets_babel import BabelFilter
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
api = Api()
assets = Environment()

scss = Bundle('scss/style.scss',filters='scss', output='gen/app.css')

register_filter(BabelFilter)
jsx = Bundle('jsx/app.jsx', filters='babel', output='gen/app.js')

assets.register('scss', scss)
assets.register('jsx', jsx)

def create_app():
    app = Flask(__name__)
    app.config.update(Config.__dict__)

    # Set up extensions
    db.init_app(app)
    app.db = db

    api.init_app(app)
    assets.init_app(app)

    # Install views
    from views.index import bp as index_bp
    app.register_blueprint(index_bp)

    # Install models
    from models.dummy import Dummy

    with app.app_context():
        db.create_all()

    return app
