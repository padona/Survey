# Survey Application

Une application d'enquête en ligne construite avec Flask pour collecter et visualiser des données à travers l'Afrique.

## Installation

1. Clonez le repository :
   ```bash
   git clone https://github.com/padona/Survey.git
   cd Survey
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement :
   - Créez un fichier `.env`
   - Ajoutez vos variables d'environnement

5. Lancez l'application :
   ```bash
   python app.py
   ```

## Fonctionnalités
- Formulaire d'enquête en ligne
- Visualisation interactive de la carte
- Collecte et stockage des données
- Validation des formulaires en temps réel

## Technologies
- Flask
- SQLAlchemy
- Leaflet.js pour la cartographie
- Bootstrap pour l'UI
