from .base_api import BaseAPI
import requests

class Praticien(BaseAPI):
    endpoint = f"{BaseAPI.api_base_url}/praticiens"

    def __init__(self, nom, prenom, profession, numero_professionnel, adresse, telephone, portable, email, id=None):
        data = {
            "nom": nom,
            "prenom": prenom,
            "profession": profession,
            "numero_professionnel": numero_professionnel,
            "adresse": {
                "voie": adresse.get('voie'),
                "code_postal": adresse.get('code_postal'),
                "ville": adresse.get('ville')
            },
            "telephone": telephone,
            "portable": portable,
            "email": email
        }
        data = {k: v for k, v in data.items() if v is not None and v != ''}
        if "adresse" in data:
            data["adresse"] = {k: v for k, v in data["adresse"].items() if v is not None}
        super().__init__(data, id)
