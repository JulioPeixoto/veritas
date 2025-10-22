import requests


class SerpAPIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://serpapi.com/search",
    ):
        self.api_key = api_key
        self.base_url = base_url


    def search(self, *args, engine: str = None, **kwargs):
        params = {
            "api_key": self.api_key,
            "engine": engine,
        }
        params.update(kwargs)

        if args:
            first = args[0]
            if isinstance(first, dict):
                params.update(first)

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
