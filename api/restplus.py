import logging
from flask_restplus import Api
from jsonschema import FormatChecker
from flask import Blueprint
from datetime import datetime

logger = logging.getLogger()

blueprint = Blueprint("ocr", __name__, url_prefix="/api/ocr")
format_checker = FormatChecker()


@format_checker.checks("date", ValueError)
def my_date_check(value):
    if value is not None:
        datetime.strptime(value, "%Y-%m-%d")
    return True


restapi = Api(blueprint, version='1.0', title='ocr api prediction',
              description='ocr api of a Flask RestPlus powered API',
              format_checker=format_checker)


@restapi.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    logger.error(message, exc_info=True)

    return {"message": str(e) or message, "type": type(e).__name__}, getattr(e, "code", 500)
