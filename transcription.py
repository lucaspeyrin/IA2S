import streamlit as st
import requests

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Définir des variables globales pour stocker les données d'image
st.session_state.image_url = None
st.session_state.image_width = None
st.session_state.image_height = None

def get_image_data_from_api(coordinates):
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.post(api_url, json={"coordinates": coordinates})
    data = response.json()
    
    # Mise à jour des variables de session avec les nouvelles données d'image
    st.session_state.image_url = data.get("url")
    st.session_state.image_width = data.get("width")
    st.session_state.image_height = data.get("height")
    
    return st.session_state.image_url, st.session_state.image_width, st.session_state.image_height

def calculate_percentage_coordinates(coordinates, image_width, image_height):
    x_percentage = (coordinates["x"] / image_width) * 100
    y_percentage = (coordinates["y"] / image_height) * 100
    return {"x": x_percentage, "y": y_percentage}

"# :dart: Streamlit Image Coordinates"

"Try clicking on the image below."

if st.session_state.image_url is None:
    # Appel API initial pour obtenir les données d'image
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height = get_image_data_from_api({})

# Calculate the displayed height based on the displayed width of 300 pixels
displayed_height = int((st.session_state.image_height / st.session_state.image_width) * 300)
displayed_width = 300

value = streamlit_image_coordinates(
    st.session_state.image_url,
    width=displayed_width,
    height=displayed_height,
    key="url",
)

st.write(value)

if st.button("Send Coordinates"):
    percentage_coordinates = calculate_percentage_coordinates(value, st.session_state.image_width, st.session_state.image_height)
    st.session_state.image_url, st.session_state.image_width, st.session_state.image_height = get_image_data_from_api(percentage_coordinates)
