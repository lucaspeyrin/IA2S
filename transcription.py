import streamlit as st
import requests

# Initialisation de la clé "last_click_coordinates" dans st.session_state
if "last_click_coordinates" not in st.session_state:
    st.session_state["last_click_coordinates"] = None

# Fonction pour récupérer l'image depuis l'API
def get_image():
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    data = response.json()
    if "url" in data:
        return data["url"]
    else:
        return None

# Fonction pour envoyer les coordonnées du clic à l'API
def send_click_coordinates(x, y):
    payload = {"x": x, "y": y}
    requests.post("https://api.ia2s.app/webhook/streamlit/click", json=payload)

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Titre de l'application
st.markdown("# :dart: Streamlit Image Coordinates")

# Affichage de l'image et marquage de l'emplacement du dernier clic
def display_image(image_url):
    # Afficher l'image avec une taille maximale de 500 pixels
    st.image(image_url, use_column_width=True, caption="Click on the image", width=500)
    
    # Récupérer les coordonnées du dernier clic
    last_click_coordinates = st.session_state["last_click_coordinates"]
    if last_click_coordinates:
        x, y = last_click_coordinates
        # Marquer l'emplacement du dernier clic sur l'image
        st.markdown(f'<div style="position:relative"><img src="{image_url}" style="width:500px"><div style="position:absolute;top:{y}px;left:{x}px;"><svg height="10" width="10"><circle cx="5" cy="5" r="5" fill="red"/></svg></div></div>', unsafe_allow_html=True)

# Récupérer l'image une seule fois au chargement de l'application
image_url = get_image()

# Afficher l'image et marquer l'emplacement du dernier clic
display_image(image_url)

# Si l'utilisateur clique sur l'image, enregistrer les coordonnées du clic
if st.session_state.mouse_click:
    x, y = st.session_state.mouse_click["x"], st.session_state.mouse_click["y"]
    st.session_state["last_click_coordinates"] = (x, y)
    send_click_coordinates(x, y)
