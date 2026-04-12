# 📫 Cold Mail Automation Manager

A premium, UI-driven cold email campaign manager built in Python and Streamlit. This tool bypasses enterprise spam filters using customized variable injection and algorithmic drip-feed pacing.

## Features
- **Dynamic Variable Injection**: Automatically customizes every email based on CSV data to bypass spam filters.
- **Glassmorphism UI**: A stunning, premium aesthetic interface for managing your campaigns.
- **Drip-Feed Pacing**: Imitates human send patterns with randomized delays.
- **Follow-up Sequence manager**: Automatically dispatches follow-ups using the exact same threads and variables.

## Getting Started

### 1. Requirements
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Setup SMTP Credentials
You need a 16-digit App Password from your email provider (like Gmail or Outlook). 
1. Go to your Google Account Security Settings.
2. Turn on 2-Step Verification.
3. Search "App Passwords" and generate a 16-digit code.

### 3. Run the App
Run the following command exactly in your terminal:
```bash
streamlit run mailer_app.py
```
The application will open immediately in your web browser. Just upload your leads CSV file, drop in your App Password, and launch your campaign!
