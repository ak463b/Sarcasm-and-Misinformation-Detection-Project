import streamlit as st
import bcrypt
import sqlite3
import os

# Database file path
DB_FILE = "users.db"

def init_db():
    """
    Initializes the SQLite database and creates the 'users' table if it doesn't exist.
    The 'users' table stores username and hashed password.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

def get_current_user():
    """
    Retrieves the username of the currently logged-in user from Streamlit's session state.

    Returns:
        str or None: The logged-in username if available, otherwise None.
    """
    return st.session_state.get("username", None)

def is_logged_in():
    """
    Checks if a user is currently logged in.

    Returns:
        bool: True if a username exists in the session state, False otherwise.
    """
    return "username" in st.session_state

def login():
    """
    Handles the user login process using a SQLite database.
    Displays input fields for username and password.
    Authenticates against the 'users' table.
    Provides a logout button if already logged in.

    Returns:
        bool: True if the user is successfully logged in (or already was), False otherwise.
    """
    st.title("🔐 Login")

    if not is_logged_in():
        user_input = st.text_input("Username", key="login_username")
        pwd_input = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if not user_input or not pwd_input:
                st.error("Please enter both username and password.")
                return False

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT hashed_password FROM users WHERE username = ?", (user_input,))
            result = c.fetchone()
            conn.close()

            if result:
                stored_hashed_password = result[0]
                if bcrypt.checkpw(pwd_input.encode('utf-8'), stored_hashed_password):
                    st.success("Logged in successfully!")
                    st.session_state["username"] = user_input
                    st.rerun() # Rerun to update UI after login
                    return True
                else:
                    st.error("Invalid credentials.")
            else:
                st.error("Invalid credentials.") # Username not found
        return False
    else:
        st.write(f"Welcome back, **{st.session_state['username']}**!")
        if st.button("Logout", key="logout_button_main"):
            logout() # Call the separate logout function
            st.rerun() # Rerun to update UI after logout
        return True

def logout():
    """
    Logs out the current user by removing their username from Streamlit's session state.
    """
    if "username" in st.session_state:
        del st.session_state["username"]
        st.success("Logged out successfully.")
    else:
        st.warning("No user was logged in.")

def signup():
    """
    Handles user registration using a SQLite database.
    Allows users to create a new account with a username and password.
    Stores hashed password in the 'users' table.
    """
    st.title("📝 Sign Up")

    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Register", key="register_button"):
        if not new_username or not new_password or not confirm_password:
            st.error("Please fill in all fields.")
            return False
        
        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return False
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Check if username already exists
        c.execute("SELECT id FROM users WHERE username = ?", (new_username,))
        if c.fetchone():
            st.error(f"Username '{new_username}' already exists. Please choose a different one.")
            conn.close()
            return False

        # Hash the password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Insert new user into the database
            c.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", 
                      (new_username, hashed_password))
            conn.commit()
            st.success(f"User '{new_username}' registered successfully!")
            st.info("You can now log in.")
            st.rerun() # Rerun to clear form and potentially redirect to login
            return True
        except sqlite3.Error as e:
            st.error(f"Error registering user: {e}")
            return False
        finally:
            conn.close()
    return False
