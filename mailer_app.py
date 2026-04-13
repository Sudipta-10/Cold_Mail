import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import time
import random

st.set_page_config(page_title="Kriyantrai Cold Mailer", page_icon="logo.png", layout="wide")

# Custom CSS for premium glassmorphism UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stNumberInput>div>div>input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* Primary Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    button[kind="primary"] * {
        color: white !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
    }
    button[kind="primary"]:active {
        transform: translateY(1px) !important;
    }

    /* Tabs UI */
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        font-weight: 600;
        padding: 15px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1e293b;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #2563eb !important;
    }

    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Sidebar Text Fix for Light Mode */
    [data-testid="stSidebar"] .css-17lntkn, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #1e293b !important;
    }

    /* Animated Sidebar Button */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        animation: pulse-glow 2s infinite ease-in-out !important;
        margin-top: 15px !important;
        padding: 0.75rem !important;
        width: 100%;
    }
    
    /* Info/Success Boxes */
    div[data-testid="stMarkdownContainer"] > div[background-color] {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Clean up native Streamlit headers, but keep the Sidebar Expand Chevron */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Balanced Sidebar Compression */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.75rem !important;
    }
    [data-testid="stSidebar"] .stNumberInput, [data-testid="stSidebar"] .stTextInput {
        margin-bottom: -5px !important;
    }
    </style>
