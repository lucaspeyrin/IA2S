import streamlit as st
import requests

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Définir des variables globales pour stocker les données d'image
image_url = None
image_width = None
image_height = None

def get_image_data_from_api(coordinates):
    global image_url, image_width, image_height
    
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.post(api_url, json={"coordinates": coordinates})
    data = response.json()
    
    # Mise à jour des variables globales avec les nouvelles données d'image
    image_url = data.get("url")
    image_width = data.get("width")
    image_height = data.get("height")
    
    return image_url, image_width, image_height

def calculate_percentage_coordinates(coordinates, image_width, image_height):
    x_percentage = (coordinates["x"] / image_width) * 100
    y_percentage = (coordinates["y"] / image_height) * 100
    return {"x": x_percentage, "y": y_percentage}

"# :dart: Streamlit Image Coordinates"

"Try clicking on the image below."

if image_url is None:
    # Appel API initial pour obtenir les données d'image
    image_url, image_width, image_height = get_image_data_from_api({})

# Calculate the displayed height based on the displayed width of 300 pixels
displayed_height = int((image_height / image_width) * 300)
displayed_width = 300

value = streamlit_image_coordinates(
    image_url,
    width=displayed_width,
    height=displayed_height,
    key="url",
)

# Observer les changements de la valeur `value`
if st.session_state.url != value:
    st.session_state.url = value
    percentage_coordinates = calculate_percentage_coordinates(value, image_width, image_height)
    get_image_data_from_api(percentage_coordinates)

# Afficher l'image mise à jour
st.image(image_url, width=displayed_width, caption="Updated Image")

