from typing import Optional, Dict, Any
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
