import streamlit as st

def login():
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Invalid credentials.")
    return False