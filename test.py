import streamlit as st
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

# Classe pour gérer l'état de session
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Fonction pour obtenir l'état de session
def get_state():
    session_id = get_report_ctx().session_id
    session_state = Server.get_current()._session_infos[session_id].session_state
    return session_state

def main():
    session_state = get_state()

    # Titre de l'application
    st.title("Application de Todos")

    # Création d'une barre latérale pour la navigation entre les pages
    st.sidebar.title("Navigation")
    pages = ["Page 1", "Page 2", "Page 3"]
    selected_page = st.sidebar.radio("Aller à", pages)

    # Initialisation de l'état de session pour chaque page
    if not hasattr(session_state, "page1_todos"):
        session_state.page1_todos = ["Tâche 1", "Tâche 2", "Tâche 3"]
    if not hasattr(session_state, "page2_todos"):
        session_state.page2_todos = ["Tâche A", "Tâche B", "Tâche C"]
    if not hasattr(session_state, "page3_todos"):
        session_state.page3_todos = ["Tâche X", "Tâche Y", "Tâche Z"]

    # Affichage de la page sélectionnée
    if selected_page == "Page 1":
        show_page1(session_state.page1_todos)
    elif selected_page == "Page 2":
        show_page2(session_state.page2_todos)
    elif selected_page == "Page 3":
        show_page3(session_state.page3_todos)

# Fonction pour afficher la page 1
def show_page1(todos):
    st.header("Page 1")
    st.write("Liste de todos de la page 1 :")
    for i, todo in enumerate(todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page1_{i}")
        todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

# Fonction pour afficher la page 2
def show_page2(todos):
    st.header("Page 2")
    st.write("Liste de todos de la page 2 :")
    for i, todo in enumerate(todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page2_{i}")
        todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

# Fonction pour afficher la page 3
def show_page3(todos):
    st.header("Page 3")
    st.write("Liste de todos de la page 3 :")
    for i, todo in enumerate(todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page3_{i}")
        todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

if __name__ == "__main__":
    main()
