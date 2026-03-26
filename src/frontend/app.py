import sys
import os

# Add the project root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import streamlit as st
from src.agents.triage_agent import triage_agent
from src.services.db_service import db_service
from src.services.user_service import user_service

# --- Page Configuration ---
st.set_page_config(
    page_title="Non-Profit Triage Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown(
    """
    <style>
    /* Clean, minimal aesthetic */
    .stApp {
        background-color: #f7f9fc;
        color: #1a1a24;
    }
    .ticket-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
        border: 1px solid #eef2f6;
    }
    
    /* Clean Header Fonts */
    h1, h2, h3 {
        color: #0d1b2a;
        font-weight: 600;
    }
    
    /* Status Colors */
    .high-urgency { color: #e63946; font-weight: 600; }
    .medium-urgency { color: #f4a261; font-weight: 600; }
    .low-urgency { color: #2a9d8f; font-weight: 600; }
    
    /* Better metrics display */
    div[data-testid="stMetricValue"] {
        color: #1d3557;
        font-weight: 700;
    }
    
    /* Input and Chat Bubbles */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Non-Profit Triage AI Assistant")
st.markdown("Automate incoming donor and beneficiary queries using Large Language Models to detect intent, flag urgency, and draft context-aware responses.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("✅ LLM (Gemini) Connected")
    st.success("✅ Database (MongoDB) Online")
    st.markdown("---")
    st.header("About")
    st.markdown(
        "This agent automatically categorizes incoming messages "
        "and extracts Named Entities (NER) before saving them to the database."
    )

# --- Authentication State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if not st.session_state.authenticated:
    st.markdown("## Please Login to Continue")
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if user_service.verify_user(login_email, login_password):
                    st.session_state.authenticated = True
                    st.session_state.user_email = login_email
                    st.session_state.messages = [] # Clear messages on login
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
    with tab2:
        with st.form("signup_form"):
            st.subheader("Create an Account")
            signup_email = st.text_input("Email")
            signup_password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                if user_service.create_user(signup_email, signup_password):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Email already exists or error creating account.")
                    
    with tab3:
        with st.form("forgot_password_form"):
            st.subheader("Reset Password")
            reset_email = st.text_input("Email")
            reset_new_password = st.text_input("New Password", type="password")
            submitted = st.form_submit_button("Reset Password")
            if submitted:
                if user_service.reset_password(reset_email, reset_new_password):
                    st.success("Password reset successfully! Please log in with your new password.")
                else:
                    st.error("Email not found. Please check your email or sign up.")

else:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_email}")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.session_state.messages = [] # Clear messages on logout
        st.rerun()

    # --- Chat Interface ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history (only the user messages and raw drafts for a clean look)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Main Input ---
    if prompt := st.chat_input("Enter donor/beneficiary message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process Message
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 Analyzing intent and extracting data..."):
                try:
                    # 1. Call Agent to Process Message
                    ticket = triage_agent.process_message(prompt)
                    
                    # 1b. Fallback to logged in user email if none was provided in the message
                    if not ticket.email_or_contact:
                        ticket.email_or_contact = st.session_state.user_email
                    
                    # 2. Save to DB
                    ticket_id = db_service.save_ticket(ticket)
                    
                    # --- Display Results UI ---
                    st.success("Message processed successfully!")
                    
                    # Setup urgency color
                    urgency_class = f"{ticket.urgency.lower()}-urgency"
                    status_icon = "🟢" if ticket.status == "auto-resolved" else "🔴"

                    st.markdown(f'<div class="ticket-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Ticket ID", str(ticket_id)[-6:])
                    col2.metric("Urgency", ticket.urgency.upper())
                    col3.metric("Status", f"{status_icon} {ticket.status.upper()}")
                    
                    st.markdown("### 📋 Extracted Data")
                    col_dr1, col_dr2 = st.columns(2)
                    with col_dr1:
                        st.markdown(f"**👤 Name:** {ticket.name or 'N/A'}")
                        st.markdown(f"**📧 Contact:** {ticket.email_or_contact or 'N/A'}")
                    with col_dr2:
                        st.markdown(f"**📅 Date:** {ticket.date or 'N/A'}")
                        st.markdown(f"**💰 Amount:** {ticket.amount or 'N/A'}")

                    st.markdown("---")
                    st.markdown("### ✍️ Drafted Response")
                    st.info(ticket.draft_response)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add agent response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": f"**Drafted Response:**\n\n{ticket.draft_response}"})

                except Exception as e:
                    st.error(f"Error processing message: {str(e)}")
