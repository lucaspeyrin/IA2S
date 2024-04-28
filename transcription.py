import streamlit as st
import requests

# Fonction pour faire l'appel API
def call_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la requête API: {response.status_code}")

# Interface utilisateur avec Streamlit
def main():
    st.title("Exemple d'appel API avec Streamlit")
    
    # URL de l'API
    api_url = "https://api.exemple.com/data"
    
    # Bouton pour déclencher l'appel API
    if st.button("Obtenir des données depuis l'API"):
        data = call_api(api_url)
        if data:
            st.write("Données récupérées depuis l'API:")
            st.write(data)

if __name__ == "__main__":
    main()
