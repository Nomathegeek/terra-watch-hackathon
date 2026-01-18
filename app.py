import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import tempfile

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
               zoom_start=selected_zone["zoom"])

# Ajouter la couche satellite (ESRI)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri Satellite',
    name='Vue satellite',
    overlay=False,
    control=True
).add_to(m)

# Ajouter OpenStreetMap comme option
folium.TileLayer('OpenStreetMap', name='Carte standard').add_to(m)
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

# Sauvegarder la carte en HTML temporaire
if analyser:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
        m.save(tmpfile.name)
        html_file = tmpfile.name
    
    # Lire le fichier HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

# Affichage
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Carte satellite interactive")
    st.write("*Utilisez la souris pour zoomer/déplacer*")
    
    if analyser:
        # Afficher la carte HTML
        st.components.v1.html(html_content, width=700, height=500, scrolling=True)
    else:
        # Carte par défaut sans analyse
        m_default = folium.Map(location=[selected_zone["lat"], selected_zone["lon"]], 
                              zoom_start=selected_zone["zoom"])
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri Satellite'
        ).add_to(m_default)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
            m_default.save(tmpfile.name)
            with open(tmpfile.name, 'r', encoding='utf-8') as f:
                html_default = f.read()
        
        st.components.v1.html(html_default, width=700, height=500, scrolling=True)
    
    # Légende
    st.markdown("""
    **Légende :**
    - 🟥 **Cercle rouge** : Changements détectés (15.2 ha)
    - 📍 **Marqueur rouge** : Centre de la zone analysée
    - 🌍 **Basculer la vue** : Icône en haut à droite (satellite/carte)
    """)

with col2:
    st.subheader("📊 Résultats")
    
    if analyser:
        # Métriques
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Superficie", "15.2 ha", "-2.4%")
        with col_b:
            st.metric("Confiance IA", "92%", "+1.5%")
        
        st.metric("CO₂ émis", "144 kt")
        
        # Graphique
        st.subheader("📈 Évolution 2020-2024")
        data = pd.DataFrame({
            'Année': [2020, 2021, 2022, 2023, 2024],
            'Couverture (%)': [100, 92, 85, 78, 75]
        })
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(data['Année'], data['Couverture (%)'], 
                marker='o', linewidth=2, color='green')
        ax.set_xlabel('Année')
        ax.set_ylabel('Couverture (%)')
        ax.grid(True, alpha=0.3)
        ax.fill_between(data['Année'], data['Couverture (%)'], alpha=0.2, color='green')
        st.pyplot(fig)
        
        # Téléchargement
        st.download_button(
            "📥 Télécharger rapport",
            data=f"Rapport TerraWatch AI\nZone: {zone}\nSuperficie: 15.2 ha\nConfiance: 92%",
            file_name=f"terra_watch_{zone}.txt",
            mime="text/plain"
        )
    else:
        st.info("""
        **Instructions :**
        1. Sélectionnez une zone
        2. Cliquez sur **🚀 Lancer la simulation**
        3. Visualisez les résultats
        
        *La carte est interactive : zoom et déplacement possibles.*
        """)

# Pied de page
st.divider()
st.caption("🚀 **TerraWatch AI** - Prototype Hackathon IA | Carte interactive Folium")
