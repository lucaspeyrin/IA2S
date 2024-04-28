import streamlit as st
import requests

from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Définir des variables globales pour stocker les données d'image
@st.cache(allow_output_mutation=True)
def get_image_data_from_api(coordinates):
    api_url = "https://api.ia2s.app/webhook/streamlit/screenshot"
    response = requests.post(api_url, json={"coordinates": coordinates})
    data = response.json()
    return data.get("url"), data.get("width"), data.get("height")

@st.cache
def calculate_percentage_coordinates(coordinates, image_width, image_height):
    x_percentage = (coordinates["x"] / image_width) * 100
    y_percentage = (coordinates["y"] / image_height) * 100
    return {"x": x_percentage, "y": y_percentage}

# Initialize variables
image_url, image_width, image_height = None, None, None

def main():
    global image_url, image_width, image_height
    
    def update_image_data(coordinates):
        nonlocal image_url, image_width, image_height
        image_url, image_width, image_height = get_image_data_from_api(coordinates)
    
    "# :dart: Streamlit Image Coordinates"

    "Try clicking on the image below."

    if image_url is None:
        # Appel API initial pour obtenir les données d'image
        update_image_data({})

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
        percentage_coordinates = calculate_percentage_coordinates(value, image_width, image_height)
        update_image_data(percentage_coordinates)

if __name__ == "__main__":
    main()
