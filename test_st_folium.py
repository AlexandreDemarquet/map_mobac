import folium
from streamlit_folium import st_folium
import streamlit as st

# Créer une carte centrée sur la Méditerranée
m = folium.Map(
    location=[38, 15],  # Coordonnées centrées sur la Méditerranée
    zoom_start=8,  # Niveau de zoom initial
    tiles=None, # Ne pas utiliser de tuiles par défaut
    crs='EPSG4326'

)

# Ajouter les tuiles locales extraites du fichier MBTiles
#local_tiles_path = "http://localhost:8000/{z}/{x}/{y}.png"
local_tiles_path = "./tiles_output/{z}/{x}/{y}.png"
folium.TileLayer(
    tiles=local_tiles_path,
    attr="Tuiles locales MBTiles",
    name="Local MBTiles"
).add_to(m)

# Ajouter des marqueurs pour tester
folium.Marker([43.3, 5.4], tooltip="Marseille", popup="Marseille").add_to(m)
folium.Marker([43.7, 7.3], tooltip="Nice", popup="Nice").add_to(m)

# Afficher la carte dans Streamlit
st.title("Carte de la Méditerranée avec MBTiles (Hors Ligne)")
st_folium(m, width=800, height=600)

