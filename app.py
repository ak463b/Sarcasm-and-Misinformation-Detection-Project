import streamlit as st
from util.auth import login
from util.models_utils import load_models, predict_text
from util.reddit_utils import fetch_reddit_posts
from util.feedback import save_feedback

st.set_page_config(page_title="Sarcasm & Misinformation Detector", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
        .main { background-color: #F8F9FA; }
        .title { font-size:36px; font-weight:700; color:#343A40; }
        .subtitle { font-size:20px; font-weight:500; color:#495057; }
        .footer { font-size:14px; color:gray; text-align:center; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login
if not st.session_state.logged_in:
    st.session_state.logged_in = login()

if st.session_state.logged_in:
    st.markdown('<p class="title">🧠 Disentangling Sarcasm & Misinformation</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-powered text analysis with XGBoost + Reddit Live + Feedback</p>', unsafe_allow_html=True)
    
    st.sidebar.title("🔍 Navigation")
    option = st.sidebar.radio("Go to", ["🏠 Home", "📄 Detect Text", "🌐 Reddit Live", "📝 Feedback"])

    # Load models
    mis_model, mis_vectorizer, sar_model, sar_vectorizer = load_models()

    if option == "🏠 Home":
        st.image("https://cdn.pixabay.com/photo/2020/06/12/23/50/coding-5288078_1280.png", use_column_width=True)
        st.markdown("""
            Welcome to the **Sarcasm & Misinformation Detector** app!  
            👉 Detect fake news and sarcasm in text using powerful ML models.  
            👉 Analyze live Reddit posts.  
            👉 Share your feedback for continuous improvement.
        """)

    elif option == "📄 Detect Text":
        st.subheader("📑 Analyze Custom Text")
        user_input = st.text_area("✏️ Enter or paste your sentence for analysis", height=150)

        if st.button("🔍 Analyze"):
            if user_input.strip():
                with st.spinner("Analyzing..."):
                    mis_pred, sar_pred = predict_text(user_input, mis_model, mis_vectorizer, sar_model, sar_vectorizer)
                st.success(f"Misinformation: {'✅ Real' if mis_pred==0 else '❌ Fake'}")
                st.success(f"Sarcasm: {'😐 Not Sarcastic' if sar_pred==0 else '😏 Sarcastic'}")
            else:
                st.warning("Please enter some text!")

    elif option == "🌐 Reddit Live":
        st.subheader("🔎 Analyze Live Reddit Posts")
        topic = st.text_input("Enter a Reddit keyword (e.g., news, politics, science)")

        if st.button("🚀 Fetch & Analyze"):
            if topic.strip():
                with st.spinner("Fetching posts from Reddit..."):
                    posts = fetch_reddit_posts(topic)
                for post in posts:
                    st.markdown(f"**📝 Title:** {post['title']}")
                    mis_pred, sar_pred = predict_text(post['title'], mis_model, mis_vectorizer, sar_model, sar_vectorizer)
                    st.markdown(f"- Misinformation: {'✅ Real' if mis_pred==0 else '❌ Fake'}")
                    st.markdown(f"- Sarcasm: {'😐 Not Sarcastic' if sar_pred==0 else '😏 Sarcastic'}")
                    st.markdown("---")
            else:
                st.warning("Please enter a topic!")

    elif option == "📝 Feedback":
        st.subheader("💬 We’d love your Feedback!")
        name = st.text_input("👤 Your Name")
        comment = st.text_area("✉️ Your Feedback", height=100)
        if st.button("✅ Submit Feedback"):
            if name and comment:
                save_feedback(name, comment)
                st.success("🎉 Thank you for your feedback!")
            else:
                st.warning("Please fill in both fields before submitting.")

    st.markdown('<div class="footer">Built with ❤️ using Streamlit and XGBoost</div>', unsafe_allow_html=True)