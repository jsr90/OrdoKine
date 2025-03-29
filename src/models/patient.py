import requests
from .base_api import BaseAPI

class Patient(BaseAPI):
    endpoint = f"{BaseAPI.api_base_url}/patients"

    def __init__(self, nom, prenom, nir=None, date_naissance=None, id=None):
        data = {k: v for k, v in {
            "nom": nom,
            "prenom": prenom,
            "nir": nir,
            "date_naissance": date_naissance
        }.items() if v is not None and v != ''}
        super().__init__(data, id)
