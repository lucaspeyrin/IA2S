import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Fonction pour récupérer l'image depuis l'API
def get_image_from_api():
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.get(api_url)
    if response.status_code == 200:
        image_url = response.json().get("url")
        if image_url:
            # Télécharger l'image depuis l'URL
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Ouvrir l'image avec PIL
                image = Image.open(BytesIO(image_response.content))
                return image
    return None

# Créez l'application Streamlit
st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Affichez le titre
st.title(":dart: Streamlit Image Coordinates")

# Récupérez l'image depuis l'API
image = get_image_from_api()

if image:
    # Affichez l'image
    st.image(image, use_column_width=True, caption="Click on the image")

    # Récupérez les coordonnées du clic
    click_coordinates = st.image_coordinates(image)

    # Affichez les coordonnées
    st.write("Coordinates of the last click:", click_coordinates)
else:
    st.write("Failed to retrieve image from the API.")
