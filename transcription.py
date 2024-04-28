import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Fonction pour récupérer l'image de l'API
def get_image_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        return image
    else:
        st.error("Failed to fetch image from API")
        return None

# URL de l'API
api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"

# Récupération de l'image depuis l'API
image = get_image_from_api(api_url)

# Vérification si l'image a été récupérée avec succès
if image:
    # Affichage de l'image
    st.image(image, use_column_width=True)

    # Récupération des coordonnées des clics
    value = st.image_coords(image)

    # Affichage des coordonnées des clics
    st.write("Coordinates of last click:", value)
