import streamlit as st

def main():
    # Titre de l'application
    st.title("Application de Todos")

    # Création d'une barre latérale pour la navigation entre les pages
    st.sidebar.title("Navigation")
    pages = ["Page 1", "Page 2", "Page 3"]
    selected_page = st.sidebar.radio("Aller à", pages)

    # Initialisation de l'état de session pour chaque page
    if "page1_todos" not in st.session_state:
        st.session_state.page1_todos = ["Tâche 1", "Tâche 2", "Tâche 3"]
    if "page2_todos" not in st.session_state:
        st.session_state.page2_todos = ["Tâche A", "Tâche B", "Tâche C"]
    if "page3_todos" not in st.session_state:
        st.session_state.page3_todos = ["Tâche X", "Tâche Y", "Tâche Z"]

    # Affichage de la page sélectionnée
    if selected_page == "Page 1":
        show_page1()
    elif selected_page == "Page 2":
        show_page2()
    elif selected_page == "Page 3":
        show_page3()

# Fonction pour afficher la page 1
def show_page1():
    st.header("Page 1")
    st.write("Liste de todos de la page 1 :")
    for i, todo in enumerate(st.session_state.page1_todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page1_{i}")
        st.session_state.page1_todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

# Fonction pour afficher la page 2
def show_page2():
    st.header("Page 2")
    st.write("Liste de todos de la page 2 :")
    for i, todo in enumerate(st.session_state.page2_todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page2_{i}")
        st.session_state.page2_todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

# Fonction pour afficher la page 3
def show_page3():
    st.header("Page 3")
    st.write("Liste de todos de la page 3 :")
    for i, todo in enumerate(st.session_state.page3_todos):
        todo_status = st.checkbox(f"{todo}", value=False, key=f"page3_{i}")
        st.session_state.page3_todos[i] = todo_status
        st.write(f"- {todo} ({todo_status})")

if __name__ == "__main__":
    main()
