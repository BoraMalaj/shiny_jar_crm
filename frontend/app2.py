# frontend/app.py - UPDATED WITH PROPER COLORS
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta
from styles import apply_global_styles
from pages.customer_dashboard import show_customer_dashboard
from pages.supplier_dashboard import show_supplier_dashboard

# Page config MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Shiny Jar Business Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/shiny-jar',
        'Report a bug': None,
        'About': "# Shiny Jar CRM\nA complete business management system"
    }
)

# Import auth
try:
    from auth import auth, show_login_page
    AUTH_AVAILABLE = True
except ImportError as e:
    st.error(f"Auth module error: {e}")
    AUTH_AVAILABLE = False
    # Create simple fallback
    auth = type('obj', (object,), {
        'is_authenticated': lambda: True,
        'get_user_role': lambda: 'admin',
        'get_username': lambda: 'Demo',
        'has_role': lambda x: True,
        'logout': lambda: None
    })()
    show_login_page = lambda: st.info("Login")

# CUSTOM CSS - FIXED COLORS TO MATCH SHINY JAR BRAND
# st.markdown("""
# <style>
#     /* Main colors: Purple theme matching Shiny Jar */
#     :root {
#         --primary: #8B5CF6;
#         --primary-dark: #7C3AED;
#         --primary-light: #A78BFA;
#         --secondary: #10B981;
#         --accent: #F59E0B;
#         --background: #F9FAFB;
#         --text: #1F2937;
#     }
    
#     /* Main header */
#     .main-header {
#         font-size: 2.8rem;
#         background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center;
#         margin-bottom: 2rem;
#         font-weight: 800;
#         padding: 10px 0;
#     }
    
#     /* Metric cards */
#     .metric-card {
#         background: white;
#         padding: 25px;
#         border-radius: 15px;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#         border-left: 5px solid #8B5CF6;
#         transition: transform 0.3s ease;
#     }
    
#     .metric-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
#     }
    
#     /* Sidebar styling */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #8B5CF6 0%, #7C3AED 100%) !important;
#         color: white !important;
#     }
    
#     [data-testid="stSidebar"] .stRadio > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         padding: 10px !important;
#         border-radius: 10px !important;
#         margin: 8px 0 !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     [data-testid="stSidebar"] .stRadio label {
#         color: white !important;
#         font-weight: 500 !important;
#     }
    
#     [data-testid="stSidebar"] .stRadio input:checked + label {
#         color: #8B5CF6 !important;
#         background: white !important;
#         border-radius: 8px !important;
#         padding: 5px 10px !important;
#     }
    
#     /* Buttons */
#     .stButton > button {
#         background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 10px !important;
#         padding: 10px 20px !important;
#         font-weight: 600 !important;
#         transition: all 0.3s ease !important;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3) !important;
#     }
    
#     /* Dataframes */
#     .stDataFrame {
#         border-radius: 10px !important;
#         overflow: hidden !important;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
#     }
    
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 10px 10px 0 0 !important;
#         padding: 12px 24px !important;
#         background: #F3F4F6 !important;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background: #8B5CF6 !important;
#         color: white !important;
#     }
    
#     /* Custom success/error */
#     .stSuccess {
#         background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
#         color: white !important;
#         border-radius: 10px !important;
#         padding: 20px !important;
#     }
    
#     .stError {
#         background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
#         color: white !important;
#         border-radius: 10px !important;
#         padding: 20px !important;
#     }
    
#     /* Custom info boxes */
#     .custom-info {
#         background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
#         color: white !important;
#         padding: 20px !important;
#         border-radius: 15px !important;
#         border-left: 5px solid #1D4ED8 !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

# Import page functions
try:
    from pages.budget import show_budget_page
    from pages.suppliers import show_suppliers_page
    from pages.analytics import show_analytics_page
    from pages.reports import show_reports_page
    PAGES_AVAILABLE = True
except ImportError as e:
    st.warning(f"Some pages not available: {e}")
    PAGES_AVAILABLE = False
    
    # Dummy functions
    def show_budget_page(): st.info("💰 Budget Management")
    def show_suppliers_page(): st.info("🏭 Supplier Management")
    def show_analytics_page(): st.info("📈 Advanced Analytics")
    def show_reports_page(): st.info("📊 Professional Reports")

