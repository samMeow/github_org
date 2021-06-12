from flask import request
from flask_restful import Resource
from flasgger import swag_from

from app.main.model import GithubOrg, GithubOrgSchema
from app.main.service import GithubService
from ..instances import logger

class GithubOrgResources(Resource):
    @swag_from('../spec/get_github_org.yml')
    def get(self):
        param = request.args
        input = param.get('input', '')
        page_size = param.get('page_size', 10)

        query = GithubOrg.query
        if input:
            query = query.filter(
                GithubOrg.name.like(f'{input}%'),
            )
        data = query.order_by(GithubOrg.name).limit(page_size).all()
        return {
            'data': GithubOrgSchema(many=True).dump(data)
        }, 200

class GithubOrgSearchResource(Resource):
    @swag_from('../spec/get_github_org_search.yml')
    def get(self):
        param = request.args
        input = param.get('input', '')
        result = GithubService.search_orgs(input=input)
        data = result['items']
        data.sort(key=lambda x: x['login'])
        return {
            'data': data,
        }, 200
        