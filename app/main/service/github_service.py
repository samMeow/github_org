import requests


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
