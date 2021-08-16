from flask import Flask
import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '')))

from api.endpoints.ocr import ns
from api.restplus import blueprint as bp, restapi as api


app = Flask(__name__, static_folder="output", static_url_path="/output")


def initialize_app():
    configure_app(app)
    initialize_app_blueprint(app)


def configure_app(flask_app):
    flask_app.config[
        "SWAGGER_UI_DOC_EXPANSION"
    ] = 'list'
    flask_app.config["RESTPLUS_VALIDATE"] = True
    flask_app.config["RESTPLUS_MASK_SWAGGER"] = False
    flask_app.config["ERROR_404_HELP"] = False
    # workground fix errorhanlder is not work in current restplus version
    flask_app.config["PROPAGATE_EXCEPTIONS"] = False

    flask_app.config["LOG_REQUEST_ID_GENERATE_IF_NOT_FOUND"] = False


def initialize_app_blueprint(flask_app):
    api.add_namespace(ns)
    flask_app.register_blueprint(bp)


@app.route("/health")
def health():
    health_info = {"health": True}
    return health_info, 200


initialize_app()


if __name__ == "__main__":
    app.run(debug=True, port=8888, host='127.0.0.1')
