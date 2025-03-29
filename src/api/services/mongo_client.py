from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from datetime import datetime

def _process_data_fields(data):
    for field in data:
        if isinstance(data[field], dict):
            data[field] = _process_data_fields(data[field])
        elif isinstance(data[field], list):
            for elem in data[field]:
                elem = _process_data_fields(elem)
        elif isinstance(data[field], str):
            if 'id' in field.lower() and isinstance(data[field], str):
                try:
                    data[field] = ObjectId(data[field])
                except Exception as e:
                    raise ValueError(f"ID invalide dans le champ '{field}' : {data[field]}")
            elif 'date' in field.lower():
                try:
                    data[field] = datetime.strptime(data[field], '%Y-%m-%d')
                except ValueError as e:
                    raise ValueError(f"Format de date invalide dans le champ '{field}' : {data[field]}")
    return data

def _reverse_process_data_fields(data):
    for field in data:
        if isinstance(data[field], dict):
            data[field] = _reverse_process_data_fields(data[field])
        elif isinstance(data[field], list):
            for i, elem in enumerate(data[field]):
                data[field][i] = _reverse_process_data_fields(elem)
        elif isinstance(data[field], ObjectId):
            data[field] = str(data[field])
        elif isinstance(data[field], datetime):
            data[field] = data[field].strftime('%Y-%m-%d')
    return data

class MongoDBClient:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collections = self.db.list_collections()

    def create(self, collection, data):
        try:
            data = _process_data_fields(data)
            result = self.db[collection].insert_one(data)
            return {"_id": str(result.inserted_id)}
        except errors.PyMongoError as e:
            return self._handle_error(e)

    def read(self, collection, query):
        try:
            result = self.db[collection].find_one(query)
            result = _reverse_process_data_fields(result)
            return result
        except errors.PyMongoError as e:
            return self._handle_error(e)

    def list_all(self, collection, filter_query={}):
        try:
            results = list(self.db[collection].find(filter_query))
            for doc in results:
                doc["_id"] = str(doc["_id"])
                for field in doc:
                    if 'date' in field.lower() and isinstance(doc[field], datetime):
                        doc[field] = doc[field].strftime('%Y-%m-%d')
            return results
        except errors.PyMongoError as e:
            return self._handle_error(e)

    def update(self, collection, query, new_data):
        try:
            new_data = _process_data_fields(new_data)
            result = self.db[collection].update_one(query, {"$set": new_data})
            if result.matched_count == 0:
                return {"error": "Document non trouvé"}
            return {"modified_count": result.modified_count}
        except errors.PyMongoError as e:
            return self._handle_error(e)

    def delete(self, collection, query):
        try:
            result = self.db[collection].delete_one(query)
            if result.deleted_count == 0:
                return {"error": "Document non trouvé"}
            return {"deleted_count": result.deleted_count}
        except errors.PyMongoError as e:
            return self._handle_error(e)

    def _handle_error(self, error):
            if isinstance(error, errors.ConfigurationError):
                raise ConnectionError("Erreur de connexion avec la base de données.")
            elif isinstance(error, errors.DuplicateKeyError):
                raise ValueError("Erreur : Duplicat détecté.")
            elif isinstance(error, errors.WriteError):
                print("Erreur d'écriture :", error)
                raise IOError(f"Erreur d'écriture : {str(error)}")
            else:
                raise Exception(f"Erreur inattendue : {str(error)}")