# Your existing page functions (simplified for testing)
def show_dashboard():
    st.markdown('<h1 class="main-header">📊 Business Dashboard</h1>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", "€2,450", "+12%", delta_color="normal")
    
    with col2:
        st.metric("📉 Total Expenses", "€890", "-5%", delta_color="inverse")
    
    with col3:
        st.metric("👥 Active Customers", "124", "+8")
    
    with col4:
        st.metric("💎 Net Profit", "€1,560", "+15%", delta_color="normal")
    
    st.divider()
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    
    transactions = pd.DataFrame({
        'Date': ['2024-12-10 14:30', '2024-12-10 11:15', '2024-12-09 16:45', '2024-12-09 09:20'],
        'Type': ['💰 Income', '💰 Income', '📦 Expense', '💰 Income'],
        'Description': ['Necklace Sale', 'Earrings Sale', 'Material Purchase', 'Custom Order'],
        'Amount': ['€89.00', '€45.50', '€-120.00', '€200.00'],
        'Status': ['Completed', 'Completed', 'Pending', 'Completed']
    })
    
    st.dataframe(transactions, use_container_width=True, hide_index=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add Transaction", use_container_width=True):
            st.success("Add transaction clicked!")
    
    with col2:
        if st.button("👤 Add Customer", use_container_width=True):
            st.success("Add customer clicked!")
    
    with col3:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    
    with col4:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

def show_expenses_page():
    st.markdown('<h1 class="main-header">💰 Expense & Income Management</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-info">Track all your business transactions in one place</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Transaction", "📋 View All", "📈 Statistics"])
    
    with tab1:
        with st.form("add_transaction"):
            col1, col2 = st.columns(2)
            with col1:
                type = st.selectbox("Type", ["Expense", "Income"])
                amount = st.number_input("Amount (€)", min_value=0.01, value=50.0)
            with col2:
                category = st.selectbox("Category", ["Materials", "Shipping", "Sales", "Other"])
                description = st.text_input("Description")
            
            if st.form_submit_button("Add Transaction", type="primary"):
                st.success(f"✅ Added {type}: €{amount} for {category}")
    
    with tab2:
        st.info("Transaction history would appear here")
    
    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", "€2,450")
        with col2:
            st.metric("Total Expenses", "€890")
        with col3:
            st.metric("Net", "€1,560")

def show_customers_page():
    st.markdown('<h1 class="main-header">👥 Customer Relationship Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 All Customers", "➕ Add Customer", "📊 Insights"])
    
    with tab1:
        customers = pd.DataFrame({
            'Name': ['Maria Silva', 'John Doe', 'Anna Smith', 'Luca Rossi'],
            'Email': ['maria@email.com', 'john@email.com', 'anna@email.com', 'luca@email.com'],
            'Instagram': ['@maria_silva', '@john_jewelry', '@anna_sparkle', '@luca_designs'],
            'Total Spent': ['€1,250.75', '€890.50', '€2,100.00', '€750.25'],
            'Last Purchase': ['2024-12-10', '2024-12-05', '2024-12-01', '2024-11-28']
        })
        
        st.dataframe(customers, use_container_width=True, hide_index=True)
    
    with tab2:
        with st.form("add_customer"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            instagram = st.text_input("Instagram Handle")
            
            if st.form_submit_button("Add Customer"):
                st.success(f"✅ Added customer: {name}")
    
    with tab3:
        st.subheader("Customer Insights")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Customers", "124")
        with col2:
            st.metric("Avg. Spend", "€189.50")
        with col3:
            st.metric("New This Month", "8")

# MAIN APP FUNCTION
def main_app():
    """Main application after login"""
    # Apply global styles FIRST
    apply_global_styles()
    
    # Get user role
    user_role = auth.get_user_role() if AUTH_AVAILABLE else "admin"
    
    # Sidebar
    with st.sidebar:
        # st.markdown("""
        # <div style="text-align: center; padding: 20px 0;">
        #     <h1 style="color: white; font-size: 2.5rem;">💎</h1>
        #     <h2 style="color: white; margin: 0;">Shiny Jar</h2>
        #     <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Business Suite</p>
        # </div>
        # """, unsafe_allow_html=True)
        
        # st.divider()
        
        # User info
        if AUTH_AVAILABLE:
            st.markdown(f"**👤 {auth.get_username()}**")
            st.markdown(f"**Role:** {auth.get_user_role().title()}")
            
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                auth.logout()
                st.rerun()
        else:
            st.markdown("**👤 Demo User**")
            st.markdown("**Role:** Administrator")
        
        st.divider()
        
        # API Status
        try:
            health = requests.get(f"{st.session_state.api_url}/health", timeout=2)
            if health.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.warning("🌐 API Not Connected")
        
        st.divider()
        
        # Navigation
        st.markdown("### 📱 Navigation")
        
        if AUTH_AVAILABLE and auth.has_role(['admin', 'manager']):
            page_options = ["Dashboard", "Expenses", "Customers", "Suppliers", "Budget", "Analytics", "Reports"]
        elif AUTH_AVAILABLE and auth.has_role('supplier'):
            page_options = ["Dashboard", "My Supplies", "My Profile"]
        elif AUTH_AVAILABLE and auth.has_role('customer'):
            page_options = ["Dashboard", "My Orders", "My Profile"]
        else:
            page_options = ["Dashboard", "Expenses", "Customers", "Suppliers", "Budget", "Analytics", "Reports"]
        
        page = st.radio(
            "Choose page:",
            page_options,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # API URL input (hidden by default)
        with st.expander("⚙️ Settings"):
            new_url = st.text_input("API URL", value=st.session_state.api_url)
            if new_url != st.session_state.api_url:
                st.session_state.api_url = new_url
                st.rerun()
    
    # Page routing
    if page == "Dashboard":
        show_dashboard()
    elif page == "Expenses":
        show_expenses_page()
    elif page == "Customers":
        show_customers_page()
    elif page == "Suppliers" and PAGES_AVAILABLE:
        show_suppliers_page()
    elif page == "Budget" and PAGES_AVAILABLE:
        show_budget_page()
    elif page == "Analytics" and PAGES_AVAILABLE:
        show_analytics_page()
    elif page == "Reports" and PAGES_AVAILABLE:
        show_reports_page()
    elif page == "My Orders":
        st.markdown('<h1 class="main-header">🛍️ My Orders</h1>', unsafe_allow_html=True)
        st.info("Your order history will appear here")
    elif page == "My Profile":
        st.markdown('<h1 class="main-header">👤 My Profile</h1>', unsafe_allow_html=True)
        st.info("Your profile information will appear here")
    elif page == "My Supplies":
        st.markdown('<h1 class="main-header">📦 My Supplies</h1>', unsafe_allow_html=True)
        st.info("Your supply orders will appear here")
    else:
        st.error("Page not available")

# MAIN EXECUTION
if __name__ == "__main__":
    # Check authentication
    if AUTH_AVAILABLE and not auth.is_authenticated():
        show_login_page()
    else:
        main_app()




import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta
import time
# from pages.budget import show_budget_page
# from pages.suppliers import show_suppliers_page
# from pages.reports import show_reports_page
# from pages.analytics import show_analytics_page
from auth import auth, show_login_page

# Page config MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Shiny Jar Business Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import auth, but provide fallback
try:
    from auth import auth, show_login_page
    AUTH_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Auth module not available: {e}")
    AUTH_AVAILABLE = False
    
    # Create dummy auth class
    class DummyAuth:
        def __init__(self):
            if 'token' not in st.session_state:
                st.session_state.token = "demo_token"
            if 'user' not in st.session_state:
                st.session_state.user = {"username": "demo", "role": "admin"}
            if 'role' not in st.session_state:
                st.session_state.role = "admin"
        
        def is_authenticated(self):
            return True
        
        def get_user_role(self):
            return st.session_state.role
        
        def get_username(self):
            return st.session_state.user.get("username", "demo")
        
        def has_role(self, roles):
            return True
        
        def get_auth_header(self):
            return {}
    
    auth = DummyAuth()
    show_login_page = lambda: st.info("🔐 Login system would appear here")

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
    }
    .stSidebar {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stSidebar .stRadio > div {
        background: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Import page functions (make sure these exist)
try:
    from pages.budget import show_budget_page
    from pages.suppliers import show_suppliers_page
    from pages.analytics import show_analytics_page
    from pages.reports import show_reports_page
    PAGES_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Some page modules not available: {e}")
    PAGES_AVAILABLE = False
    
    # Create dummy functions for missing pages
    def show_budget_page():
        st.info("💰 Budget page - Module not loaded")
    
    def show_suppliers_page():
        st.info("🏭 Suppliers page - Module not loaded")
    
    def show_analytics_page():
        st.info("📈 Analytics page - Module not loaded")
    
    def show_reports_page():
        st.info("📊 Reports page - Module not loaded")

# Initialize session state for API URL if not exists
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

############################# Wrapping the app in authetication check ###############################

# MAIN APP LOGIC
def main():
    # Check authentication
    if AUTH_AVAILABLE and not auth.is_authenticated():
        show_login_page()
        return
    
    # Initialize session state for API URL if not exists
    if 'api_url' not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"
    
    # Sidebar
    with st.sidebar:
        st.title("💎 Shiny Jar")
        st.markdown("---")
        
        # User info
        if AUTH_AVAILABLE:
            st.markdown(f"**👤 {auth.get_username()}**")
            st.markdown(f"**Role:** {auth.get_user_role()}")
            
            if st.button("🚪 Logout", use_container_width=True):
                auth.logout()
        else:
            st.markdown("**👤 Demo User (Admin)**")
            st.markdown("**Role:** Administrator")
        
        st.markdown("---")
        
        # API Status
        try:
            health = requests.get(f"{st.session_state.api_url}/health", timeout=2)
            if health.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Unavailable")
        
        st.markdown("---")
        
        # Navigation based on role
        if AUTH_AVAILABLE and auth.has_role(['admin', 'manager']):
            pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Budget", "Analytics", "Reports"]
        elif AUTH_AVAILABLE and auth.has_role('supplier'):
            pages = ["Dashboard", "My Orders", "My Profile"]
        elif AUTH_AVAILABLE and auth.has_role('customer'):
            pages = ["Dashboard", "My Orders", "My Profile"]
        else:
            # Default full access for demo
            pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Budget", "Analytics", "Reports"]
        
        page = st.radio("Navigation", pages)
        
        st.markdown("---")
        st.caption(f"Backend: {st.session_state.api_url}")


    # Real Dashboard with data from our docker database
    if page == "Dashboard":
        st.markdown('<h1 class="main-header">📊 Shiny Jar Dashboard</h1>', unsafe_allow_html=True)
        
        try:
            # Fetch dashboard data
            response = requests.get(f"{st.session_state.api_url}/api/dashboard")
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get("summary", {})
                
                # Key Metrics
                st.subheader("📈 Key Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Income", 
                        f"€{summary.get('total_income', 0):,.2f}",
                        help="Total income from all sales"
                    )
                
                with col2:
                    st.metric(
                        "Total Expenses", 
                        f"€{summary.get('total_expenses', 0):,.2f}",
                        help="Total business expenses"
                    )
                
                with col3:
                    profit = summary.get('profit', 0)
                    profit_color = "normal" if profit >= 0 else "inverse"
                    st.metric(
                        "Net Profit", 
                        f"€{profit:,.2f}",
                        delta_color=profit_color,
                        help="Income minus expenses"
                    )
                
                with col4:
                    st.metric(
                        "Customers", 
                        summary.get('customer_count', 0),
                        help="Total customers in CRM"
                    )
                
                # Charts Row
                st.subheader("📊 Financial Overview")
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    # Expense by Category
                    expense_cats = data.get("expense_categories", [])
                    if expense_cats:
                        df_expenses = pd.DataFrame(expense_cats)
                        fig1 = px.pie(
                            df_expenses, 
                            values='total', 
                            names='category',
                            title='Expenses by Category',
                            color_discrete_sequence=px.colors.sequential.RdBu,
                            hole=0.4
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        st.info("No expense data yet")
                
                with chart_col2:
                    # Income by Category
                    income_cats = data.get("income_categories", [])
                    if income_cats:
                        df_income = pd.DataFrame(income_cats)
                        fig2 = px.pie(
                            df_income, 
                            values='total', 
                            names='category',
                            title='Income by Category',
                            color_discrete_sequence=px.colors.sequential.Greens,
                            hole=0.4
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("No income data yet")
                
                # Monthly Trends
                st.subheader("📅 Monthly Trends")
                monthly_data = data.get("monthly_trends", [])
                if monthly_data:
                    df_monthly = pd.DataFrame(monthly_data)
                    df_pivot = df_monthly.pivot_table(
                        index='month', 
                        columns='type', 
                        values='total', 
                        aggfunc='sum'
                    ).fillna(0).reset_index()
                    
                    fig3 = px.line(
                        df_pivot, 
                        x='month', 
                        y=['income', 'expense'],
                        title='Monthly Income vs Expenses',
                        markers=True,
                        labels={'value': 'Amount (€)', 'variable': 'Type'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("Not enough data for monthly trends")
                
                # Recent Activity Row
                st.subheader("🕒 Recent Activity")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Recent Transactions
                    st.markdown("**Recent Transactions**")
                    recent = data.get("recent_transactions", [])
                    if recent:
                        df_recent = pd.DataFrame(recent)
                        if 'date' in df_recent.columns:
                            df_recent['date'] = pd.to_datetime(df_recent['date'])
                            df_recent['date'] = df_recent['date'].dt.strftime('%m-%d %H:%M')
                        
                        df_recent['amount'] = df_recent['amount'].apply(lambda x: f"€{x:,.2f}")
                        df_recent['type'] = df_recent['type'].apply(
                            lambda x: "💰" if x == "expense" else "💎"
                        )
                        
                        st.dataframe(
                            df_recent[['date', 'type', 'category', 'amount']],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "date": "Date",
                                "type": "Type",
                                "category": "Category",
                                "amount": "Amount"
                            }
                        )
                    else:
                        st.info("No recent transactions")
                
                with col2:
                    # Top Customers
                    st.markdown("**Top Customers**")
                    top_customers = data.get("top_customers", [])
                    if top_customers:
                        df_customers = pd.DataFrame(top_customers)
                        df_customers['total_spent'] = df_customers['total_spent'].apply(
                            lambda x: f"€{x:,.2f}"
                        )
                        
                        st.dataframe(
                            df_customers[['name', 'instagram', 'total_spent']],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "name": "Customer",
                                "instagram": "Instagram",
                                "total_spent": "Total Spent"
                            }
                        )
                    else:
                        st.info("No customer data yet")
                
                # Quick Actions
                st.subheader("⚡ Quick Actions")
                action_cols = st.columns(4)
                
                with action_cols[0]:
                    if st.button("➕ Add Expense", use_container_width=True):
                        st.session_state.page = "Expenses"
                        st.rerun()
                
                with action_cols[1]:
                    if st.button("👤 Add Customer", use_container_width=True):
                        st.session_state.page = "Customers"
                        st.rerun()
                
                with action_cols[2]:
                    if st.button("📊 View Reports", use_container_width=True):
                        st.session_state.page = "Analytics"
                        st.rerun()
                
                with action_cols[3]:
                    if st.button("🔄 Refresh Data", use_container_width=True):
                        st.rerun()
                
            else:
                st.error("Could not load dashboard data")
                # Show sample data for demo
                show_sample_dashboard()
                
        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")
            show_sample_dashboard()

    # Expenses Page
    elif page == "Expenses":
        st.markdown('<h1 class="main-header">💰 Expense & Income Management</h1>', unsafe_allow_html=True)
        
        # Fetch categories from backend
        try:
            categories_response = requests.get(f"{st.session_state.api_url}/api/categories")
            if categories_response.status_code == 200:
                categories = categories_response.json()
                expense_categories = categories.get("expense_categories", [])
                income_categories = categories.get("income_categories", [])
            else:
                expense_categories = ["Materials", "Shipping", "Packaging", "Marketing", "Other"]
                income_categories = ["Jewelry Sales", "Custom Orders", "Repairs", "Other"]
        except:
            expense_categories = ["Materials", "Shipping", "Packaging", "Marketing", "Other"]
            income_categories = ["Jewelry Sales", "Custom Orders", "Repairs", "Other"]
        
        # Tabs for Add Transaction and View Transactions
        tab1, tab2, tab3 = st.tabs(["➕ Add Transaction", "📋 View Transactions", "📊 Statistics"])
        
        with tab1:
            # Add transaction form
            with st.form("add_transaction_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    transaction_type = st.selectbox(
                        "Type *", 
                        ["expense", "income"],
                        format_func=lambda x: "💰 Expense" if x == "expense" else "💎 Income"
                    )
                    amount = st.number_input(
                        "Amount (€) *", 
                        min_value=0.01, 
                        step=0.01,
                        format="%.2f"
                    )
                
                with col2:
                    if transaction_type == "expense":
                        category = st.selectbox("Category *", expense_categories)
                    else:
                        category = st.selectbox("Category *", income_categories)
                    
                    description = st.text_area("Description", placeholder="What was this for?")
                
                submitted = st.form_submit_button("Add Transaction", type="primary", use_container_width=True)
                
                if submitted:
                    if amount <= 0:
                        st.error("⚠️ Amount must be greater than 0")
                    else:
                        transaction_data = {
                            "amount": amount,
                            "type": transaction_type,
                            "category": category,
                            "description": description if description else None
                        }
                        
                        try:
                            response = requests.post(
                                f"{st.session_state.api_url}/api/transactions", 
                                json=transaction_data
                            )
                            
                            if response.status_code == 200:
                                st.success(f"✅ {transaction_type.title()} added successfully!")
                                st.balloons()
                                # Refresh the page to show new transaction
                                st.rerun()
                            else:
                                error_detail = response.json().get("detail", "Unknown error")
                                st.error(f"❌ Failed to add transaction: {error_detail}")
                        except Exception as e:
                            st.error(f"❌ Connection error: {str(e)}")
        
        # In the Expenses page, "View Transactions" tab (tab2)
        with tab2:
            # View transactions with filters
            st.subheader("Transaction History")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_type = st.selectbox("Filter by type", ["All", "expense", "income"])
            with col2:
                sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Amount (High to Low)", "Amount (Low to High)"])
            with col3:
                limit = st.slider("Show entries", 5, 50, 20)
            
            try:
                # Build query parameters
                params = {"limit": limit}
                if filter_type != "All":
                    params["type"] = filter_type
                
                response = requests.get(f"{st.session_state.api_url}/api/transactions", params=params)
                
                if response.status_code == 200:
                    transactions = response.json()
                    
                    if transactions:
                        # Convert to DataFrame
                        df = pd.DataFrame(transactions)
                        
                        # DEBUG: Show what columns we have
                        # st.write("Available columns:", df.columns.tolist())
                        
                        # FIX: Check if we have 'date' or 'transaction_date' column
                        if 'transaction_date' in df.columns and 'date' not in df.columns:
                            df['date'] = df['transaction_date']
                        
                        # FIX: Handle category_id vs category
                        if 'category_id' in df.columns and 'category' not in df.columns:
                            # We need to fetch category names
                            try:
                                categories_response = requests.get(f"{st.session_state.api_url}/api/categories")
                                if categories_response.status_code == 200:
                                    categories_data = categories_response.json()
                                    # Create a mapping from category_id to category name
                                    category_map = {}
                                    
                                    # Map expense categories (they don't have IDs in the simple categories endpoint)
                                    # For now, use category_id as category name
                                    df['category'] = df['category_id'].apply(lambda x: f"Category {x}" if pd.notna(x) else "Unknown")
                            except:
                                df['category'] = df['category_id'].apply(lambda x: f"Category {x}" if pd.notna(x) else "Unknown")
                        
                        # Convert date string to datetime
                        if 'date' in df.columns:
                            df['date'] = pd.to_datetime(df['date'])
                        
                        # Apply sorting
                        if sort_by == "Newest":
                            df = df.sort_values('date', ascending=False)
                        elif sort_by == "Oldest":
                            df = df.sort_values('date', ascending=True)
                        elif sort_by == "Amount (High to Low)":
                            df = df.sort_values('amount', ascending=False)
                        elif sort_by == "Amount (Low to High)":
                            df = df.sort_values('amount', ascending=True)
                        
                        # Format display
                        display_df = df.copy()
                        if 'date' in display_df.columns:
                            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d %H:%M')
                        display_df['amount'] = display_df['amount'].apply(lambda x: f"€{x:,.2f}")
                        display_df['type'] = display_df['type'].apply(
                            lambda x: f"💰 {x}" if x == "expense" else f"💎 {x}"
                        )
                        
                        # Display table - Use available columns
                        columns_to_show = []
                        if 'date' in display_df.columns:
                            columns_to_show.append('date')
                        columns_to_show.extend(['type', 'category', 'amount'])
                        if 'description' in display_df.columns:
                            columns_to_show.append('description')
                        
                        st.dataframe(
                            display_df[columns_to_show],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "date": st.column_config.TextColumn("Date & Time"),
                                "type": st.column_config.TextColumn("Type"),
                                "category": st.column_config.TextColumn("Category"),
                                "amount": st.column_config.TextColumn("Amount"),
                                "description": st.column_config.TextColumn("Description")
                            }
                        )
                        
                        # Summary
                        total_expenses = df[df['type'] == 'expense']['amount'].sum()
                        total_income = df[df['type'] == 'income']['amount'].sum()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Expenses", f"€{total_expenses:,.2f}")
                        with col2:
                            st.metric("Total Income", f"€{total_income:,.2f}")
                        with col3:
                            st.metric("Net", f"€{total_income - total_expenses:,.2f}")
                        
                        # Export button
                        if st.button("📥 Export to CSV", use_container_width=True):
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name="shiny_jar_transactions.csv",
                                mime="text/csv"
                            )
                    else:
                        st.info("📭 No transactions yet. Add your first one!")
                else:
                    st.error(f"Failed to fetch transactions: {response.status_code}")
            except Exception as e:
                st.error(f"Error loading transactions: {str(e)}")
        
        with tab3:
            # Statistics
            st.subheader("📈 Transaction Statistics")
            
            try:
                stats_response = requests.get(f"{st.session_state.api_url}/api/stats")
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Income", f"€{stats['total_income']:,.2f}")
                    with col2:
                        st.metric("Total Expenses", f"€{stats['total_expenses']:,.2f}")
                    with col3:
                        profit_color = "normal" if stats['profit'] >= 0 else "inverse"
                        st.metric("Profit", f"€{stats['profit']:,.2f}", delta_color=profit_color)
                    with col4:
                        st.metric("Total Transactions", stats['transaction_count'])
                    
                    # Category breakdown
                    st.subheader("Category Breakdown")
                    
                    try:
                        all_transactions = requests.get(f"{st.session_state.api_url}/api/transactions", params={"limit": 1000}).json()
                        if all_transactions:
                            df_all = pd.DataFrame(all_transactions)
                            
                            # FIX: Handle date/transaction_date and category_id/category
                            if 'transaction_date' in df_all.columns and 'date' not in df_all.columns:
                                df_all['date'] = df_all['transaction_date']
                            
                            # For category, if we have category_id but not category name
                            if 'category_id' in df_all.columns and 'category' not in df_all.columns:
                                # Use category_id as temporary category name
                                df_all['category'] = df_all['category_id'].apply(lambda x: f"Category {x}" if pd.notna(x) else "Unknown")
                            
                            # Expense categories
                            expense_df = df_all[df_all['type'] == 'expense']
                            if not expense_df.empty:
                                expense_by_category = expense_df.groupby('category')['amount'].sum().reset_index()
                                expense_by_category = expense_by_category.sort_values('amount', ascending=False)
                                
                                fig1 = px.pie(
                                    expense_by_category, 
                                    values='amount', 
                                    names='category',
                                    title='Expense Distribution by Category',
                                    color_discrete_sequence=px.colors.sequential.RdBu
                                )
                                st.plotly_chart(fig1, use_container_width=True)
                            
                            # Income categories
                            income_df = df_all[df_all['type'] == 'income']
                            if not income_df.empty:
                                income_by_category = income_df.groupby('category')['amount'].sum().reset_index()
                                income_by_category = income_by_category.sort_values('amount', ascending=False)
                                
                                fig2 = px.pie(
                                    income_by_category, 
                                    values='amount', 
                                    names='category',
                                    title='Income Distribution by Category',
                                    color_discrete_sequence=px.colors.sequential.Greens
                                )
                                st.plotly_chart(fig2, use_container_width=True)
                    except Exception as e:
                        st.info(f"No data available for charts yet: {str(e)}")
                        
                else:
                    st.info("Statistics not available yet")
            except Exception as e:
                st.info(f"Connect to backend to see statistics: {str(e)}")
    #Customers page
    # elif page == "Customers":
    #     st.markdown('<h1 class="main-header">👥 Customer CRM</h1>', unsafe_allow_html=True)
        
    #     # Add customer form
    #     with st.form("add_customer"):
    #         col1, col2 = st.columns(2)
            
    #         with col1:
    #             name = st.text_input("Customer Name")
    #             email = st.text_input("Email")
            
    #         with col2:
    #             instagram = st.text_input("Instagram Handle")
    #             phone = st.text_input("Phone")
            
    #         submitted = st.form_submit_button("Add Customer")
            
    #         if submitted and name:
    #             st.success(f"✅ Customer {name} added (simulated)")
    #             # In a real app, you would send this to the backend
        
    #     # Customer list
    #     st.subheader("📋 Customer Directory")
    #     try:
    #         response = requests.get(f"{st.session_state.api_url}/api/customers")
    #         if response.status_code == 200:
    #             customers = response.json()["customers"]
    #             if customers:
    #                 df = pd.DataFrame(customers)
    #                 st.dataframe(df, use_container_width=True)
    #             else:
    #                 st.info("No customers yet. Add your first customer!")
    #         else:
    #             # Show sample data
    #             sample_customers = [
    #                 {"id": 1, "name": "Maria Silva", "instagram": "maria_silva", "email": "maria@email.com", "total_spent": 250.00},
    #                 {"id": 2, "name": "John Doe", "instagram": "john_jewelry", "email": "john@email.com", "total_spent": 180.00},
    #                 {"id": 3, "name": "Anna Smith", "instagram": "anna_sparkle", "email": "anna@email.com", "total_spent": 320.00},
    #             ]
    #             df = pd.DataFrame(sample_customers)
    #             st.dataframe(df, use_container_width=True)
    #             st.info("Showing sample data. Connect to backend for real data.")
    #     except:
    #         st.info("Connect to backend to see customers")

    # Real Customers Page
    # elif st.session_state.page == "Customers":
    elif page == "Customers":
        st.markdown('<h1 class="main-header">👥 Customer CRM</h1>', unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 All Customers", "➕ Add Customer", "🔍 Search", "📊 Insights"])
        
        with tab1:
            # All Customers with CRUD operations
            st.subheader("Customer Directory")
            
            try:
                response = requests.get(f"{st.session_state.api_url}/api/customers")
                
                if response.status_code == 200:
                    customers = response.json()
                    
                    if customers:
                        df = pd.DataFrame(customers)
                        
                        # Format for display
                        display_df = df.copy()
                        display_df['total_spent'] = display_df['total_spent'].apply(lambda x: f"€{x:,.2f}")
                        
                        # Show table
                        st.dataframe(
                            display_df[['name', 'instagram_handle', 'email', 'total_spent']],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "name": st.column_config.TextColumn("Customer Name", width="medium"),
                                "instagram_handle": st.column_config.TextColumn("Instagram", width="small"),
                                "email": st.column_config.TextColumn("Email", width="medium"),
                                "total_spent": st.column_config.TextColumn("Total Spent", width="small")
                            }
                        )
                        
                        # Customer actions
                        st.subheader("Customer Actions")
                        action_cols = st.columns(3)
                        
                        with action_cols[0]:
                            selected_customer = st.selectbox(
                                "Select Customer",
                                options=[f"{c['id']}: {c['name']}" for c in customers],
                                key="customer_select"
                            )
                        
                        with action_cols[1]:
                            if selected_customer and st.button("👀 View Details", use_container_width=True):
                                customer_id = int(selected_customer.split(":")[0])
                                st.session_state.view_customer_id = customer_id
                                st.rerun()
                        
                        with action_cols[2]:
                            if selected_customer:
                                if st.button("🗑️ Delete", use_container_width=True, type="secondary"):
                                    # Confirmation
                                    customer_id = int(selected_customer.split(":")[0])
                                    customer_name = selected_customer.split(":")[1].strip()
                                    
                                    with st.popover("⚠️ Confirm Delete"):
                                        st.warning(f"Delete {customer_name}? This cannot be undone!")
                                        if st.button(f"DELETE {customer_name}", type="primary"):
                                            try:
                                                delete_response = requests.delete(
                                                    f"{st.session_state.api_url}/api/customers/{customer_id}"
                                                )
                                                if delete_response.status_code == 200:
                                                    st.success("✅ Customer deleted!")
                                                    time.sleep(1)
                                                    st.rerun()
                                                else:
                                                    st.error("❌ Failed to delete customer")
                                            except Exception as e:
                                                st.error(f"❌ Connection error: {str(e)}")
                        
                    else:
                        st.info("📭 No customers yet. Add your first customer!")
                else:
                    st.error("Failed to load customers")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            # Add Customer Form
            st.subheader("Add New Customer")
            
            with st.form("add_customer_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name *", placeholder="Maria Silva")
                    email = st.text_input("Email", placeholder="maria@email.com")
                
                with col2:
                    instagram = st.text_input("Instagram Handle", placeholder="@maria_silva")
                    total_spent = st.number_input("Total Spent (€)", min_value=0.0, step=10.0, value=0.0)
                
                notes = st.text_area("Notes", placeholder="Customer preferences, special requests...")
                
                submitted = st.form_submit_button("Add Customer", type="primary", use_container_width=True)
                
                if submitted:
                    if not name:
                        st.error("Name is required!")
                    else:
                        customer_data = {
                            "name": name,
                            "instagram_handle": instagram if instagram else None,
                            "email": email if email else None,
                            "total_spent": total_spent
                        }
                        
                        try:
                            response = requests.post(
                                f"{st.session_state.api_url}/api/customers",
                                json=customer_data
                            )
                            
                            if response.status_code == 200:
                                st.success(f"✅ Customer {name} added successfully!")
                                st.balloons()
                                st.rerun()
                            else:
                                error_detail = response.json().get("detail", "Unknown error")
                                st.error(f"❌ Failed to add customer: {error_detail}")
                        except Exception as e:
                            st.error(f"❌ Connection error: {str(e)}")
        
        with tab3:
            # Search Customers
            st.subheader("Search Customers")
            
            search_query = st.text_input("Search by name, Instagram, or email", key="customer_search")
            
            if search_query:
                try:
                    response = requests.get(
                        f"{st.session_state.api_url}/api/customers/search",
                        params={"q": search_query}
                    )
                    
                    if response.status_code == 200:
                        customers = response.json()
                        
                        if customers:
                            df = pd.DataFrame(customers)
                            df['total_spent'] = df['total_spent'].apply(lambda x: f"€{x:,.2f}")
                            
                            st.dataframe(
                                df[['name', 'instagram_handle', 'email', 'total_spent']],
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            st.metric("Found Customers", len(customers))
                        else:
                            st.info("No customers found matching your search")
                    else:
                        st.error("Search failed")
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
            else:
                st.info("Enter a search term to find customers")
        
        with tab4:
            # Customer Insights
            st.subheader("Customer Insights")
            
            try:
                response = requests.get(f"{st.session_state.api_url}/api/customers")
                
                if response.status_code == 200:
                    customers = response.json()
                    
                    if customers:
                        df = pd.DataFrame(customers)
                        
                        # Top Customers Chart
                        top_customers = df.nlargest(5, 'total_spent')
                        
                        fig1 = px.bar(
                            top_customers,
                            x='name',
                            y='total_spent',
                            title='Top 5 Customers by Spending',
                            color='total_spent',
                            color_continuous_scale='Viridis',
                            labels={'name': 'Customer', 'total_spent': 'Total Spent (€)'}
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        # Customer Stats
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            avg_spent = df['total_spent'].mean()
                            st.metric("Average Spend", f"€{avg_spent:,.2f}")
                        
                        with col2:
                            total_customers = len(df)
                            st.metric("Total Customers", total_customers)
                        
                        with col3:
                            total_revenue = df['total_spent'].sum()
                            st.metric("Total Revenue", f"€{total_revenue:,.2f}")
                        
                        # Customer distribution by spend
                        st.subheader("Spending Distribution")
                        fig2 = px.histogram(
                            df, 
                            x='total_spent',
                            nbins=10,
                            title='Customer Spending Distribution',
                            labels={'total_spent': 'Total Spent (€)', 'count': 'Number of Customers'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                        
                    else:
                        st.info("No customer data available for insights")
                else:
                    st.error("Failed to load customer data")
            except Exception as e:
                st.error(f"Error loading insights: {str(e)}")
        
        # View Customer Details (if selected)
        if 'view_customer_id' in st.session_state:
            st.markdown("---")
            st.subheader("👤 Customer Details")
            
            try:
                customer_id = st.session_state.view_customer_id
                response = requests.get(f"{st.session_state.api_url}/api/customers")
                
                if response.status_code == 200:
                    customers = response.json()
                    customer = next((c for c in customers if c['id'] == customer_id), None)
                    
                    if customer:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Name:** {customer['name']}")
                            if customer['instagram_handle']:
                                st.markdown(f"**Instagram:** @{customer['instagram_handle']}")
                            if customer['email']:
                                st.markdown(f"**Email:** {customer['email']}")
                        
                        with col2:
                            st.markdown(f"**Total Spent:** €{customer['total_spent']:,.2f}")
                            st.markdown(f"**Customer ID:** {customer['id']}")
                        
                        # Edit form
                        with st.expander("✏️ Edit Customer"):
                            with st.form("edit_customer_form"):
                                new_name = st.text_input("Name", value=customer['name'])
                                new_instagram = st.text_input("Instagram", value=customer['instagram_handle'] or "")
                                new_email = st.text_input("Email", value=customer['email'] or "")
                                new_total = st.number_input("Total Spent", value=customer['total_spent'])
                                
                                if st.form_submit_button("Update Customer"):
                                    update_data = {
                                        "name": new_name,
                                        "instagram_handle": new_instagram if new_instagram else None,
                                        "email": new_email if new_email else None,
                                        "total_spent": new_total
                                    }
                                    
                                    try:
                                        update_response = requests.put(
                                            f"{st.session_state.api_url}/api/customers/{customer_id}",
                                            json=update_data
                                        )
                                        if update_response.status_code == 200:
                                            st.success("Customer updated!")
                                            del st.session_state.view_customer_id
                                            st.rerun()
                                        else:
                                            st.error("Update failed")
                                    except:
                                        st.error("Connection error")
                        
                        # Close button
                        if st.button("Close Details"):
                            del st.session_state.view_customer_id
                            st.rerun()
                            
                    else:
                        st.error("Customer not found")
                        del st.session_state.view_customer_id
                else:
                    st.error("Failed to load customer data")
            except:
                st.error("Error loading customer details")

    # Suppliers page under frontend/pages
    elif page == "Suppliers":
        show_suppliers_page()

    # Budgeting page undre frontend/pages
    elif page == "Budget":
        show_budget_page()
        
    # Reporting page under frontend/pages
    elif page == "Reports":
        show_reports_page()

    # Analytics page under frontend/pages
    elif page == "Analytics":
        show_analytics_page()

    # Analytics below are just dummy for testings
    # Analytics page
    # elif page == "Analytics":
    #     st.markdown('<h1 class="main-header">📈 Analytics & Reports</h1>', unsafe_allow_html=True)
        
    #     # Sample analytics
    #     col1, col2 = st.columns(2)
        
    #     with col1:
    #         st.subheader("Monthly Revenue")
    #         months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    #         revenue = [1500, 1800, 2200, 1900, 2400, 2800]
    #         expenses = [800, 850, 900, 820, 950, 1000]
            
    #         df = pd.DataFrame({
    #             'Month': months,
    #             'Revenue': revenue,
    #             'Expenses': expenses
    #         })
            
    #         fig = px.line(df, x='Month', y=['Revenue', 'Expenses'], 
    #                      title='Monthly Performance', markers=True)
    #         st.plotly_chart(fig, use_container_width=True)
        
    #     with col2:
    #         st.subheader("Customer Spending")
    #         customers = ['Customer A', 'Customer B', 'Customer C', 'Customer D', 'Customer E']
    #         spending = [320, 280, 450, 190, 310]
            
    #         df2 = pd.DataFrame({
    #             'Customer': customers,
    #             'Spending (€)': spending
    #         })
            
    #         fig2 = px.bar(df2, x='Customer', y='Spending (€)', 
    #                       title='Top Customers', color='Spending (€)')
    #         st.plotly_chart(fig2, use_container_width=True)
        
    #     # Export options
    #     st.subheader("📤 Export Reports")
    #     col1, col2, col3 = st.columns(3)
        
    #     with col1:
    #         if st.button("📄 Export as PDF", use_container_width=True):
    #             st.success("PDF export simulated")
        
    #     with col2:
    #         if st.button("📊 Export as Excel", use_container_width=True):
    #             st.success("Excel export simulated")
        
    #     with col3:
    #         if st.button("📈 Export as CSV", use_container_width=True):
    #             st.success("CSV export simulated")
    
    # For now, just show dashboard if nothing else
    st.markdown('<h1 class="main-header">💎 Shiny Jar CRM</h1>', unsafe_allow_html=True)
    st.info("🚀 Application is running! Please select a page from the sidebar.")

# Helper function for sample dashboard
def show_sample_dashboard():
    """Show sample data when API is unavailable"""
    st.warning("Showing sample data - API connection needed for real data")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Income", "€2,450")
    with col2:
        st.metric("Total Expenses", "€890")
    with col3:
        st.metric("Net Profit", "€1,560")
    with col4:
        st.metric("Customers", "124")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 Connect to backend for expense chart")
    with col2:
        st.info("📈 Connect to backend for income chart")
        
# Add this to your dashboard page or create a separate analytics page:

def show_advanced_analytics(api_url):
    st.markdown('<h1 class="main-header">🔮 Advanced Analytics</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Sales Forecasting", "📊 Customer Insights", "📦 Inventory Analytics"])
    
    with tab1:
        show_sales_forecasting(api_url)
    
    with tab2:
        show_customer_insights(api_url)
    
    with tab3:
        show_inventory_analytics(api_url)

def show_sales_forecasting(api_url):
    st.subheader("Sales Forecasting")
    
    try:
        # Fetch transaction data
        response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
        
        if response.status_code == 200:
            transactions = response.json()
            
            if transactions:
                df = pd.DataFrame(transactions)
                df['date'] = pd.to_datetime(df['date'])
                
                # Filter income transactions
                income_df = df[df['type'] == 'income']
                
                if not income_df.empty:
                    # Resample to monthly
                    monthly_sales = income_df.set_index('date').resample('M')['amount'].sum().reset_index()
                    
                    # Simple forecasting (linear regression)
                    monthly_sales['month_num'] = range(len(monthly_sales))
                    
                    # Fit linear model
                    from sklearn.linear_model import LinearRegression
                    import numpy as np
                    
                    X = monthly_sales['month_num'].values.reshape(-1, 1)
                    y = monthly_sales['amount'].values
                    
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    # Forecast next 3 months
                    future_months = np.array([[len(monthly_sales)], 
                                            [len(monthly_sales) + 1], 
                                            [len(monthly_sales) + 2]])
                    predictions = model.predict(future_months)
                    
                    # Display forecast
                    st.subheader("3-Month Sales Forecast")
                    
                    forecast_df = pd.DataFrame({
                        'Month': ['Next Month', 'Month +2', 'Month +3'],
                        'Forecasted Sales': predictions
                    })
                    
                    st.dataframe(
                        forecast_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Month": "Month",
                            "Forecasted Sales": st.column_config.NumberColumn("Amount", format="€%.2f")
                        }
                    )
                    
                    # Chart with forecast
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(go.Scatter(
                        x=monthly_sales['date'],
                        y=monthly_sales['amount'],
                        mode='lines+markers',
                        name='Historical Sales',
                        line=dict(color='blue', width=2)
                    ))
                    
                    # Forecast
                    future_dates = pd.date_range(
                        start=monthly_sales['date'].iloc[-1] + pd.DateOffset(months=1),
                        periods=3,
                        freq='M'
                    )
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=predictions,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='red', width=2, dash='dash')
                    ))
                    
                    fig.update_layout(
                        title='Sales Trend & Forecast',
                        xaxis_title='Date',
                        yaxis_title='Sales (€)',
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Insights
                    st.subheader("📈 Insights")
                    
                    growth_rate = ((monthly_sales['amount'].iloc[-1] - monthly_sales['amount'].iloc[0]) / 
                                  monthly_sales['amount'].iloc[0] * 100) if monthly_sales['amount'].iloc[0] > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Avg Monthly Sales", f"€{monthly_sales['amount'].mean():,.2f}")
                    with col2:
                        st.metric("Growth Rate", f"{growth_rate:.1f}%")
                    with col3:
                        st.metric("Best Month", f"€{monthly_sales['amount'].max():,.2f}")
                    
                else:
                    st.info("No sales data available for forecasting")
            
            else:
                st.info("No transaction data available")
        
        else:
            st.error("Failed to fetch transaction data")
    
    except Exception as e:
        st.error(f"Error in sales forecasting: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "💎 Shiny Jar Business Suite | Built with ❤️ for University Project"
    "</div>",
    unsafe_allow_html=True
)

# Run the app
if __name__ == "__main__":
    main()