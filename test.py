import streamlit as st

def main():
    # Titre de l'application
    st.title("Application de Todos")

    # Création d'une barre latérale pour la navigation entre les pages
    st.sidebar.title("Navigation")
    pages = ["Page 1", "Page 2", "Page 3"]
    selected_page = st.sidebar.radio("Aller à", pages)

    # Affichage de la page sélectionnée
    if selected_page == "Page 1":
        show_page1()
    elif selected_page == "Page 2":
        show_page2()
    elif selected_page == "Page 3":
        show_page3()

def show_page1():
    st.header("Page 1")
    st.write("Liste de todos de la page 1 :")
    todos = ["Tâche 1", "Tâche 2", "Tâche 3"]
    for todo in todos:
        st.write(f"- {todo}")

def show_page2():
    st.header("Page 2")
    st.write("Liste de todos de la page 2 :")
    todos = ["Tâche A", "Tâche B", "Tâche C"]
    for todo in todos:
        st.write(f"- {todo}")

def show_page3():
    st.header("Page 3")
    st.write("Liste de todos de la page 3 :")
    todos = ["Tâche X", "Tâche Y", "Tâche Z"]
    for todo in todos:
        st.write(f"- {todo}")

if __name__ == "__main__":
    main()
