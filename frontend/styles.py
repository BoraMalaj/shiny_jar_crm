# frontend/styles.py - CENTRALIZED STYLING
import streamlit as st

def apply_global_styles():
    """Apply beautiful global styles to the app"""
    # st.markdown("""
    # <style>
    # /* ====== ROOT VARIABLES ====== */
    # :root {
    #     --primary: #8B5CF6;
    #     --primary-dark: #7C3AED;
    #     --primary-light: #A78BFA;
    #     --secondary: #10B981;
    #     --accent: #F59E0B;
    #     --danger: #EF4444;
    #     --warning: #F59E0B;
    #     --success: #10B981;
    #     --info: #3B82F6;
    #     --background: #F8FAFC;
    #     --card-bg: #FFFFFF;
    #     --text-primary: #1E293B;
    #     --text-secondary: #64748B;
    #     --border: #E2E8F0;
    #     --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    #     --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    #     --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    #     --radius: 12px;
    # }
    
    # /* ====== MAIN APP STYLING ====== */
    # .stApp {
    #     background: var(--background) !important;
    #     font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    # }
    
    # /* ====== HEADERS ====== */
    # .main-header {
    #     font-size: 2.8rem !important;
    #     background: linear-gradient(135deg, var(--primary) 0%, #6366F1 100%) !important;
    #     -webkit-background-clip: text !important;
    #     -webkit-text-fill-color: transparent !important;
    #     text-align: center !important;
    #     margin-bottom: 2rem !important;
    #     font-weight: 800 !important;
    #     padding: 10px 0 !important;
    #     letter-spacing: -0.5px !important;
    # }
    
    # h1, h2, h3 {
    #     color: var(--text-primary) !important;
    #     font-weight: 700 !important;
    # }
    
    # /* ====== SIDEBAR ====== */
    # [data-testid="stSidebar"] {
    #     background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    #     border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    # }
    
    # [data-testid="stSidebar"] * {
    #     color: white !important;
    # }
    
    # [data-testid="stSidebar"] .stRadio > div {
    #     background: rgba(255, 255, 255, 0.1) !important;
    #     backdrop-filter: blur(10px) !important;
    #     padding: 8px 12px !important;
    #     border-radius: var(--radius) !important;
    #     margin: 6px 0 !important;
    #     border: 1px solid rgba(255, 255, 255, 0.2) !important;
    #     transition: all 0.3s ease !important;
    # }
    
    # [data-testid="stSidebar"] .stRadio > div:hover {
    #     background: rgba(255, 255, 255, 0.15) !important;
    #     transform: translateX(5px) !important;
    # }
    
    # [data-testid="stSidebar"] .stRadio label {
    #     font-weight: 500 !important;
    #     padding: 8px !important;
    #     width: 100% !important;
    # }
    
    # [data-testid="stSidebar"] .stRadio input:checked + label {
    #     background: white !important;
    #     color: var(--primary) !important;
    #     border-radius: 8px !important;
    #     font-weight: 600 !important;
    # }
    
    # /* ====== METRIC CARDS ====== */
    # .metric-card {
    #     background: var(--card-bg) !important;
    #     padding: 25px !important;
    #     border-radius: var(--radius) !important;
    #     box-shadow: var(--shadow) !important;
    #     border-left: 5px solid var(--primary) !important;
    #     transition: all 0.3s ease !important;
    #     text-align: center !important;
    # }
    
    # .metric-card:hover {
    #     transform: translateY(-5px) !important;
    #     box-shadow: var(--shadow-lg) !important;
    #     border-left-color: var(--secondary) !important;
    # }
    
    # /* ====== BUTTONS ====== */
    # .stButton > button {
    #     background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    #     color: white !important;
    #     border: none !important;
    #     border-radius: var(--radius) !important;
    #     padding: 12px 24px !important;
    #     font-weight: 600 !important;
    #     transition: all 0.3s ease !important;
    #     box-shadow: var(--shadow) !important;
    # }
    
    # .stButton > button:hover {
    #     transform: translateY(-2px) !important;
    #     box-shadow: var(--shadow-lg) !important;
    #     background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%) !important;
    # }
    
    # /* ====== DATA TABLES ====== */
    # .stDataFrame {
    #     border-radius: var(--radius) !important;
    #     overflow: hidden !important;
    #     box-shadow: var(--shadow) !important;
    #     border: 1px solid var(--border) !important;
    # }
    
    # /* ====== TABS ====== */
    # .stTabs [data-baseweb="tab-list"] {
    #     gap: 8px !important;
    #     padding: 8px !important;
    #     background: var(--card-bg) !important;
    #     border-radius: var(--radius) !important;
    #     box-shadow: var(--shadow-sm) !important;
    # }
    
    # .stTabs [data-baseweb="tab"] {
    #     border-radius: 8px !important;
    #     padding: 12px 24px !important;
    #     background: transparent !important;
    #     color: var(--text-secondary) !important;
    #     font-weight: 500 !important;
    #     transition: all 0.3s ease !important;
    # }
    
    # .stTabs [data-baseweb="tab"]:hover {
    #     background: rgba(139, 92, 246, 0.1) !important;
    #     color: var(--primary) !important;
    # }
    
    # .stTabs [aria-selected="true"] {
    #     background: var(--primary) !important;
    #     color: white !important;
    #     font-weight: 600 !important;
    #     box-shadow: var(--shadow) !important;
    # }
    
    # /* ====== FORMS ====== */
    # .stTextInput input, .stTextArea textarea, .stSelectbox select {
    #     border: 2px solid var(--border) !important;
    #     border-radius: var(--radius) !important;
    #     padding: 12px 16px !important;
    #     font-size: 1rem !important;
    #     transition: all 0.3s ease !important;
    # }
    
    # .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
    #     border-color: var(--primary) !important;
    #     box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    #     outline: none !important;
    # }
    
    # /* ====== CARDS ====== */
    # .custom-card {
    #     background: var(--card-bg) !important;
    #     padding: 24px !important;
    #     border-radius: var(--radius) !important;
    #     box-shadow: var(--shadow) !important;
    #     border: 1px solid var(--border) !important;
    #     margin-bottom: 16px !important;
    # }
    
    # /* ====== STATUS BADGES ====== */
    # .status-success {
    #     background: linear-gradient(135deg, var(--success) 0%, #059669 100%) !important;
    #     color: white !important;
    #     padding: 6px 12px !important;
    #     border-radius: 20px !important;
    #     font-size: 0.85rem !important;
    #     font-weight: 600 !important;
    #     display: inline-block !important;
    # }
    
    # .status-warning {
    #     background: linear-gradient(135deg, var(--warning) 0%, #D97706 100%) !important;
    #     color: white !important;
    #     padding: 6px 12px !important;
    #     border-radius: 20px !important;
    #     font-size: 0.85rem !important;
    #     font-weight: 600 !important;
    #     display: inline-block !important;
    # }
    
    # .status-danger {
    #     background: linear-gradient(135deg, var(--danger) 0%, #DC2626 100%) !important;
    #     color: white !important;
    #     padding: 6px 12px !important;
    #     border-radius: 20px !important;
    #     font-size: 0.85rem !important;
    #     font-weight: 600 !important;
    #     display: inline-block !important;
    # }
    
    # /* ====== LOADING SPINNER ====== */
    # .stSpinner > div {
    #     border-color: var(--primary) !important;
    #     border-right-color: transparent !important;
    # }
    
    # /* ====== CUSTOM DIVIDERS ====== */
    # .divider {
    #     height: 1px !important;
    #     background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
    #     margin: 2rem 0 !important;
    # }
    
    # /* ====== SCROLLBAR ====== */
    # ::-webkit-scrollbar {
    #     width: 8px !important;
    #     height: 8px !important;
    # }
    
    # ::-webkit-scrollbar-track {
    #     background: var(--background) !important;
    #     border-radius: 4px !important;
    # }
    
    # ::-webkit-scrollbar-thumb {
    #     background: var(--primary-light) !important;
    #     border-radius: 4px !important;
    # }
    
    # ::-webkit-scrollbar-thumb:hover {
    #     background: var(--primary) !important;
    # }
    
    # /* ====== FOOTER ====== */
    # .app-footer {
    #     text-align: center !important;
    #     color: var(--text-secondary) !important;
    #     font-size: 0.9rem !important;
    #     margin-top: 3rem !important;
    #     padding-top: 1.5rem !important;
    #     border-top: 1px solid var(--border) !important;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    """Apply modern dark theme styles"""
    st.markdown("""
    <style>
    /* ====== DARK THEME VARIABLES ====== */
    :root {
        --primary: #8B5CF6;
        --primary-dark: #7C3AED;
        --secondary: #10B981;
        --accent: #F59E0B;
        --danger: #EF4444;
        --success: #10B981;
        --info: #3B82F6;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --border: #334155;
        --radius: 12px;
    }
    
    /* ====== MAIN APP BACKGROUND ====== */
    .stApp {
        background: var(--bg-dark) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ====== HEADERS ====== */
    .main-header {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid var(--border) !important;
    }
    
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    /* ====== SIDEBAR ====== */
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 39, 0.95) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* ====== BUTTONS ====== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* ====== METRIC CARDS ====== */
    .metric-card {
        background: var(--bg-card) !important;
        padding: 1.5rem !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        text-align: center !important;
    }
    
    /* ====== DATA TABLES ====== */
    .stDataFrame {
        background: var(--bg-card) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
    }
    
    /* ====== TABS ====== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card) !important;
        padding: 0.5rem !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* ====== INPUT FIELDS ====== */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: var(--bg-card) !important;
        border: 2px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius) !important;
    }
    
    /* ====== STATUS BADGES ====== */
    .status-badge {
        padding: 0.25rem 0.75rem !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    
    .status-success {
        background: rgba(16, 185, 129, 0.2) !important;
        color: #10B981 !important;
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2) !important;
        color: #F59E0B !important;
    }
    
    /* ====== API STATUS ====== */
    .api-connected {
        background: rgba(16, 185, 129, 0.1) !important;
        color: #10B981 !important;
        padding: 0.75rem !important;
        border-radius: var(--radius) !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }
    
    .api-disconnected {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #EF4444 !important;
        padding: 0.75rem !important;
        border-radius: var(--radius) !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    /* ====== DIVIDER ====== */
    .divider {
        height: 1px !important;
        background: var(--border) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* ====== HIDE STREAMLIT BRANDING ====== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)