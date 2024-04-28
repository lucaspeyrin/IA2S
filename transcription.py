import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import requests

def send_click_coordinates(x, y):
    url = "https://api.ia2s.app/webhook/streamlit/click"
    data = {"x": x, "y": y}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        st.success("Coordonnées du clic envoyées avec succès !")
    else:
        st.error("Erreur lors de l'envoi des coordonnées du clic.")

def main():
    st.title("Application Streamlit pour les clics sur les images")

    # Demander la première image en utilisant votre API
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    if response.status_code == 200:
        image_data = response.json()["data"]
        st.image(image_data, use_column_width=True, caption="Cliquez sur l'image")

        # Récupérer les coordonnées du clic de l'utilisateur
        value = streamlit_image_coordinates(image_data, key="local")
        st.write(value)

        # Envoyer les coordonnées du clic à votre API
        if value:
            x, y = value["x"], value["y"]
            send_click_coordinates(x, y)
    else:
        st.error("Erreur lors de la récupération de l'image.")

if __name__ == "__main__":
    main()
