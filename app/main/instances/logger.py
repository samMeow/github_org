import logging
from flask.logging import default_handler

gunicorn_logger = logging.getLogger('gunicorn.error')

logger = logging.Logger(__name__)
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)