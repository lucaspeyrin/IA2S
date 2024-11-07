import streamlit as st
import requests
from PIL import Image
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
    st.session_state.phone_id = None

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = None
    st.session_state.percentage_coordinates = None

if 'ignore' not in st.session_state:
    st.session_state.ignore = True

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
    if st.session_state.ignore == False:
        api_url = "https://api.ia2s.app/webhook/streamlit/actions"
        response = requests.post(api_url, json={"coordinates": coordinates, "layout": layout})
        if response.status_code != 200:
            st.session_state.ignore = True
            st.error(f"Error: API returned status code {response.status_code}")
            return []
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data.get("actions")
    else:
        return []

# Fonction pour récupérer les données de l'image de l'API avec gestion des erreurs
def get_image_data_from_api(phone_id):
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.post(api_url, json={"phone_id": phone_id})
    if response.status_code != 200:
        st.session_state.ignore = True
        st.error(f"Error: API returned status code {response.status_code}")
        return None, None, None, None
    response.raise_for_status()
    data = response.json()
    return data.get("url"), data.get("width"), data.get("height"), data.get("layout")

# Fonction pour récupérer la liste des téléphones de l'API
def get_phone_list():
    api_url = "https://api.ia2s.app/webhook/streamlit/phones"
    try:
        response = requests.get(api_url)
        
        # Vérification du code de statut de la réponse
        if response.status_code != 200:
            st.error(f"Erreur : l'API a retourné le code de statut {response.status_code}")
            return []
        
        # Tenter de décoder la réponse en JSON
        data = response.json()

        # Vérifier que la réponse est une liste
        if isinstance(data, list):
            # Extraire le nom des appareils (device_name) dans une liste
            return data
        else:
            st.error("Erreur : la réponse de l'API n'est pas au format attendu")
            return []
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la connexion à l'API : {e}")
        return []
    except ValueError as e:
        st.error("Erreur lors de l'analyse de la réponse JSON de l'API")
        return []

# Titre "Phone Id"
st.title("Phone Id")

# Appel de la fonction pour récupérer la liste des téléphones
phones = get_phone_list()
phone_options = [
    f"{phone.get('device_name', 'Unknown')} ({phone.get('alternative_name', 'N/A')}) - {phone.get('id', 'Unknown ID')}"
    for phone in phones
]
phone_ids = {phone_options[i]: phones[i]["id"] for i in range(len(phones))}
selected_phone = st.selectbox("Select Phone", options=phone_options)
st.session_state.phone_id = phone_ids[selected_phone]

if st.session_state.ignore is not True and st.session_state.image_url is None and st.session_state.phone_id is not None:
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height, st.session_state.layout = get_image_data_from_api(st.session_state.phone_id)

# Calcul des dimensions d'affichage
if st.session_state.image_width and st.session_state.image_height:
    displayed_height = int((st.session_state.image_height / st.session_state.image_width) * 300)
    displayed_width = 300
else:
    displayed_height = 2340
    displayed_width = 1080

# Affichage en colonnes
col1, col2 = st.columns(2)

# Colonne 1 : Affichage de l'image avec les coordonnées
with col1:
    if st.session_state.image_url:
        
        # Affichage de l'image avec les coordonnées
        coordinates = streamlit_image_coordinates(
            st.session_state.image_url,
            width=displayed_width,
            height=displayed_height,
            key="url",
        )
        
        # Affichage des coordonnées
        st.write(coordinates)
        st.session_state.coordinates = coordinates
        
    if st.session_state.coordinates:
        st.session_state.ignore = False
        st.session_state.percentage_coordinates = calculate_percentage_coordinates(st.session_state.coordinates, st.session_state.image_width, st.session_state.image_height)

# Colonne 2 : Boutons 'Click' et 'Refresh', affichage des actions
if st.session_state.image_url:
    with col2:
        # Affichage du Phone ID sélectionné
        st.subheader("Selected Phone ID")
        st.code(st.session_state.phone_id, language='text')  # Utilisation de st.code pour rendre le texte copiable
        
        # Bouton 'Click' pour envoyer les coordonnées de clic à l'API
        if st.button("Click"):
            if st.session_state.percentage_coordinates:
                click_url = "https://api.ia2s.app/webhook/streamlit/click"
                click_data = {
                    "phone_id": st.session_state.phone_id,
                    "x": st.session_state.percentage_coordinates["x"],
                    "y": st.session_state.percentage_coordinates["y"]
                }
                click_response = requests.post(click_url, json=click_data)
                if click_response.status_code != 200:
                    st.error(f"Error: Click API returned status code {click_response.status_code}")
                else:
                    st.success("Click sent successfully")
                    st.session_state.ignore = False
                    st.session_state.image_url = None
                    st.rerun()
                    st.session_state.actions = []

        # Bouton refresh pour rafraîchir les données de l'image
        if st.button("Refresh"):
            st.session_state.ignore = False
            st.session_state.image_url = None
            st.rerun()
            st.session_state.actions = []
        
        # Titre "Actions"
        st.title("Actions")
    
        # Si les coordonnées existent, appeler l'API pour obtenir les actions
        if st.session_state.coordinates and st.session_state.ignore is not True:
            actions = get_actions_from_api(
                {"x": (st.session_state.image_width * st.session_state.percentage_coordinates["x"]) / 100, 
                 "y": (st.session_state.image_height * st.session_state.percentage_coordinates["y"]) / 100}, 
                st.session_state.layout
            )
    
            # Afficher chaque action
            for action in actions:
                st.subheader(action["name"])
                st.code(action["xpath"])

if st.session_state.image_url is None:
    if st.button("Start"):
        st.session_state.ignore = False
        st.session_state.image_url, st.session_state.image_width, st.session_state.image_height, st.session_state.layout = get_image_data_from_api(st.session_state.phone_id)
        st.rerun()