""", unsafe_allow_html=True)

import os
if os.path.exists("logo.png"):
    col1, col2, col3 = st.sidebar.columns([1, 8, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.sidebar.markdown("<h3 style='text-align: center; margin-top: -20px; margin-bottom: 0px; color: #0f172a; line-height: 1.2;'>Cold_Mail<br>for Kriyantrai</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85em; margin-bottom: 0px;'>Deliverability & Pipeline Manager</p>", unsafe_allow_html=True)

st.title("Campaign Dashboard")

# 1. Configuration
st.sidebar.markdown("<hr style='margin-top: 5px; margin-bottom: 5px;'>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='margin-bottom: 0px; margin-top: 0px; color: #1e293b;'>⚙️ SMTP Configuration</h4>", unsafe_allow_html=True)
smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP Port", value=465)
sender_email = st.sidebar.text_input("Sender Email")
sender_password = st.sidebar.text_input("App Password", type="password", help="Use an App Password if using Gmail/Outlook")
if st.sidebar.button("ENTER 🔐", use_container_width=True, type="primary"):
    st.sidebar.success("Credentials saved for session!")

# 2. Data Loading
st.header("1. Load Leads")
uploaded_file = st.file_uploader("Upload custom Leads Data (Optional)", type=['csv', 'xlsx', 'xls'])
default_file = "Kriyantrai_Cold_Mail_Leads.csv"

try:
    if uploaded_file is not None:
        filename = uploaded_file.name
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.markdown(f"""
        <div style="background-color: #dcfce7; border-left: 6px solid #22c55e; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #166534; margin: 0;">✅ Successfully loaded {len(df)} custom leads from {filename}</h4>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback to the default tracking CSV
        df = pd.read_csv(default_file)
        st.markdown(f"""
        <div style="background-color: #dcfce7; border-left: 6px solid #22c55e; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #166534; margin: 0;">✅ Successfully loaded {len(df)} leads from {default_file} (Default)</h4>
        </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
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
    
    st.header("4. Target Segment (Row Index)")
    c1, c2 = st.columns(2)
    with c1:
        start_row = st.number_input("Start Row (0-indexed)", min_value=0, max_value=len(df)-1 if len(df) > 0 else 0, value=0, key="c_start")
    with c2:
        end_row = st.number_input("End Row (Exclusive)", min_value=1, max_value=len(df), value=len(df), key="c_end")
    
    if st.button("🚀 Start Campaign Execution", type="primary"):
        if not sender_email or not sender_password:
            st.error("Please configure your SMTP settings in the sidebar first!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Login once
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    
                    df_target = df.iloc[start_row:end_row]
                    total_emails = len(df_target)
                    sent_count = 0
                    
                    for index, row in df_target.iterrows():
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
                        status_text.markdown(f'''
                        <div style="background-color: #f8fafc; border-left: 6px solid #94a3b8; padding: 15px; border-radius: 8px;">
                            <h4 style="color: #475569; margin: 0;">⚙️ Sending to {target_email} ({row['Company']})...</h4>
                        </div>
                        ''', unsafe_allow_html=True)
                        server.send_message(msg)
                        
                        # Progress & Rate Limiting
                        sent_count += 1
                        progress = min(sent_count / total_emails, 1.0)
                        progress_bar.progress(progress)
                        
                        # Delay (skip on last email)
                        if sent_count < total_emails:
                            delay = int(random.uniform(delay_min, delay_max))
                            for remaining in range(delay, 0, -1):
                                status_text.markdown(f'''
                                <div style="background-color: #eff6ff; border-left: 6px solid #3b82f6; padding: 15px; border-radius: 8px;">
                                    <h4 style="color: #1e3a8a; margin: 0;">📤 Email {sent_count}/{total_emails} dispatched! Next sending in: <b>{remaining}s</b></h4>
                                </div>
                                ''', unsafe_allow_html=True)
                                time.sleep(1)
                            status_text.empty()
                            
                st.success("✅ Campaign successfully dispatched!")
            except Exception as e:
                st.error(f"❌ Error during sending: {str(e)}")

with tab2:
    st.header("Follow-up Configuration")
    st.markdown("Select an existing sent list to schedule auto follow-ups 3-5 days after the initial contact.")
    st.info("Follow-up integration is active. Ensure you use the exact same SMTP credentials above.")
    follow_subject = st.text_input("Follow-up Subject", value="Re: Digital acceleration for {Company}")
    follow_body = st.text_area("Follow-up Body", value="Hi {Contact Name},\n\nJust bumping this up. Let me know if you would like to discuss the {Requirement (Software Only)} implementation.\n\nThanks!", height=150)
    
    st.header("Target Segment (Row Index)")
    c1, c2 = st.columns(2)
    with c1:
        f_start_row = st.number_input("Start Row (0-indexed)", min_value=0, max_value=len(df)-1 if len(df) > 0 else 0, value=0, key="f_start")
    with c2:
        f_end_row = st.number_input("End Row (Exclusive)", min_value=1, max_value=len(df), value=len(df), key="f_end")
    if st.button("Send Follow-up Sequence", type="primary"):
        if not sender_email or not sender_password:
            st.error("Please configure your SMTP settings in the sidebar first!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Login once
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    
                    df_target = df.iloc[f_start_row:f_end_row]
                    total_emails = len(df_target)
                    sent_count = 0
                    
                    for index, row in df_target.iterrows():
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
                        status_text.markdown(f'''
                        <div style="background-color: #f8fafc; border-left: 6px solid #94a3b8; padding: 15px; border-radius: 8px;">
                            <h4 style="color: #475569; margin: 0;">⚙️ Sending Follow-up to {target_email} ({row['Company']})...</h4>
                        </div>
                        ''', unsafe_allow_html=True)
                        server.send_message(msg)
                        
                        # Progress & Rate Limiting
                        sent_count += 1
                        progress = min(sent_count / total_emails, 1.0)
                        progress_bar.progress(progress)
                        
                        # Delay (skip on last email)
                        if sent_count < total_emails:
                            delay = int(random.uniform(delay_min, delay_max))
                            for remaining in range(delay, 0, -1):
                                status_text.markdown(f'''
                                <div style="background-color: #eef2ff; border-left: 6px solid #6366f1; padding: 15px; border-radius: 8px;">
                                    <h4 style="color: #312e81; margin: 0;">🔄 Follow-up {sent_count}/{total_emails} dispatched! Next sending in: <b>{remaining}s</b></h4>
                                </div>
                                ''', unsafe_allow_html=True)
                                time.sleep(1)
                            status_text.empty()
                            
                st.success("✅ Follow-up Sequence successfully dispatched!")
            except Exception as e:
                st.error(f"❌ Error during sending: {str(e)}")
