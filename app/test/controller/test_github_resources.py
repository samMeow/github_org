from unittest import mock

from app.test.base import BaseTestCase
from app.main.model import GithubOrg
from app.main.instances import db

class TestGitHubResources(BaseTestCase):
    def test_get_nothing_if_nothing_in_db(self):
        with self.client:
            res = self.client.get('/github_orgs/')
            assert res.status_code == 200
            data = res.json
            assert data['data'] == []
            
    def test_get_anything_with_filter(self):
        r1 = GithubOrg(github_id=1, name="abc")
        r2 = GithubOrg(github_id=2, name="xyz")
        db.session.add(r1, r2)
        db.session.commit()
        with self.client:
            res = self.client.get('/github_orgs/?input=a')
            assert res.status_code == 200
            data = res.json
            assert len(data['data']) == 1
            assert 'abc' in [ x['name'] for x in data['data'] ]

class TestGitHubSearchResource(BaseTestCase):
    @mock.patch('app.main.service.GithubService.search_orgs')
    def test_should_sort_result_by_name(self, search_orgs):
        search_orgs.return_value = {
            'items': [
                { 'id': 1, 'login': 'xyz' },
                { 'id': 2, 'login': 'abc' },
            ]
        }
        with self.client:
            res = self.client.get('/github_orgs/search/?input=a')
            assert res.status_code == 200
            data = res.json
            assert len(data['data']) == 2
            assert data['data'][0]['login'] == 'abc'
            assert data['data'][1]['login'] == 'xyz'