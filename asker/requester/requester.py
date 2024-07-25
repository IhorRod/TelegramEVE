import logging
from typing import Optional, Dict, Any, Tuple, List
import requests
from abc import ABC, abstractmethod


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


class Pagination(ABC):
    _base_url: str
    _token: str

    _start_url: str
    _next: Optional[str]
    _previous: Optional[str]
    _items: List[Any]
    _total: int

    def __init__(self, base_url: str, token: str, *args, **kwargs):
        """
        Initialize the pagination object

        :param base_url: Base URL for the API
        :param token:  token
        :param args: Additional positional arguments
        :param kwargs: Additional query parameters
        """
        self._base_url = base_url
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
                if value is not None:
                    self._start_url += f"{key}={value}&"
            self._start_url = self._start_url[:-1]

        request = Requester.ask_seat(self._start_url, self._token)

        self._next = request.get("links", {}).get("next", None)
        self._previous = request.get("links", {}).get("prev", None)
        self._items = [self._transform(item) for item in request.get("data", [])]
        self._total = request.get("meta", {}).get("total", 0)

    def __next__(self):
        """
        Get the next page of data

        :return: None
        """
        if self._next:
            request = Requester.ask_seat(self._next, self._token)
            self._next = request.get("links", {}).get("next", None)
            self._previous = request.get("links", {}).get("prev", None)
            temp_items = [self._transform(item) for item in request.get("data", [])]

            for item in temp_items:
                if not self.__contains(item):
                    self._items.append(item)

    def __previous__(self):
        """
        Get the previous page of data

        :return: None
        """
        if self._previous:
            request = Requester.ask_seat(self._previous, self._token)
            self._next = request.get("links", {}).get("next", None)
            self._previous = request.get("links", {}).get("prev", None)
            temp_items = [self._transform(item) for item in request.get("data", [])]

            for item in temp_items:
                if not self.__contains(item):
                    self._items.append(item)

    @abstractmethod
    def _equal(self, one: Any, other: Any) -> bool:
        """
        Compare two items. This method should be overridden by the child class

        :param one: First item
        :param other: Second item
        :return: True if the items are equal, False otherwise
        """
        ...

    @abstractmethod
    def _transform(self, item: Dict) -> Any:
        """
        Transform the item from raw to smth of BaseObject. This method should be overridden by the child class

        :param item: Item to transform
        :return: Transformed item
        """
        ...

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        """
        Get the endpoint for the API

        :return: Endpoint
        """
        ...

    @property
    @abstractmethod
    def _warn_if_not_total(self) -> str:
        """
        Warn if the total number of items in meta is different from the actual number of items
        Message should be returned
        Should be overridden by the child class
        """
        ...

    def __contains(self, item: Any) -> bool:
        """
        Check if the item is already in the list

        :param item: Item to check
        :return: True if the item is already in the list, False otherwise
        """
        for i in self._items:
            if self._equal(i, item):
                return True
        return False

    def collect(self) -> List[Any]:
        """
        Collect all the data from the API

        :return: None
        """
        while self._next:
            self.__next__()

        if len(self._items) != self._total:
            logging.warning(self._warn_if_not_total)

        return self._items
