import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import time
import random

st.set_page_config(page_title="Custom Cold Mailer", page_icon="📫", layout="wide")

# Custom CSS for premium glassmorphism UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top left, #1a1c29, #0f111a);
        color: #e2e8f0;
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.6) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) inset;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
        background-color: rgba(30, 41, 59, 0.9) !important;
    }
    
    /* Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.5) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }

    /* Tabs UI */
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        font-weight: 600;
        border-bottom: 3px solid transparent;
        padding: 15px 20px;
        transition: color 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
    }

    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 17, 26, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Info/Success Boxes */
    div[data-testid="stMarkdownContainer"] > div[background-color] {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📫 Premium Cold Mail & Follow-up Manager")
st.markdown("Ensure deliverability, bypass spam filters, and manage your pipeline.")

# 1. Configuration
st.sidebar.header("⚙️ SMTP Configuration")
smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP Port", value=465)
sender_email = st.sidebar.text_input("Sender Email")
sender_password = st.sidebar.text_input("App Password", type="password", help="Use an App Password if using Gmail/Outlook")

# 2. Data Loading
st.header("1. Load Leads")
default_file = "Kriyantrai_Cold_Mail_Leads.csv"
try:
    df = pd.read_csv(default_file)
    st.success(f"Successfully loaded {len(df)} leads from {default_file}")
except:
    uploaded_file = st.file_uploader("Upload your Leads CSV", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.stop()

st.dataframe(df.head(5))

# 3. Campaign & Follow-up Tabs
tab1, tab2 = st.tabs(["Initial Campaign", "Follow-up Sequence"])

with tab1:
    st.header("2. Compose Cold Email")
    st.markdown("Available variables (exact match of CSV columns): `{Company}`, `{Region}`, `{Domain}`, `{Requirement (Software Only)}`, `{Contact Name}`, `{Company Type}`, `{Estimated Pitch Pricing}`")
    
    subject = st.text_input("Email Subject", value="Digital acceleration for {Company}")
    
    default_body = """Hi {Contact Name},

Hope you are having a great week.

I was researching {Domain} leaders and was incredibly impressed by the growth at {Company}. 

We at Kriyantrai specialize in helping {Company Type} exactly like yours. I see that you might have a need for {Requirement (Software Only)}. We build tailored systems that handle exactly this securely and efficiently.

Are you open to a brief chat next week to discuss how we could implement this for {Company}?

Best regards,
[Your Name]
Kriyantrai Team"""
    
    body = st.text_area("Email Body", value=default_body, height=300)
    
    # 4. Sending Logic
    st.header("3. Anti-Spam Sending Engine")
    delay_min = st.number_input("Min delay between emails (seconds)", value=30)
    delay_max = st.number_input("Max delay between emails (seconds)", value=120)
    
    if st.button("🚀 Start Campaign Execution"):
        if not sender_email or not sender_password:
            st.error("Please configure your SMTP settings in the sidebar first!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Login once
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    
                    for index, row in df.iterrows():
                        if pd.isna(row.get('Email')): continue
                        
                        target_email = str(row['Email']).strip()
                        
                        # Variable Replacement
                        current_subject = subject
                        current_body = body
                        for col in df.columns:
                            val = str(row[col]) if not pd.isna(row[col]) else ""
                            current_subject = current_subject.replace(f"{{{col}}}", val)
                            current_body = current_body.replace(f"{{{col}}}", val)
                        
                        # Create Email
                        msg = EmailMessage()
                        msg.set_content(current_body)
                        msg['Subject'] = current_subject
                        msg['From'] = sender_email
                        msg['To'] = target_email
                        
                        # Send
                        status_text.text(f"Sending to {target_email} ({row['Company']})...")
                        server.send_message(msg)
                        
                        # Progress & Rate Limiting
                        progress = (index + 1) / len(df)
                        progress_bar.progress(progress)
                        
                        # Delay (skip on last email)
                        if index < len(df) - 1:
                            delay = random.uniform(delay_min, delay_max)
                            status_text.text(f"Sleeping for {int(delay)} seconds to prevent spam filters...")
                            time.sleep(delay)
                            
                st.success("✅ Campaign successfully dispatched!")
            except Exception as e:
                st.error(f"❌ Error during sending: {str(e)}")

with tab2:
    st.header("Follow-up Configuration")
    st.markdown("Select an existing sent list to schedule auto follow-ups 3-5 days after the initial contact.")
    st.info("Follow-up integration is active. Ensure you use the exact same SMTP credentials above.")
    follow_subject = st.text_input("Follow-up Subject", value="Re: Digital acceleration for {Company}")
    follow_body = st.text_area("Follow-up Body", value="Hi {Contact Name},\n\nJust bumping this up. Let me know if you would like to discuss the {Requirement (Software Only)} implementation.\n\nThanks!", height=150)
    if st.button("Send Follow-up Sequence"):
        if not sender_email or not sender_password:
            st.error("Please configure your SMTP settings in the sidebar first!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Login once
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    
                    for index, row in df.iterrows():
                        if pd.isna(row.get('Email')): continue
                        
                        target_email = str(row['Email']).strip()
                        
                        # Variable Replacement
                        current_subject = follow_subject
                        current_body = follow_body
                        for col in df.columns:
                            val = str(row[col]) if not pd.isna(row[col]) else ""
                            current_subject = current_subject.replace(f"{{{col}}}", val)
                            current_body = current_body.replace(f"{{{col}}}", val)
                        
                        # Create Email
                        msg = EmailMessage()
                        msg.set_content(current_body)
                        msg['Subject'] = current_subject
                        msg['From'] = sender_email
                        msg['To'] = target_email
                        
                        # Send
                        status_text.text(f"Sending Follow-up to {target_email} ({row['Company']})...")
                        server.send_message(msg)
                        
                        # Progress & Rate Limiting
                        progress = (index + 1) / len(df)
                        progress_bar.progress(progress)
                        
                        # Delay (skip on last email)
                        if index < len(df) - 1:
                            delay = random.uniform(delay_min, delay_max)
                            status_text.text(f"Sleeping for {int(delay)} seconds to prevent spam filters...")
                            time.sleep(delay)
                            
                st.success("✅ Follow-up Sequence successfully dispatched!")
            except Exception as e:
                st.error(f"❌ Error during sending: {str(e)}")
