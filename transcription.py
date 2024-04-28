import streamlit as st
import requests

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

def get_image_data_from_api():
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.get(api_url)
    data = response.json()
    image_url = data.get("url")
    image_width = data.get("width")
    image_height = data.get("height")
    return image_url, image_width, image_height

def send_coordinates_to_api(coordinates):
    api_url = "https://api.ia2s.app/webhook/streamlit/coordinates"
    response = requests.post(api_url, json={"coordinates": coordinates})
    if response.status_code == 200:
        st.success("Coordinates sent successfully.")
        return response.json()
    else:
        st.error("Failed to send coordinates.")
        return None

def calculate_percentage_coordinates(coordinates, image_width, image_height):
    x_percentage = (coordinates["x"] / image_width) * 100
    y_percentage = (coordinates["y"] / image_height) * 100
    return {"x": x_percentage, "y": y_percentage}

"# :dart: Streamlit Image Coordinates"

"Try clicking on the image below."

image_url, image_width, image_height = get_image_data_from_api()

# Calculate the displayed height based on the displayed width of 300 pixels
displayed_height = int((image_height / image_width) * 300)
displayed_width = 300

value = streamlit_image_coordinates(
    image_url,
    width=displayed_width,
    height=displayed_height,
    key="url",
)

st.write(value)

if st.button("Send Coordinates"):
    percentage_coordinates = calculate_percentage_coordinates(value, displayed_width, displayed_height)
    response_data = send_coordinates_to_api(percentage_coordinates)
    if response_data:
        image_url = response_data.get("url")  # Update image_url if response_data exists

        # Display the new image URL
        st.write("New Image URL:", image_url)
