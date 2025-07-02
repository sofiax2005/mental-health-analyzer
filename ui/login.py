import streamlit as st
import requests

FIREBASE_API_KEY = "AIzaSyDkM5LMKrPboIXpxNN6XQz6jMV1Nodu1FY"

def signup_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(url, json=payload).json()

def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(url, json=payload).json()

def login_ui():
    st.sidebar.title("🔐 Login")
    choice = st.sidebar.selectbox("Login or Signup", ["Login", "Signup"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Signup":
        if st.sidebar.button("Create Account"):
            response = signup_user(email, password)
            if "error" in response:
                st.sidebar.error(f"Signup failed: {response['error']['message']}")
            else:
                st.sidebar.success("Account created! Please log in.")

    if choice == "Login":
        if st.sidebar.button("Login"):
            response = login_user(email, password)
            if "error" in response:
                st.sidebar.error(f"Login failed: {response['error']['message']}")
            else:
                st.session_state["user"] = response
                st.sidebar.success("Logged in!")

    if "user" not in st.session_state:
        st.warning("Please log in to use the app.")
        return False

    return True
