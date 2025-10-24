import requests
from http_client.http_client_interface import HTTPClientInterface

class RequestsHTTPClient(HTTPClientInterface):
    def __init__(self):
        super().__init__()

    def get(self, endpoint):
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


    