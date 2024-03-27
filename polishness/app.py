from typing import TypeVar
from os import makedirs

from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import render_template

from polishness.utils import STATIC_DIR, PROJECT_DIR
from polishness.api.monuments.monuments_api import monuments_bp

FlaskApp = TypeVar("FlaskApp", bound=Flask)


def create_app() -> FlaskApp:
    """Creates Flask app object (factory function)

    Patterns:
    - Application factory.
    - Flask extensions patterns (future)
       ~ making an object available in global context.
    """
    inst_path = PROJECT_DIR + 'instance/'
    flask_app = Flask(__name__, static_folder=STATIC_DIR, template_folder=STATIC_DIR, instance_path=PROJECT_DIR)

    # ensure the instance folder exists
    try:
        makedirs(flask_app.instance_path)
    except OSError:
        pass

    _register_endpoints(flask_app)

    return flask_app


def _register_endpoints(application: FlaskApp):
    """Registers endpoints in Flask app object."""

    _bp_proxy = Blueprint('bp_proxy', __name__, template_folder="/home/danielp/temp/polishness/polishness/gui/templates")
    _bp_proxy.register_blueprint(monuments_bp)

    @application.route("/")
    def index():
        return render_template('index.html')

    @application.route("/hello")
    def hello():
        return jsonify("Hello, World (json)!")

    application.register_blueprint(_bp_proxy)


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
