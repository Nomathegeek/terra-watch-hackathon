import streamlit as st
import pandas as pd

# Configuration
st.set_page_config(page_title="TerraWatch AI", layout="wide")

# Titre
st.title("🌍 TerraWatch AI - Prototype Hackathon")
st.markdown("**Détection intelligente des changements terrestres par satellite**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres d'analyse")
    zone = st.selectbox("Zone d'étude", ["Amazonie", "Dubai", "Forêt des Landes"])
    annee = st.slider("Période d'analyse", 2019, 2024, (2020, 2024))
    
    if st.button("🚀 Lancer la simulation IA", type="primary"):
        analyser = True
    else:
        analyser = False

# Contenu principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Visualisation des changements")
    
    # Image satellite selon la zone
    if zone == "Amazonie":
        st.image("https://i.imgur.com/9ZqD3yl.png", 
                caption=f"Zone analysée : {zone} | Période : {annee[0]}-{annee[1]}")
    elif zone == "Dubai":
        st.image("https://i.imgur.com/XJpD8kE.png", 
                caption=f"Zone analysée : {zone} | Période : {annee[0]}-{annee[1]}")
    else:
        st.image("https://i.imgur.com/Yc7BwCq.png", 
                caption=f"Zone analysée : {zone} | Période : {annee[0]}-{annee[1]}")
    
    if analyser:
        st.success("✅ Analyse IA terminée ! Changements détectés en rouge.")

with col2:
    st.subheader("📊 Résultats de l'analyse")
    
    if analyser:
        # Métriques
        st.metric("**Superficie affectée**", "15.2 ha", delta="-2.4%")
        st.metric("**Confiance de l'IA**", "92%", delta="+1.5%")
        st.metric("**Impact CO₂ estimé**", "144 kt")
        
        # Données simulées
        st.subheader("📈 Évolution de la couverture")
        data = pd.DataFrame({
            'Année': [2019, 2020, 2021, 2022, 2023, 2024],
            'Couverture (%)': [100, 95, 88, 82, 77, 75]
        })
        
        # Afficher tableau
        st.dataframe(data, use_container_width=True, hide_index=True)
        
        # Téléchargement
        csv = data.to_csv(index=False)
        st.download_button(
            label="📥 Exporter les données",
            data=csv,
            file_name=f"terra_watch_{zone}.csv",
            mime="text/csv"
        )
        
        # Conclusion
        st.info(f"""
        **Résumé pour {zone} :**
        - Perte de **15.2 hectares** entre {annee[0]} et {annee[1]}
        - Confiance de détection : **92%**
        - Recommandation : **Surveillance renforcée** requise
        """)
    else:
        st.info("""
        **Prêt à analyser ?**
        1. Sélectionnez une zone
        2. Ajustez la période
        3. Lancez la simulation IA
        
        *Les résultats apparaîtront ici en temps réel.*
        """)

# Pied de page
st.divider()
st.caption("🚀 **TerraWatch AI** - Prototype pour Hackathon IA | Surveillance territoriale par intelligence artificielle")
