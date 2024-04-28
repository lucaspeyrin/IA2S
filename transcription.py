import streamlit as st
import requests

# Initialisation de la clé "image_clicked" dans st.session_state
if "image_clicked" not in st.session_state:
    st.session_state["image_clicked"] = None

# Fonction pour récupérer la prochaine image depuis l'API
def get_next_image():
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    data = response.json()
    if "url" in data:
        return data["url"]
    else:
        return None

# Fonction pour envoyer les coordonnées du clic à l'API
def send_click_coordinates(x, y):
    payload = {"x": x, "y": y}
    requests.post("https://api.ia2s.app/webhook/streamlit/click", json=payload)

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Streamlit Image Coordinates",
    page_icon="🎯",
    layout="wide",
)

# Titre de l'application
st.markdown("# :dart: Streamlit Image Coordinates")

# Fonction pour afficher l'image et récupérer les coordonnées du clic
def display_image_with_coordinates(image_url):
    value = st.image(image_url, use_column_width=True, caption="Click on the image")
    if value:
        click_coordinates = st.session_state["image_clicked"]
        if click_coordinates:
            x, y = click_coordinates
            send_click_coordinates(x, y)
            st.info(f"Coordinates clicked: ({x}, {y})")

# Fonction principale de l'application
def main():
    image_url = get_next_image()
    if image_url:
        display_image_with_coordinates(image_url)
    else:
        st.error("Failed to fetch the next image from the API.")

if __name__ == "__main__":
    main()
