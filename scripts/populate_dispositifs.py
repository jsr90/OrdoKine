from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis un fichier .env
load_dotenv(dotenv_path='config/.env')

# Obtenir l'URI de MongoDB à partir des variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")

# Connexion à MongoDB
client = MongoClient(MONGO_URI)

# Sélectionner la base de données et la collection
db = client['ordokine']
dispositifs = db['dispositifs']

# Liste des dispositifs à insérer
dispositifs_data = [
    {'nom': 'Potences et soulève-malades'},
    {'nom': 'Matelas anti-escarres'},
    {'nom': 'Coussin anti-escarres'},
    {'nom': 'Barrières de lits et cerceaux'},
    {'nom': 'Aide à la déambulation'},
    {'nom': 'Fauteuil roulant manuel'},
    {'nom': 'Attelles souples orthopédiques'},
    {'nom': 'Ceintures lombaires de soutien'},
    {'nom': 'Bandes de contention élastique'},
    {'nom': 'Sonde périnale'},
    {'nom': 'Collecteurs d’urines'},
    {'nom': 'Attelles souples de posture'},
    {'nom': 'Embouts de cannes'},
    {'nom': 'Talonnettes'},
    {'nom': 'Débitmètre de pointe'},
    {'nom': 'Pansements pour balnéothérapie'}
]

# Insérer les dispositifs si la collection est vide
if dispositifs.count_documents({}) == 0:
    result = dispositifs.insert_many(dispositifs_data)
    print(f"✅ {len(result.inserted_ids)} dispositifs insérés avec succès !")
else:
    print("⚠️ La collection 'dispositifs' contient déjà des données. Aucune insertion effectuée.")
