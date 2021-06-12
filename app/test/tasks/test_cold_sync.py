from unittest import mock

from app.main.tasks.cold_sync import cold_sync
from app.main.model import GithubOrg

from app.test.base import BaseTestCase

class TestColdSync(BaseTestCase):
    @mock.patch('app.main.service.GithubService.list_orgs')
    def test_should_do_nothing_if_nothing_return(self, list_orgs):
        list_orgs.return_value = []
        cold_sync()
        result = GithubOrg.query.first()
        assert result == None

    @mock.patch('app.main.service.GithubService.list_orgs')
    def test_should_insert_data_from_github(self, list_orgs):
        list_orgs.side_effect = [[{ 'id': 1, 'login': 'whatever' }], []]
        cold_sync()
        result = GithubOrg.query.all()
        assert 'whatever' in [ x.name for x in result ]