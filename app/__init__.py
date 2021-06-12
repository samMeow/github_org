import asyncio

from flask_restful import Api
from flask import Blueprint, request

from .main.util.error_handler import init_error_handler
from .main.config import Config
from .main.controller import GithubOrgResources

blueprint = Blueprint('api', __name__)


api = Api(blueprint)
init_error_handler(blueprint)
api.add_resource(GithubOrgResources, '/github_orgs')

@blueprint.after_request
def after_request(response):
    """
    add cors header
    """
    allowed = Config.ALLOWED_ORIGIN.split(',')
    origin = request.environ.get('HTTP_ORIGIN', None)
    if origin and origin in allowed:
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    return response
