import streamlit as st
import folium
from streamlit_folium import folium_static  # CHANGÉ : folium_static au lieu de st_folium
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Configuration
st.set_page_config(page_title="TerraWatch AI", layout="wide")

# Titre
st.title("🌍 TerraWatch AI - Prototype Hackathon")
st.markdown("**Détection des changements terrestres par satellite**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    zone = st.selectbox("Zone d'étude", ["Amazonie", "Dubai", "Forêt des Landes"])
    
    # Coordonnées pour chaque zone
    zones_data = {
        "Amazonie": {"lat": -3.465, "lon": -62.215, "zoom": 10},
        "Dubai": {"lat": 25.2048, "lon": 55.2708, "zoom": 12},
        "Forêt des Landes": {"lat": 44.2, "lon": -0.74, "zoom": 11}
    }
    
    date_debut = st.date_input("Date début", date(2020, 1, 1))
    date_fin = st.date_input("Date fin", date(2024, 1, 1))
    analyser = st.button("🚀 Lancer la simulation", type="primary")

# Créer la carte Folium
selected_zone = zones_data[zone]
m = folium.Map(location=[selected_zone["lat"], selected_zone["lon"]], 
               zoom_start=selected_zone["zoom"],
               tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
               attr='Esri Satellite Imagery',
               name='Satellite')

# Ajouter une couche de carte alternative (optionnel)
folium.TileLayer('OpenStreetMap').add_to(m)
folium.LayerControl().add_to(m)

# Si analyse déclenchée, ajouter une zone simulée
if analyser:
    # Ajouter un marqueur
    folium.Marker(
        [selected_zone["lat"], selected_zone["lon"]],
        popup="Zone de changement détectée",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Ajouter un cercle rouge (zone affectée)
    folium.Circle(
        location=[selected_zone["lat"], selected_zone["lon"]],
        radius=2000,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.3,
        popup="Superficie affectée: 15.2 ha"
    ).add_to(m)
    
    st.success("✅ Analyse terminée ! Zone de changement détectée en rouge.")

# Affichage
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Carte satellite interactive")
    st.write("*Zoom : molette | Déplacement : cliquer-glisser*")
    
    # Afficher la carte avec folium_static (GARANTI de fonctionner)
    folium_static(m, width=700, height=500)
    
    # Légende
    st.markdown("""
    **Légende :**
    - 🟥 **Zone rouge** : Changements détectés (15.2 ha)
    - 📍 **Marqueur** : Centre de la zone analysée
    - 🌍 **Basculer la vue** : Icône en haut à droite
    """)

with col2:
    st.subheader("📊 Résultats")
    
    if analyser:
        # Métriques dans des cartes
        st.metric(label="**Superficie affectée**", value="15.2 ha", delta="-2.4%")
        st.metric(label="**Confiance IA**", value="92%", delta="+1.5%")
        st.metric(label="**CO₂ émis estimé**", value="144 kt")
        
        # Séparateur
        st.divider()
        
        # Graphique
        st.subheader("📈 Évolution 2020-2024")
        data = pd.DataFrame({
            'Année': [2020, 2021, 2022, 2023, 2024],
            'Couverture (%)': [100, 92, 85, 78, 75]
        })
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(data['Année'], data['Couverture (%)'], 
                marker='o', linewidth=2, color='#1E88E5', markersize=8)
        ax.set_xlabel('Année')
        ax.set_ylabel('Couverture (%)', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.fill_between(data['Année'], data['Couverture (%)'], alpha=0.2, color='#1E88E5')
        
        # Ajouter les valeurs sur les points
        for i, (année, valeur) in enumerate(zip(data['Année'], data['Couverture (%)'])):
            ax.text(année, valeur+1, f'{valeur}%', ha='center', fontsize=9)
        
        st.pyplot(fig)
        
        # Téléchargement
        st.download_button(
            label="📥 Télécharger le rapport",
            data=f"Rapport TerraWatch AI\nZone: {zone}\nSuperficie affectée: 15.2 ha\nConfiance: 92%\nPériode: {date_debut} à {date_fin}",
            file_name=f"terra_watch_{zone}.txt",
            mime="text/plain"
        )
    else:
        st.info("""
        **Instructions :**
        1. Sélectionnez une zone
        2. Ajustez les dates si besoin
        3. Cliquez sur **🚀 Lancer la simulation**
        
        *Les résultats apparaîtront ici.*
        """)

# Pied de page
st.divider()
cols = st.columns(3)
with cols[1]:
    st.caption("🚀 **TerraWatch AI** - Prototype Hackathon IA")
    st.caption("Carte interactive avec Folium & Streamlit")