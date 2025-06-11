import folium
import json
import requests
import os

# Charger les données GeoJSON
url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
response = requests.get(url_geojson)
departements_geojson = response.json()

# Créer la carte
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Ajouter chaque département avec le nom comme tooltip
for feature in departements_geojson["features"]:
    folium.GeoJson(
        feature,
        style_function=lambda f: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda f: {
            'fillColor': 'grey',
            'fillOpacity': 0.7,
            'weight': 2
        },
        tooltip=folium.GeoJsonTooltip(fields=["nom"], aliases=["Département :"])
    ).add_to(m)

# Injection du JavaScript pour la communication avec la page parente
map_js_variable_name = m.get_name()
# Modif: Encapsuler le script dans un écouteur d'événement 'load' pour s'assurer que la carte est entièrement chargée
js_after_map_creation = f"""
<script>
    // Le code à l'intérieur de cette fonction ne s'exécutera qu'une fois que tout le contenu de la page
    // (y compris la carte Folium/Leaflet) est complètement chargé.
    window.addEventListener('load', function() {{
        // Vérifier si la variable de la carte est définie après le chargement complet de la fenêtre
        if (typeof {map_js_variable_name} !== 'undefined') {{
            {map_js_variable_name}.eachLayer(function(layer) {{
                // S'assurer que le layer a une feature et des propriétés (c'est-à-dire que c'est un département)
                if (layer.feature && layer.feature.properties && layer.feature.properties.code) {{
                    layer.on('click', function(e) {{
                        var departmentName = e.target.feature.properties.nom;
                        var departmentCode = e.target.feature.properties.code;
                        // Envoyer le message à la page parente
                        window.parent.postMessage({{
                            type: 'departmentClick',
                            name: departmentName,
                            code: departmentCode
                        }}, '*'); // Utilisez '*' ou l'origine spécifique pour la sécurité
                    }});
                }}
            }});
        }} else {{
            console.error("La variable de la carte Folium '{map_js_variable_name}' n'est toujours pas définie après le chargement de la page. Il pourrait y avoir un problème plus profond avec l'initialisation de la carte.");
        }}
    }});
</script>
"""
m.get_root().html.add_child(folium.Element(js_after_map_creation))

m.save("templates/carte_departements.html")