import streamlit as st
import requests

def get_next_image():
    response = requests.get("https://api.ia2s.app/webhook/streamlit/screenshot")
    return response.json()["url"]

def send_click_coordinates(x, y):
    requests.post("https://api.ia2s.app/webhook/streamlit/click", json={"x": x, "y": y})

def main():
    st.set_page_config(page_title="Image Clicker App", layout="wide")

    st.title("Image Clicker App")

    # Récupérer l'URL de la prochaine image
    image_url = get_next_image()

    # Afficher l'image et récupérer les coordonnées du clic
    value = st.image(image_url, use_column_width=True)
    if value:
        x, y = value
        send_click_coordinates(x, y)

        # Attendre la prochaine image
        st.write("Waiting for the next image...")
        st.stop()

if __name__ == "__main__":
    main()
