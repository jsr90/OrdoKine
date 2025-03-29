import requests
from .base_api import BaseAPI

class Prescription(BaseAPI):
    endpoint = f"{BaseAPI.api_base_url}/prescriptions"

    def __init__(self, praticien_id, patient_id, dispositifs, date_prescription, id=None):
        data = {
            "praticien_id": praticien_id,
            "patient_id": patient_id,
            "dispositifs": dispositifs,
            "date_prescription": date_prescription,
        }
        data = {k: v for k, v in data.items() if v is not None}
        super().__init__(data, id)
