# WikiEau – Visualisation de la Qualité de l’Eau Potable en France

WikiEau est une application web interactive permettant de visualiser, explorer et analyser les données publiques sur la qualité de l’eau potable en France. Les données sont issues de l’API officielle [Hub’Eau](https://hubeau.eaufrance.fr/page/api-qualite-eau-potable) et enrichies par un stockage local pour de meilleures performances.

## Fonctionnalités principales

- **Carte interactive** : Visualisez les résultats d’analyses par département, commune, site de prélèvement, et accédez à des détails récents sur la qualité de l’eau.
- **Statistiques dynamiques** : Générez des graphiques (barres, lignes, camembert) sur les concentrations de paramètres chimiques ou microbiologiques, filtrés par département et période.
- **Page À propos** : Découvrez la démarche, les choix techniques et les sources de données utilisées.
- **Navigation fluide** : Interface moderne, responsive, avec menu latéral et transitions animées.

## Structure du projet

```
.
├── api/
│   ├── app.py                # Backend Flask (API REST)
│   ├── crea_carte.py         # Génération de la carte interactive
│   └── base_de_donnees_204_V5_test.db # Base SQLite locale
├── templates/
│   ├── index.html            # Page d’accueil
│   ├── carte.html            # Carte interactive
│   ├── stats.html            # Statistiques et graphiques
│   ├── apropos.html          # Page À propos
│   ├── style.css             # Feuilles de style
│   └── ...                   # Images et ressources
├── Qeau_data_cleaned.json    # Données locales nettoyées
├── maj_V2.py                # Script d’importation/mise à jour des données
├── README.md                # Ce fichier
└── ...
```

## Installation et lancement

### Prérequis

- Python 3.8+
- [Flask](https://flask.palletsprojects.com/)
- [requests](https://pypi.org/project/requests/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)

### Installation

1. **Clonez le dépôt**  
   ```sh
   git clone https://github.com/Ryn-GH/S204_S201.git
   cd S204_S201
   ```

2. **Installez les dépendances**  
   ```sh
   pip install flask requests
   ```

3. **(Optionnel) Mettez à jour la base de données**  
   Lancez le script d’importation pour récupérer les dernières données :
   ```sh
   python maj_V2.py
   ```

4. **Démarrez le serveur Flask**  
   ```sh
   cd api
   python app.py
   ```

5. **Accédez à l’application**  
   Ouvrez votre navigateur à l’adresse [http://localhost:5000](http://localhost:5000)

## Utilisation

- **Accueil** : Présentation du projet et guide d’utilisation.
- **Carte** : Cliquez sur un département pour afficher les résultats d’analyses détaillés.
- **Statistiques** : Sélectionnez un département et un paramètre pour générer des graphiques dynamiques.
- **À propos** : Informations sur la démarche, l’architecture et les sources.

## Architecture technique

- **Backend** : Python, Flask, SQLite
- **Frontend** : HTML5, CSS (Tailwind), JavaScript (Chart.js)
- **Données** : API Hub’Eau + stockage local JSON/SQLite

## Sources et API

- [API Hub’Eau – Qualité de l’eau potable](https://hubeau.eaufrance.fr/page/api-qualite-eau-potable)
- [EauFrance](https://www.eaufrance.fr/)

## Auteurs

Projet réalisé dans le cadre des SAE 2.01 et 2.04 du BUT Informatique – IUT Créteil-Vitry.

---

**Licence** : Projet pédagogique, libre de réutilisation.
