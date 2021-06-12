import requests
from ..instances import logger

class GithubService:
    BASE_URL = 'https://api.github.com'

    @classmethod
    def list_orgs(cls, since: int = 0, page_size: int = 100) -> list:
        res = requests.get(
            f'{cls.BASE_URL}/organizations',
            params={ 'since': since, 'per_page': page_size },
            headers={'Accept': 'application/json'}
        )
        res.raise_for_status()
        return res.json()

    @classmethod
    def search_orgs(cls, input: str) -> list:
        extra = f'+{input}' if input else ''
        res = requests.get(
            # request will encode url
            f'{cls.BASE_URL}/search/users?q=type:org{extra}&per_page=10',
            headers={'Accept': 'application/json'}
        )
        res.raise_for_status()
        return res.json()