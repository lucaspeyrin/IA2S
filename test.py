import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html


hide_streamlit_style = """
<style>

.viewerBadge_container__1QSob {
    display: none !important;
}

.css-1avcm0n.e13qjvis2 {visibility: hidden;}
.css-erpbzb.e1ewe7hr3 {visibility: hidden;}
.css-q16mip.ejj6ze0 {visibility: hidden;}
.css-erpbzb.e1ewe7hr3 {visibility: hidden;}
.stActionButton {visibility: hidden;}
.css-14xtw13.e13qjvis0 {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def afficher_taches(taches):
    for tache in taches:
        st.write(f"- {tache}")

def main():
    st.title("Tâches d'Anne Lorie aujourd'hui")
    
    taches = [
        "Répondre aux e-mails",
        "Préparer le rapport de vente",
        "Planifier la réunion d'équipe",
        "Finaliser la présentation client"
    ]
    
    taches_effectuees = []
    
    for i, tache in enumerate(taches):
        tache_effectuee = st.checkbox(tache)
        if tache_effectuee:
            taches_effectuees.append(tache)
    
    st.write("\n\n**Tâches effectuées :**")
    if not taches_effectuees:
        st.write("Aucune tâche effectuée pour le moment.")
    else:
        afficher_taches(taches_effectuees)
    
    st.write("\n\n**Tâches restantes :**")
    taches_restantes = list(set(taches) - set(taches_effectuees))
    if not taches_restantes:
        st.write("Toutes les tâches ont été effectuées.")
    else:
        afficher_taches(taches_restantes)

if __name__ == "__main__":
    main()
