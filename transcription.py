import streamlit as st
import requests

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

def get_image_from_api():
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.get(api_url)
    data = response.json()
    image_url = data.get("url")
    return image_url

"# :dart: Streamlit Image Coordinates"

st.code("pip install streamlit-image-coordinates")

"Try clicking on the image below."

value = streamlit_image_coordinates(
    get_image_from_api(),
    key="url",
)

st.write(value)
