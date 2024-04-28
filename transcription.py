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

def send_coordinates_to_api(coordinates):
    api_url = "https://api.ia2s.app/webhook/streamlit/coordinates"
    response = requests.post(api_url, json={"coordinates": coordinates})
    if response.status_code == 200:
        st.success("Coordinates sent successfully.")
        return response.json()
    else:
        st.error("Failed to send coordinates.")
        return None

"# :dart: Streamlit Image Coordinates"

"Try clicking on the image below."

value = streamlit_image_coordinates(
    get_image_from_api(),
    width=300,
    key="url",
)

st.write(value)

st.write("Coordinates (in percentage):")
if value:
    image_width, image_height = value["image_dimensions"]
    coordinates_percentage = [(x / image_width * 100, y / image_height * 100) for x, y in value["coordinates"]]
    st.write(coordinates_percentage)

if st.button("Send Coordinates"):
    response_data = send_coordinates_to_api(value)
    if response_data:
        new_image_url = response_data.get("url")
        if new_image_url:
            st.write("New Image:")
            st.image(new_image_url, width=300)
        else:
            st.warning("No new image URL received.")
