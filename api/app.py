import sqlite3
import os
from flask import Flask, jsonify, request
from flask_cors import (
    CORS,
)  # Nécessaire pour permettre les requêtes depuis le frontend (CORS)

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Obtenez le chemin absolu du répertoire où se trouve ce fichier (app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "base_de_donnees_204_V5_test.db")
# DATABASE = 'C:\\Users\\but-info\\Downloads\\base_de_donnees_204_V5_test.db'
# DATABASE = r"base_de_donnees_204_V5_test.db"  # Chemin relatif pour le fichier de base de données


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn


@app.route("/api/departements", methods=["GET"])
def get_departements():
    conn = get_db_connection()
    # Ordonner par nom_departement pour une meilleure UX
    departements_db = conn.execute(
        "SELECT code_departement, nom_departement FROM Département ORDER BY nom_departement"
    ).fetchall()
    conn.close()
    departements = [
        {"code": d["code_departement"], "nom": d["nom_departement"]}
        for d in departements_db
    ]
    return jsonify(departements)


@app.route("/api/parametres", methods=["GET"])
def get_parametres():
    conn = get_db_connection()
    # Récupérer les paramètres uniques des analyses (ou de votre table de paramètres si elle existe)
    # Si votre table Analyse contient des libelle_parametre uniques, utilisez-les.
    # Sinon, vous devrez créer une table dédiée aux paramètres si vous voulez une liste complète.
    # Pour cet exemple, je vais simuler une récupération des paramètres les plus pertinents de votre schéma.
    # L'API Hub'Eau utilise des "code_parametre", donc il est bon de les récupérer si possible.
    parametres_db = conn.execute(
        """
        SELECT DISTINCT code_parametre, libelle_parametre, libelle_unite
        FROM Analyse
        WHERE code_parametre IS NOT NULL AND libelle_parametre IS NOT NULL
        ORDER BY libelle_parametre
    """
    ).fetchall()
    conn.close()
    parametres = [
        {
            "code": p["code_parametre"],
            "nom": p["libelle_parametre"],
            "unite": p[
                "libelle_unite"
            ],  # Si disponible, sinon gérer le cas où c'est null
        }
        for p in parametres_db
    ]
    return jsonify(parametres)


# Exemple d'un endpoint qui pourrait potentiellement appeler Hub'Eau ou votre DB
# Pour cet exemple, nous allons continuer à appeler Hub'Eau depuis le frontend,
# car il est plus simple de le faire directement pour des données "live" de qualité de l'eau.
# Si vous voulez cacher la logique Hub'Eau, ce serait l'endroit pour le faire.

if __name__ == "__main__":
    app.run(debug=True)
