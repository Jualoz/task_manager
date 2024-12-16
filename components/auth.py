import streamlit as st
from db import SessionLocal, db_functions
import re  # Para trabajar con expresiones regulares

def is_valid_email(email):
    """Verifica si el email tiene un formato válido."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$"
    return re.match(email_regex, email) is not None

def login():
    option = st.radio("Choose an action:", ["Create", "Login"])

    if option == "Create":
        st.subheader("Create Account")
        with st.form(key='create'):
            username_input = st.text_input('Enter UserName')
            email_input = st.text_input('Enter Email')
            password_input = st.text_input('Enter Password', type='password')
            submit_button = st.form_submit_button('Create')

            if submit_button:
                # Validar que los campos no estén vacíos
                if not username_input or not email_input or not password_input:
                    st.error("All fields are required.")
                # Validar rango de longitud para el username
                elif len(username_input) < 3 or len(username_input) > 15:
                    st.error("Username must be between 3 and 15 characters long.")
                # Validar formato del email
                elif not is_valid_email(email_input):
                    st.error("Please enter a valid email address.")
                else:
                    db = SessionLocal()
                    result = db_functions.create_user(db, username_input, email_input, password_input)

                    if "error" in result:
                        st.error(result["error"])  # Muestra el mensaje de error
                    elif "user" in result:
                        user = result["user"]
                        st.success(f"Account created for {user.username} with email {user.email}!")
                    else:
                        st.error("Unexpected error occurred.")

    elif option == "Login":
        st.subheader("Login")
        with st.form(key='login'):
            username_input = st.text_input('Enter UserName')
            password_input = st.text_input('Enter Password', type='password')
            login_button = st.form_submit_button('Login')

            if login_button:
                # Verificar si algún campo está vacío
                if not username_input or not password_input:
                    st.error("Both username and password are required.")
                else:
                    db = SessionLocal()
                    result = db_functions.verify_user_credentials(db, username_input, password_input)

                    if result["status"] == "user_not_found":
                        st.error(f"The username '{username_input}' does not exist.")
                    elif result["status"] == "wrong_password":
                        st.error("Incorrect password. Please try again.")
                    elif result["status"] == "success":
                        user = result["user"]
                        st.session_state.user_id = user.id  # Guardar el ID del usuario en la sesión
                        st.rerun()
                        return True
                    else:
                        st.error("An unexpected error occurred. Please try again.")

    return False  # Si no se autentica, devuelve False
