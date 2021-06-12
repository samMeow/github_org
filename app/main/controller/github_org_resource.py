from flask import request
from flask_restful import Resource
from flasgger import swag_from

class GithubOrgResources(Resource):
    @swag_from('../spec/get_github_org.yml')
    def get(self):
        param = request.args
        input = param.get('input', '')
        return {
            'data': input
        }, 200