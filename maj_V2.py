import requests
import json
import sqlite3

# --- CONFIG ---
API_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/resultats_dis?page=1&size=1007"
LOCAL_JSON = "Qeau_data_cleaned.json"
DB_PATH = "C:\Users/but-info/OneDrive - UPEC\Documents\BUT-INFO\BUT1\S2\sae_204\base_de_donnees_204_V3.db"

# --- Connect to SQLite ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Check connection and list tables ---
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("📋 Tables trouvées dans la base :", [t[0] for t in tables])


# --- Empty tables before insert ---
print("🔄 Nettoyage des tables...")
cursor.execute("DELETE FROM Reseau")
cursor.execute("DELETE FROM Analyse")
cursor.execute("DELETE FROM Prelevement")
cursor.execute("DELETE FROM Departement")
conn.commit()

# --- STEP 1: Fetch data from API ---
print("🌐 Téléchargement des données API...")
response = requests.get(API_URL)
data_api = response.json()["data"]
print(f"✅ {len(data_api)} enregistrements récupérés depuis l'API")

# --- STEP 2: Load local JSON (optional) ---
try:
    with open(LOCAL_JSON, "r", encoding="utf-8") as f:
        local_data = json.load(f)["data"]
    print(f"✅ {len(local_data)} enregistrements récupérés du fichier local")
except FileNotFoundError:
    print("⚠️ Aucun fichier local trouvé, on continue uniquement avec l'API")
    local_data = []

all_data = data_api + local_data
print(f"🔢 Total combiné : {len(all_data)} enregistrements")

# --- STEP 3: Insert unique départements ---
dept_seen = set()
for item in all_data:
    code = item["code_departement"]
    nom = item.get("nom_departement", "")
    if code not in dept_seen:
        cursor.execute("INSERT INTO Departement (code_departement, nom_departement) VALUES (?, ?)", (code, nom))
        dept_seen.add(code)

# --- STEP 4: Insert unique prélèvements ---
prelev_seen = set()
for item in all_data:
    id_prelev = item["code_prelevement"]
    if id_prelev not in prelev_seen:
        cursor.execute("INSERT INTO Prelevement (id_prelevement, date_prelevement, code_departement) VALUES (?, ?, ?)",
                       (id_prelev, item["date_prelevement"], item["code_departement"]))
        prelev_seen.add(id_prelev)

# --- STEP 5: Insert analyses ---
for idx, item in enumerate(all_data):
    cursor.execute("""
        INSERT INTO Analyse (
            id_analyse, code_parametre, reference_qualite, id_prelevement, libelle_parametre,
            code_parametre_se, code_parametre_cas, libelle_unite, limite_qualite_parametre, reference_qualite_parametre
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        idx + 1,  # simple index
        item.get("code_parametre"),
        item.get("reference_analyse"),
        item["code_prelevement"],
        item.get("libelle_parametre"),
        item.get("code_parametre_se"),
        item.get("code_parametre_cas"),
        item.get("libelle_unite"),
        item.get("limite_qualite_parametre"),
        item.get("reference_qualite_parametre")
    ))

# --- STEP 6: Insert réseaux ---
for item in all_data:
    id_prelev = item["code_prelevement"]
    for reseau in item.get("reseaux", []):
        cursor.execute("INSERT INTO Reseau (code_reseau, nom_reseau, debit, id_prelevement) VALUES (?, ?, ?, ?)",
                       (reseau.get("code"), reseau.get("nom"), reseau.get("debit"), id_prelev))

# --- Commit and close ---
conn.commit()
conn.close()
print("✅✅ Données insérées avec succès dans la base SQLite !")
