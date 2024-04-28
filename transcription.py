import streamlit as st
import requests

# Fonction pour appeler l'API et récupérer l'URL de l'image
def get_image_url():
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    data = response.json()
    return data.get("url")

# Fonction pour envoyer les coordonnées (x, y) à l'API
def send_click_coordinates(x, y):
    payload = {"x": x, "y": y}
    requests.post("https://api.ia2s.app/webhook/streamlit/click", json=payload)

# Appel de la fonction pour obtenir l'URL de l'image
image_url = get_image_url()

# Affichage de l'image dans l'application Streamlit
if image_url:
    st.image(image_url, use_column_width=True, caption="Cliquez sur l'image")

    # Gestion du clic sur l'image
    if st.button("Cliquez ici"):
        click_coordinates = st.image_coordinates(image_url)
        x, y = click_coordinates["x"], click_coordinates["y"]
        send_click_coordinates(x, y)
        st.success(f"Coordonnées du clic: x={x}, y={y}")
else:
    st.error("Impossible de récupérer l'image. Veuillez réessayer plus tard.")
