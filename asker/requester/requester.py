from typing import Optional, Dict, Any, Tuple, List
import requests


class Requester:

    @staticmethod
    def __request(url: str,
                  headers: Optional[dict] = None,
                  data: Optional[dict] = None) -> Dict[str, Any]:
        """
        Send a request to the server

        :param url: URL to send the request
        :param headers: Headers to send
        :param data: Data to send
        :return: Response from the server
        """

        response = requests.request("GET", url, headers=headers, data=data)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    @staticmethod
    def ask_seat(url: str, token: str) -> Dict[str, Any]:
        """
        Ask the SEAT API for data

        :param url: URL to send the request
        :param token: API token
        :return: Response from the server
        """

        headers = {
            'X-Token': token,
            'accept': 'application/json',
        }
        return Requester.__request(url, headers=headers)


class Pagination:
    _next: Optional[str]
    _previous: Optional[str]
    _start_url: str
    _endpoint: str
    _token: str
    _items: List[Any]

    def __init__(self, base_url: str, endpoint: str, token: str, *args, **kwargs):
        """
        Initialize the pagination object

        :param base_url: Base URL for the API
        :param endpoint: Endpoint for the API
        :param token: API token
        :param args: Additional positional arguments
        :param kwargs: Additional query parameters
        """
        self._base_url = base_url
        self._endpoint = endpoint
        self._token = token
        self._next = None
        self._previous = None
        self._items = []

        self._start_url = f"{self._base_url}/{self._endpoint}"
        if args:
            for arg in args:
                self._start_url += f"/{arg}"

        if kwargs:
            self._start_url += "?"
            for key, value in kwargs.items():
                self._start_url += f"{key}={value}&"
            self._start_url = self._start_url[:-1]

    async def next(self) -> Tuple[bool, List[Any], Optional[str]]:
        """
        Fetch the next set of items.
        """
        if not self._next:
            return False, [], "No next page"
        return await self._fetch_and_process(self._next)

    async def previous(self) -> Tuple[bool, List[Any], Optional[str]]:
        """
        Fetch the previous set of items.
        """
        if not self._previous:
            return False, [], "No previous page"
        return await self._fetch_and_process(self._previous)

