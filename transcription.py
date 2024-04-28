import streamlit as st
import requests
from streamlit_image_coordinates import streamlit_image_coordinates

# Vérifier si les variables d'image sont déjà initialisées dans la session
if 'image_url' not in st.session_state:
    st.session_state.image_url = None
    st.session_state.image_width = None
    st.session_state.image_height = None

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = None

# Fonction pour récupérer les données d'image de l'API
def get_image_data_from_api(coordinates):
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.post(api_url, json={"coordinates": coordinates})
    data = response.json()
    
    # Mettre à jour les variables de session avec les nouvelles données d'image
    st.session_state.image_url = data.get("url")
    st.session_state.image_width = data.get("width")
    st.session_state.image_height = data.get("height")
    
    return st.session_state.image_url, st.session_state.image_width, st.session_state.image_height

# Fonction pour calculer les coordonnées en pourcentage
def calculate_percentage_coordinates(coordinates, image_width, image_height):
    if coordinates:
        x_percentage = (coordinates["x"] / image_width) * 100
        y_percentage = (coordinates["y"] / image_height) * 100
        return {"x": x_percentage, "y": y_percentage}
    else:
        return {}

# Définir une fonction de rappel pour mettre à jour les variables en fonction des coordonnées
@st.cache(suppress_st_warning=True)
def update_variables():
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height = get_image_data_from_api(st.session_state.percentage_coordinates)
    st.session_state.coordinates = streamlit_image_coordinates(
        st.session_state.image_url,
        width=displayed_width,
        height=displayed_height,
        key="url",
    )

# Affichage de l'interface utilisateur Streamlit
st.title("Streamlit Image Coordinates")

# Calculer les coordonnées en pourcentage en premier
st.session_state.percentage_coordinates = calculate_percentage_coordinates(st.session_state.coordinates, st.session_state.image_width, st.session_state.image_height)

# Obtenir les données d'image de l'API en utilisant les coordonnées en pourcentage
if st.session_state.coordinates is None:
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height = get_image_data_from_api({})
    st.write("First execution")
else:
    update_variables()
    st.write("Next execution")

# Calculer la hauteur affichée en fonction de la largeur affichée de 300 pixels
displayed_height = int((st.session_state.image_height / st.session_state.image_width) * 300)
displayed_width = 300

# Affichage des coordonnées
st.write(st.session_state.coordinates)
