from werkzeug.exceptions import HTTPException

from ..instances.logger import logger

def global_handler(err):
    """
    handle all exception
    """
    logger.error(str(err), exc_info=True)
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    return {'message': str(err)}, code

def init_error_handler(app):
    """
    init app with handler
    """
    app.register_error_handler(Exception, global_handler)
    return app
