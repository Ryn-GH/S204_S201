import json
import sqlite3


#La colonne sqlite_sequence est utilisée pour gérer le AUTOINCRMENT des clés primaires.
# Fichiers dont on a besoin
json_file = "C:/Users/but-info/OneDrive - UPEC/Documents/BUT-INFO/BUT1/S2/sae_204/Qeau_data_cleaned.json"
db_file = "C:/Users/but-info/OneDrive - UPEC/Documents/BUT-INFO/BUT1/S2/sae_204/base_de_donnees_204_V4.db"

# Connexion SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Vérifier qu'on récupère bien les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables trouvées dans la base :", [t[0] for t in tables])


# Charger JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

# Traiter les entrées
for item in data:
    code_departement = item.get('code_departement')
    nom_departement = item.get('nom_departement')
    id_prelevement = item.get('code_prelevement')
    date_prelevement = item.get('date_prelevement')
    id_analyse = item.get('reference_analyse')
    code_parametre = item.get('code_parametre')
    reference_qualite = item.get('reference_qualite_parametre')
    libelle_parametre = item.get('libelle_parametre')
    code_parametre_se = item.get('code_parametre_se')
    code_parametre_acs = item.get('code_parametre_cas')
    libelle_unite = item.get('libelle_unite')
    limite_qualite_parametre = item.get('limite_qualite_parametre')
    reference_qaulite_parametre = item.get('reference_qualite_parametre')

    # Insérer ou ignorer Département
    cursor.execute("""
        INSERT OR IGNORE INTO Département (code_departement, nom_departement)
        VALUES (?, ?)
    """, (code_departement, nom_departement))

    # Insérer ou ignorer Prelevement
    cursor.execute("""
        INSERT OR IGNORE INTO Prelevement (id_prelevement, date_prelevement, code_departement)
        VALUES (?, ?, ?)
    """, (id_prelevement, date_prelevement, code_departement))

    # Insérer Analyse
    cursor.execute("""
        INSERT OR IGNORE INTO Analyse (
            id_analyse, code_parametre, reference_qualite, id_prelevement,
            libelle_parametre, code_parametre_se, code_parametre_cas,
            libelle_unite, limite_qualite_parametre, reference_qualite_parametre
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_analyse, code_parametre, reference_qualite, id_prelevement,
        libelle_parametre, code_parametre_se, code_parametre_acs,
        libelle_unite, limite_qualite_parametre, reference_qaulite_parametre
    ))

    # Insérer Réseaux liés
    if 'reseaux' in item:
        for reseau in item['reseaux']:
            cursor.execute("""
                INSERT OR IGNORE INTO Reseau (code_reseau, nom_reseau, debit, code_departement)
                VALUES (?, ?, ?, ?)
            """, (
                reseau.get('code'),
                reseau.get('nom'),
                reseau.get('debit'),
                code_departement
            ))

# Commit & close
conn.commit()
conn.close()

print("Import terminé avec succès !")
