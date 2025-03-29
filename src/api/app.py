from flask import Flask, request, jsonify
from services.mongo_client import MongoDBClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")

db_client = MongoDBClient(uri=mongo_uri, db_name="ordokine")

# Liste des collections autorisées (sécurité)
collections = db_client.collections.to_list()
collection_names = [collection['name'] for collection in collections]

# Lister tous les documents (GET /<collection>)
@app.route('/<collection>', methods=['GET'])
def get_all(collection):
    if collection not in collection_names:
        return jsonify({"error": "Collection non autorisée"}), 403
    return jsonify(db_client.list_all(collection))

# Obtenir un document par ID (GET /<collection>/<id>)
@app.route('/<collection>/<id>', methods=['GET'])
def get_by_id(collection, id):
    if collection not in collection_names:
        return jsonify({"error": "Collection non autorisée"}), 403
    data = db_client.read(collection, {"_id": ObjectId(id)})
    return jsonify(data or {"error": "Document non trouvé"}), 404 if not data else 200

# Créer un document (POST /<collection>)
@app.route('/<collection>', methods=['POST'])
def create_document(collection):
    if collection not in collection_names:
        return jsonify({"error": "Collection non autorisée"}), 403
    data = request.json
    result = db_client.create(collection, data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201

# Mettre à jour un document (PUT /<collection>/<id>)
@app.route('/<collection>/<id>', methods=['PUT'])
def update_document(collection, id):
    if collection not in collection_names:
        return jsonify({"error": "Collection non autorisée"}), 403
    data = request.json
    result = db_client.update(collection, {"_id": ObjectId(id)}, data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)

# Supprimer un document (DELETE /<collection>/<id>)
@app.route('/<collection>/<id>', methods=['DELETE'])
def delete_document(collection, id):
    if collection not in collection_names:
        return jsonify({"error": "Collection non autorisée"}), 403
    result = db_client.delete(collection, {"_id": ObjectId(id)})
    if 'error' in result:
        return jsonify(result), 400 
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
