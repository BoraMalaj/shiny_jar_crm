import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Shiny Jar Business Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #8B5CF6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Sidebar
with st.sidebar:
    st.title("💎 Shiny Jar")
    st.markdown("---")
    
    if st.session_state.logged_in:
        st.success(f"👋 Welcome, {st.session_state.user.get('username', 'User')}")
        st.page_link("app.py", label="📊 Dashboard", icon="📊")
        st.page_link("pages/01_Dashboard.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/02_Expenses.py", label="💰 Expenses", icon="💰")
        st.page_link("pages/03_Customers.py", label="👥 Customers", icon="👥")
        st.page_link("pages/04_Analytics.py", label="📈 Analytics", icon="📈")
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Please login to continue")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                # TODO: Implement actual login
                st.session_state.logged_in = True
                st.session_state.user = {"username": username}
                st.rerun()

# Main content
if st.session_state.logged_in:
    st.markdown('<h1 class="main-header">💎 Shiny Jar Business Dashboard</h1>', unsafe_allow_html=True)
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Revenue", value="€2,450", delta="+12%")
    
    with col2:
        st.metric(label="Total Expenses", value="€890", delta="-5%")
    
    with col3:
        st.metric(label="Active Customers", value="124", delta="+8")
    
    with col4:
        st.metric(label="Inventory Items", value="89", delta="+3")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Recent Transactions")
        # Sample data - replace with API call
        transactions = pd.DataFrame({
            'Date': pd.date_range('2023-12-01', periods=10),
            'Amount': [150, 89, 45, 120, 65, 200, 85, 95, 110, 75],
            'Category': ['Materials', 'Shipping', 'Marketing', 'Materials', 'Packaging', 
                        'Sale', 'Sale', 'Sale', 'Sale', 'Sale'],
            'Type': ['expense', 'expense', 'expense', 'expense', 'expense',
                    'income', 'income', 'income', 'income', 'income']
        })
        st.dataframe(transactions, use_container_width=True)
    
    with col2:
        st.subheader("📊 Expense by Category")
        fig = px.pie(transactions[transactions['Type'] == 'expense'], 
                    values='Amount', names='Category',
                    color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add Expense", use_container_width=True):
            st.switch_page("pages/02_Expenses.py")
    
    with col2:
        if st.button("👤 Add Customer", use_container_width=True):
            st.switch_page("pages/03_Customers.py")
    
    with col3:
        if st.button("📊 View Reports", use_container_width=True):
            st.switch_page("pages/04_Analytics.py")
    
    with col4:
        if st.button("📱 Instagram Sync", use_container_width=True):
            st.info("Instagram sync coming soon!")
    
else:
    # Login page
    st.markdown('<h1 class="main-header">💎 Welcome to Shiny Jar Business Suite</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=Shiny+Jar", 
                caption="Manage your jewelry business efficiently")
        
        st.markdown("""
        ### 📋 Features
        - 💰 **Expense Tracking** - Track all business expenses
        - 👥 **Customer CRM** - Manage customer relationships
        - 📊 **Analytics** - Visualize sales and expenses
        - 📱 **Instagram Integration** - Sync with social media
        - 💎 **Inventory Management** - Track jewelry stock
        
        ### 🚀 Get Started
        1. Login with your credentials
        2. Add your first transaction
        3. Import customers from Instagram
        4. Start analyzing your business!
        """)
        
        with st.expander("Demo Credentials"):
            st.code("Username: admin\nPassword: admin123")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "💎 Shiny Jar Business Suite | Built with ❤️ for University Project"
    "</div>",
    unsafe_allow_html=True
)