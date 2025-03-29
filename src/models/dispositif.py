import requests
from .base_api import BaseAPI

class Dispositif(BaseAPI):
    endpoint = f"{BaseAPI.api_base_url}/dispositifs"

    def __init__(self, nom, id=None):
        data = {
            "nom": nom
        }
        super().__init__(data, id)
