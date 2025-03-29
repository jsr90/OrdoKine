# OrdoKiné 📝

## Description technique

OrdoKiné est une application conçue pour gérer les ordonnances d'un kinésithérapeute. Elle permet la création, la gestion du stock et le suivi des ordonnances de manière efficace et centralisée.

### Stack technique :
- **Backend** : Développé en Python avec le framework **APIFlask**, permettant de créer des API RESTful robustes et performantes.
- **Base de données** : Utilisation de **MongoDB** pour stocker les données de manière flexible et évolutive.
- **Interface utilisateur** : Intégration de **Gradio** pour fournir une interface utilisateur interactive et intuitive.
- **Génération de documents** : Utilisation de la bibliothèque **FPDF** pour la mise en page et la génération de fichiers PDF professionnels.

### Méthodologie :
- **CRUD** : Implémentation des opérations Create, Read, Update et Delete pour une gestion complète des données.
- **Programmation orientée objet (POO)** : Structuration du code en classes et objets pour une meilleure modularité et maintenabilité.
- **Réutilisation de code** : Adoption de bonnes pratiques pour éviter la duplication et maximiser l'efficacité.
- **Gestion des erreurs** : Mise en place de mécanismes robustes pour capturer et traiter les erreurs, garantissant une expérience utilisateur fiable.

### Structure du projet :
```
OrdoKine/
├── scripts/
│   ├── init_db.py
│   ├── populate_dispositifs.py
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── mongo_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_api.py
│   │   ├── dispositif.py
│   │   ├── patient.py
│   │   ├── praticien.py
│   │   └── prescription.py
│   ├── utils/
│   │   ├── generate_pdf.py
│   │   └── utils.py
│   ├── __init__.py
│   └── run.py
├── .env
├── requirements.txt
└── REAMDE.md
```

## Guide d'utilisation

1. **Configurer la variable d'environnement** :  
   Ajouter la variable `MONGO_URI=` dans le fichier `.env` avec l'URI de connexion à votre base de données MongoDB.

2. **Installer les dépendances** :  
   Exécuter la commande suivante pour installer les bibliothèques nécessaires :  
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialiser la base de données** :  
   Lancer le script `init_db.py` pour créer et initialiser les collections dans la base de données :  
   ```bash
   python scripts/init_db.py
   ```

4. **Démarrer l'API** :  
   Exécuter le fichier `app.py` pour démarrer l'API Flask :  
   ```bash
   python src/api/app.py
   ```

5. **Lancer l'interface utilisateur** :  
   Utiliser la commande suivante pour démarrer l'interface Gradio :  
   ```bash
   python src/run.py
   ```

## Améliorations futures

- Implémenter les opérations CRUD dans l'interface utilisateur pour toutes les classes.
- Ajouter une option permettant de récupérer les prescriptions par patient.
- Intégrer des fonctionnalités pour afficher des données statistiques, comme le nombre de prescriptions par praticien ou les dispositifs les plus utilisés.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
