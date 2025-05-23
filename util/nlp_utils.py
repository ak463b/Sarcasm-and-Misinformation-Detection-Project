import streamlit as st
import sqlite3
import datetime # To get current timestamp
import json

# Database file path for feedback
# It's good practice to keep feedback in a separate DB file or table from users.
FEEDBACK_DB_FILE = "feedback.db"

def init_db_feedback():
    """
    Initializes the SQLite database for feedback and creates the necessary tables
    if they don't exist.
    - 'general_feedback' table for general user comments.
    - 'nlp_feedback' table for NLP analysis results.
    """
    conn = sqlite3.connect(FEEDBACK_DB_FILE)
    c = conn.cursor()

    # Create general_feedback table
    c.execute('''
        CREATE TABLE IF NOT EXISTS general_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            feedback TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Create nlp_feedback table
    c.execute('''
        CREATE TABLE IF NOT EXISTS nlp_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            input_text TEXT,
            cleaned_text TEXT,
            pos_tags_json TEXT,  -- Storing JSON string for complex data
            sentiment_json TEXT, -- Storing JSON string for complex data
            topics_json TEXT,    -- Storing JSON string for complex data
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the feedback database when this module is imported
init_db_feedback()

def save_feedback(user, feedback_text):
    """
    Saves user feedback to the SQLite database.

    Args:
        user (str): The username of the feedback submitter.
        feedback_text (str): The feedback message.
    """
    if not feedback_text.strip():
        st.warning("Feedback cannot be empty.")
        return

    conn = sqlite3.connect(FEEDBACK_DB_FILE)
    c = conn.cursor()
    try:
        timestamp = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO general_feedback (username, feedback, timestamp) VALUES (?, ?, ?)",
                  (user, feedback_text, timestamp))
        conn.commit()
        # st.success("Feedback saved successfully!") # Displayed in app.py
    except sqlite3.Error as e:
        st.error(f"Error saving general feedback to database: {e}")
    finally:
        conn.close()

def save_nlp_feedback(user, input_text, cleaned_text, pos_tags_data, sentiment_data, topic_data):
    """
    Saves NLP analysis results as feedback to the SQLite database.

    Args:
        user (str): The username of the submitter.
        input_text (str): The original input text.
        cleaned_text (str): The preprocessed text.
        pos_tags_data (list): Part-of-speech tags.
        sentiment_data (dict): Sentiment analysis results.
        topic_data (list): Topic modeling results.
    """
    if not input_text.strip():
        st.warning("Cannot save NLP feedback for empty input text.")
        return

    conn = sqlite3.connect(FEEDBACK_DB_FILE)
    c = conn.cursor()
    try:
        timestamp = datetime.datetime.now().isoformat()
        
        # Convert complex Python objects to JSON strings for SQLite storage
        pos_tags_json = json.dumps(pos_tags_data)
        sentiment_json = json.dumps(sentiment_data)
        topics_json = json.dumps(topic_data)

        c.execute(
            "INSERT INTO nlp_feedback (username, input_text, cleaned_text, pos_tags_json, sentiment_json, topics_json, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user, input_text, cleaned_text, pos_tags_json, sentiment_json, topics_json, timestamp)
        )
        conn.commit()
        # st.success("NLP Feedback saved successfully!") # Displayed in app.py
    except sqlite3.Error as e:
        st.error(f"Error saving NLP feedback to database: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while preparing NLP feedback for saving: {e}")
    finally:
        conn.close()
