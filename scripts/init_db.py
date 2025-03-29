from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Obtenir l'URI de MongoDB à partir des variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("L'URI de MongoDB n'est pas défini dans les variables d'environnement.")

# Connexion à MongoDB
client = MongoClient(MONGO_URI)

# Sélectionner la base de données
db = client['ordokine']

# Définition du schéma pour la collection 'patients'
patients_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nom", "prenom"],
        "properties": {
            "nom": {
                "bsonType": "string",
                "description": "Le nom est obligatoire et doit être une chaîne."
            },
            "prenom": {
                "bsonType": "string",
                "description": "Le prénom est obligatoire et doit être une chaîne."
            },
            "nir": {
                "bsonType": "string",
                "pattern": "^[1-2]\d{2}(0[1-9]|1[0-2])\d{2}\d{3}\d{3}\d{2}$",
                "description": "Le NIR doit respecter le format SAAMMDDXXXXXXXX (S: 1 ou 2, MM: 01-12)."
            },
            "date_naissance": {
                "bsonType": "date",
                "description": "La date de naissance doit être une date valide."
            }
        }
    }
}

# Définition du schéma pour la collection 'dispositifs'
dispositifs_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nom"],
        "properties": {
            "nom": {
                "bsonType": "string",
                "description": "Le nom du dispositif est obligatoire."
            }
        }
    }
}

# Définition du schéma pour la collection 'prescriptions'
prescriptions_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["praticien_id", "patient_id", "dispositifs", "date_prescription"],
        "properties": {
            "praticien_id": {
                "bsonType": "objectId",
                "description": "L'ID du praticien est obligatoire et doit être un ObjectId."
            },
            "patient_id": {
                "bsonType": "objectId",
                "description": "L'ID du patient est obligatoire et doit être un ObjectId."
            },
            "dispositifs": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["dispositif_id", "quantity"],
                    "properties": {
                        "dispositif_id": {
                            "bsonType": "objectId",
                            "description": "L'ID du dispositif est obligatoire et doit être un ObjectId."
                        },
                        "quantity": {
                            "bsonType": "int",
                            "description": "La quantité est obligatoire et doit être un entier."
                        }
                    }
                },
                "description": "Les dispositifs sont obligatoires et doivent contenir des ObjectIds et des quantités."
            },
            "date_prescription": {
                "bsonType": "date",
                "description": "La date de prescription est obligatoire et doit être une date valide."
            }
        }
    }
}

# Définition du schéma pour la collection 'praticiens'
praticiens_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nom", "prenom", "profession", "numero_professionnel", "adresse", "telephone", "portable", "email"],
        "properties": {
            "nom": {
                "bsonType": "string",
                "description": "Le nom est obligatoire et doit être une chaîne."
            },
            "prenom": {
                "bsonType": "string",
                "description": "Le prénom est obligatoire et doit être une chaîne."
            },
            "profession": {
                "bsonType": "string",
                "description": "La profession est obligatoire et doit être une chaîne."
            },
            "numero_professionnel": {
                "bsonType": "string",
                "description": "Le numéro professionnel est obligatoire et doit être une chaîne."
            },
            "adresse": {
                "bsonType": "object",
                "required": ["voie", "code_postal", "ville"],
                "properties": {
                    "voie": {
                        "bsonType": "string",
                        "description": "La voie est obligatoire et doit être une chaîne."
                    },
                    "code_postal": {
                        "bsonType": "string",
                        "description": "Le code postal est obligatoire et doit être une chaîne."
                    },
                    "ville": {
                        "bsonType": "string",
                        "description": "Le nom de la ville est obligatoire et doit être une chaîne."
                    }
                },
                "description": "L'adresse est obligatoire et doit être un objet contenant voie, code_postal et ville."
            },
            "telephone": {
                "bsonType": "string",
                "description": "Le téléphone est obligatoire et doit être une chaîne."
            },
            "portable": {
                "bsonType": "string",
                "description": "Le portable est obligatoire et doit être une chaîne."
            },
            "email": {
                "bsonType": "string",
                "description": "L'email est obligatoire et doit être une chaîne."
            }
        }
    }
}

# Création des collections avec validation

# Vérification et suppression de la collection 'patients' si elle existe
if "patients" in db.list_collection_names():
    try:
        db.drop_collection("patients")
        print("Collection 'patients' supprimée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection 'patients': {e}")

# Création de la collection 'patients' avec validation
try:
    db.create_collection("patients", validator=patients_schema)
    print("Collection 'patients' créée avec validation.")
except Exception as e:
    print(f"Erreur lors de la création de la collection 'patients': {e}")

# Vérification et suppression de la collection 'dispositifs' si elle existe
if "dispositifs" in db.list_collection_names():
    try:
        db.drop_collection("dispositifs")
        print("Collection 'dispositifs' supprimée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection 'dispositifs': {e}")

# Création de la collection 'dispositifs' avec validation
try:
    db.create_collection("dispositifs", validator=dispositifs_schema)
    print("Collection 'dispositifs' créée avec validation.")
except Exception as e:
    print(f"Erreur lors de la création de la collection 'dispositifs': {e}")

# Vérification et suppression de la collection 'prescriptions' si elle existe
if "prescriptions" in db.list_collection_names():
    try:
        db.drop_collection("prescriptions")
        print("Collection 'prescriptions' supprimée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection 'prescriptions': {e}")

# Création de la collection 'prescriptions' avec validation
try:
    db.create_collection("prescriptions", validator=prescriptions_schema)
    print("Collection 'prescriptions' créée avec validation.")
except Exception as e:
    print(f"Erreur lors de la création de la collection 'prescriptions': {e}")

# Vérification et suppression de la collection 'praticiens' si elle existe
if "praticiens" in db.list_collection_names():
    try:
        db.drop_collection("praticiens")
        print("Collection 'praticiens' supprimée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection 'praticiens': {e}")

# Création de la collection 'praticiens' avec validation
try:
    db.create_collection("praticiens", validator=praticiens_schema)
    print("Collection 'praticiens' créée avec validation.")
except Exception as e:
    print(f"Erreur lors de la création de la collection 'praticiens': {e}")