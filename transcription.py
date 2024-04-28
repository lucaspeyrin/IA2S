import requests
import streamlit as st

# Fonction pour récupérer la prochaine image depuis l'API
def get_next_image():
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    data = response.json()
    return data.get("url")

# Fonction pour envoyer les coordonnées du clic à l'API
def send_click_coordinates(x, y):
    payload = {"x": x, "y": y}
    requests.post("https://api.ia2s.app/webhook/streamlit/click", json=payload)

# Affichage de l'image et récupération des coordonnées du clic
value = st.image_coords(get_next_image(), key="url")
st.write(value)

# Vérification si l'utilisateur a cliqué sur l'image
if st.button("Envoyer les coordonnées du clic"):
    clicked_x, clicked_y = value
    send_click_coordinates(clicked_x, clicked_y)
    st.success("Coordonnées du clic envoyées avec succès!")
