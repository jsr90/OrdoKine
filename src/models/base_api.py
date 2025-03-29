import requests

class BaseAPIError(Exception):
    """Exception de base pour les erreurs de l'API."""
    pass

class NotFoundError(BaseAPIError):
    """Exception pour les erreurs 404."""
    pass

class AccessDeniedError(BaseAPIError):
    """Exception pour les erreurs 403."""
    pass

class GeneralAPIError(BaseAPIError):
    """Exception pour d'autres erreurs de l'API."""
    pass


class BaseAPI:
    api_base_url = "http://localhost:5000"

    def __init__(self, data=None, id=None):
        self.data = data
        self.id = id

    def create(self):
        response = requests.post(self.endpoint, json=self.data)
        if response.status_code == 201:
            self.id = response.json()['_id']
        return self._handle_response(response)

    def update(self, data):
        if not self.id:
            return {"error": "No ID provided in the data"}
        response = requests.put(f"{self.endpoint}/{self.id}", json=data)
        if response.status_code == 200:
            self.data.update(data)
        return self._handle_response(response)

    def delete(self):
        if not self.id:
            return {"error": "No ID provided"}
        response = requests.delete(f"{self.endpoint}/{self.id}")
        if response.status_code == 200:
            self.id = None
            self.data = None
        return self._handle_response(response)
    
    def compare(self, other):
        if not isinstance(other, BaseAPI):
            return False
        if self.id != other.id:
            return False
        if self.data != other.data:
            return False

        return True

    @classmethod
    def get_by_id(cls, item_id):
        response = requests.get(f"{cls.endpoint}/{item_id}")
        data = cls._handle_response(response)
        if "error" not in data:
            item_id = data.pop("_id")
            return cls(**data, id=item_id)
        return data

    @classmethod
    def list_all(cls):
        response = requests.get(cls.endpoint)
        return cls._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 404:
            raise NotFoundError("Document not found")
        elif response.status_code == 403:
            raise AccessDeniedError("Access denied")
        else:
            raise GeneralAPIError(f"Error {response.status_code}: {response.text}")
