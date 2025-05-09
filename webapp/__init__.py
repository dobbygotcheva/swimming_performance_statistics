from flask import Flask
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .routes import main
    app.register_blueprint(main)

    return app

# Import modules to make them available
from . import data_utils
from . import convert_utils 