import streamlit as st
import requests
from streamlit_image_coordinates import streamlit_image_coordinates


# Initialisation des variables de session
if 'image_url' not in st.session_state:
    st.session_state.image_url = None
    st.session_state.image_width = None
    st.session_state.image_height = None
    st.session_state.layout = None

if 'actions' not in st.session_state:
    st.session_state.actions = []

if 'phone_id' not in st.session_state:
    st.session_state.phone_id = "0afabf51-238e-4e1e-be1b-9388c97fe006"

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = None
    st.session_state.percentage_coordinates = None
    st.session_state.ignore = False

# Fonction pour calculer les coordonnées en pourcentage
def calculate_percentage_coordinates(coordinates, image_width, image_height):
    if coordinates:
        x_percentage = (coordinates["x"] / displayed_width) * 100
        y_percentage = (coordinates["y"] / displayed_height) * 100
        return {"x": x_percentage, "y": y_percentage}
    else:
        return {}

# Fonction pour récupérer les actions de l'API avec gestion des erreurs
def get_actions_from_api(coordinates, layout):
    api_url = "https://api.ia2s.app/webhook/streamlit/actions"
    try:
        response = requests.post(api_url, json={"coordinates": coordinates, "layout": layout})
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data.get("actions")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching actions from the API: {e}")
        st.session_state.ignore = True
        return []

# Fonction pour récupérer les données de l'image de l'API avec gestion des erreurs
def get_image_data_from_api(phone_id):
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    try:
        response = requests.post(api_url, json={"phone_id": phone_id})
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data.get("url"), data.get("width"), data.get("height"), data.get("layout")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching image data from the API: {e}")
        st.session_state.ignore = True
        return None, None, None, None

# Titre "Phone Id"
st.title("Phone Id")

# Input pour le phone id
st.session_state.phone_id = st.text_input("Phone Id", st.session_state.phone_id)

# Si le phone id est rempli et l'image URL est vide, faire l'appel API pour obtenir les données de l'image
if st.session_state.phone_id and not st.session_state.image_url and st.session_state.ignore is not True:
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height, st.session_state.layout = get_image_data_from_api(st.session_state.phone_id)


if st.session_state.image_width and st.session_state.image_height:
    # Calcul de la hauteur affichée en fonction de la largeur affichée de 300 pixels
    displayed_height = int((st.session_state.image_height / st.session_state.image_width) * 300)
    displayed_width = 300

# Affichage en colonnes
col1, col2 = st.columns(2)

# Colonne 1 : Affichage de l'image avec les coordonnées
with col1:
    # Affichage de l'image avec les coordonnées
    coordinates = streamlit_image_coordinates(
        st.session_state.image_url,
        width=displayed_width,
        height=displayed_height,
        key="url",
    )
    
    # Affichage des coordonnées
    st.write(coordinates)
    
    if coordinates:
        st.session_state.coordinates = coordinates
        st.session_state.ignore = False
        st.session_state.percentage_coordinates = calculate_percentage_coordinates(st.session_state.coordinates, st.session_state.image_width, st.session_state.image_height)

# Colonne 2 : Bouton refresh et affichage des actions
with col2:
    # Bouton refresh pour rafraîchir les données de l'image
    if st.button("Refresh"):
        st.session_state.image_url, st.session_state.image_width, st.session_state.image_height, st.session_state.layout = get_image_data_from_api(st.session_state.phone_id)
        st.session_state.actions = []
        st.session_state.ignore = False

    # Titre "Actions"
    st.title("Actions")

    # Si les coordonnées existent, appeler l'API pour obtenir les actions
    if st.session_state.coordinates and st.session_state.ignore is not True:
        actions = get_actions_from_api(
            {"x": (st.session_state.image_width * st.session_state.percentage_coordinates["x"])/100, 
             "y": (st.session_state.image_height * st.session_state.percentage_coordinates["y"])/100}, 
            st.session_state.layout
        )

        # Afficher chaque action
        for action in actions:
            st.subheader(action["name"])
            st.code(action["xpath"])

