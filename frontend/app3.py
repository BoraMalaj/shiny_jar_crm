# frontend/app.py - COMPATIBLE FIXED VERSION
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import time

# ========== PAGE CONFIG (MUST BE FIRST) ==========
st.set_page_config(
    page_title="Shiny Jar CRM | Jewelry Business Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== IMPORT AUTH ==========
try:
    from auth import auth, show_login_page
    AUTH_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Auth module error: {str(e)}")
    AUTH_AVAILABLE = False
    class DummyAuth:
        def is_authenticated(self): return True
        def get_user_role(self): return 'admin'
        def get_username(self): return 'Admin'
        def get_user_data(self): return {'role': 'admin'}
        def has_role(self, x): return True
        def logout(self): pass
        def get_auth_header(self): return {}
        def is_demo_mode(self): return True
    
    auth = DummyAuth()
    show_login_page = lambda: st.info("Login system loading...")

# ========== IMPORT PAGES ==========
# Initialize all page variables first with safe defaults
show_budget_page = None
show_suppliers_page = None
show_analytics_page = None
show_reports_page = None
show_inventory_page = None
generate_inventory_report = None

# Customer page functions
show_customer_dashboard = None
show_customer_orders = None
show_customer_invoices = None
show_customer_profile = None

# Supplier page functions  
show_supplier_dashboard = None
show_supplier_orders = None
show_supplier_products = None
show_supplier_payments = None
show_supplier_profile = None

# Page availability flags - ADD THESE!
CUSTOMER_PAGES_AVAILABLE = False
SUPPLIER_PAGES_AVAILABLE = False
INVENTORY_AVAILABLE = False
PAGES_AVAILABLE = False

# Try to import with error handling
try:
    from pages.budget import show_budget_page
    from pages.suppliers import show_suppliers_page
    from pages.analytics import show_analytics_page
    from pages.reports import show_reports_page
    from pages.inventory import show_inventory_page, generate_inventory_report
    INVENTORY_AVAILABLE = True
    PAGES_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Some admin pages not available: {str(e)}")
    PAGES_AVAILABLE = False
    INVENTORY_AVAILABLE = False
    
    # Create fallback functions
    def show_budget_page(): 
        st.info("💰 Budget Management")
    
    def show_suppliers_page(): 
        st.info("🏭 Supplier Management")
    
    def show_analytics_page(): 
        st.info("📈 Advanced Analytics")
    
    def show_reports_page(): 
        st.info("📊 Professional Reports")
    
    def show_inventory_page(): 
        st.info("📦 Inventory Management")
    
    def generate_inventory_report(): 
        st.info("📄 Inventory Reports")

# Try to import customer dashboard - UPDATE THIS SECTION:
try:
    from pages.customer_dashboard import show_customer_dashboard
    CUSTOMER_PAGES_AVAILABLE = True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = False
    def show_customer_dashboard(): 
        st.info("👤 Customer Dashboard")
        
try:
    from pages.customer_dashboard import display_customer_real_data
    CUSTOMER_PAGES_AVAILABLE = True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = False
    def display_customer_real_data(): 
        st.info("👤 Customer Data")
        
try:
    from pages.customer_dashboard import show_customer_demo_dashboard
    CUSTOMER_PAGES_AVAILABLE = True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = False
    def show_customer_demo_dashboard(): 
        st.info("👤 Customer Demo Dashboard")

try:
    from pages.customer_dashboard import show_customer_orders
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or False
    def show_customer_orders(): 
        st.info("🛍️ Customer Orders")

try:
    from pages.customer_dashboard import show_customer_invoices
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or False
    def show_customer_invoices(): 
        st.info("💳 Customer Invoices")

try:
    from pages.customer_dashboard import show_customer_profile
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or True
except ImportError:
    CUSTOMER_PAGES_AVAILABLE = CUSTOMER_PAGES_AVAILABLE or False
    def show_customer_profile(): 
        st.info("👤 Customer Profile")

# Try to import supplier dashboard - UPDATE THIS SECTION:
try:
    from pages.supplier_dashboard import show_supplier_dashboard
    SUPPLIER_PAGES_AVAILABLE = True
except ImportError:
    SUPPLIER_PAGES_AVAILABLE = False
    def show_supplier_dashboard(): 
        st.info("🏭 Supplier Dashboard")

try:
    from pages.supplier_dashboard import show_supplier_orders
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or True
except ImportError:
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or False
    def show_supplier_orders(): 
        st.info("📦 Supplier Orders")

try:
    from pages.supplier_dashboard import show_supplier_products
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or True
except ImportError:
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or False
    def show_supplier_products(): 
        st.info("📋 Supplier Products")

try:
    from pages.supplier_dashboard import show_supplier_payments
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or True
except ImportError:
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or False
    def show_supplier_payments(): 
        st.info("💰 Supplier Payments")

try:
    from pages.supplier_dashboard import show_supplier_profile
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or True
except ImportError:
    SUPPLIER_PAGES_AVAILABLE = SUPPLIER_PAGES_AVAILABLE or False
    def show_supplier_profile(): 
        st.info("🏢 Supplier Profile")

# ========== DARK MODERN STYLES ==========
def apply_dark_theme():
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

# ========== PAGE FUNCTIONS ==========

#================================================== Demo Dashboard ===================================================================
def show_demo_dashboard():
    """Main dashboard with dark theme"""
    st.markdown('<h1 class="main-header">💎 Dashboard Overview</h1>', unsafe_allow_html=True)
    
    if auth.is_demo_mode():
        st.warning("**Demo Mode** - Using sample data. Connect to backend for live data.")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", "€12,450", "+12%")
    
    with col2:
        st.metric("📉 Total Expenses", "€4,890", "-5%")
    
    with col3:
        st.metric("👥 Active Customers", "124", "+8")
    
    with col4:
        st.metric("💎 Net Profit", "€7,560", "+15%")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Monthly Performance")
        revenue_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Revenue': [1500, 1800, 2200, 1900, 2400, 2800],
            'Expenses': [800, 850, 900, 820, 950, 1000]
        })
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=revenue_data['Month'],
            y=revenue_data['Revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#8B5CF6', width=3)
        ))
        fig1.add_trace(go.Scatter(
            x=revenue_data['Month'],
            y=revenue_data['Expenses'],
            mode='lines+markers',
            name='Expenses',
            line=dict(color='#10B981', width=3)
        ))
        
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#F1F5F9'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("📊 Expense Distribution")
        expense_data = pd.DataFrame({
            'Category': ['Materials', 'Shipping', 'Marketing', 'Packaging', 'Other'],
            'Amount': [45, 12, 18, 14, 11]
        })
        
        fig2 = px.pie(expense_data, values='Amount', names='Category', hole=0.4)
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#F1F5F9'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    
    transactions = pd.DataFrame({
        'Date': ['2024-12-10', '2024-12-09', '2024-12-08', '2024-12-07'],
        'Type': ['Income', 'Income', 'Expense', 'Income'],
        'Description': ['Silver Necklace', 'Earrings', 'Materials', 'Custom Order'],
        'Amount': [89.00, 45.50, -120.00, 200.00],
        'Status': ['Completed', 'Completed', 'Pending', 'Completed']
    })
    
    st.dataframe(transactions, use_container_width=True, hide_index=True)
    
    # Quick actions
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("➕ Add Transaction", use_container_width=True):
            st.session_state.page = "Expenses"
            st.rerun()
    
    with action_cols[1]:
        if st.button("👤 Add Customer", use_container_width=True):
            st.session_state.page = "Customers"
            st.rerun()
    
    with action_cols[2]:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    
    with action_cols[3]:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
#===================================================== End of Demo Dashboard =====================================================

# Real Data from backend
def show_dashboard():
    """Main dashboard with REAL data from backend"""
    st.markdown('<h1 class="main-header">💎 Dashboard Overview</h1>', unsafe_allow_html=True)
    
    if auth.is_demo_mode():
        st.warning("**Demo Mode** - Using sample data. Connect to backend for live data.")
        # Fall back to demo data if in demo mode
        show_demo_dashboard()
        return
    
    try:
        # Fetch real data from backend
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        # Fetch dashboard stats
        response = requests.get(f"{api_url}/api/dashboard", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            display_real_dashboard(data)
        else:
            st.error(f"Failed to fetch dashboard data: {response.status_code}")
            show_demo_dashboard()  # Fallback
            
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        show_demo_dashboard()  # Fallback

def display_real_dashboard(data):
    """Display dashboard with real data"""
    summary = data.get('summary', {})
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", f"€{summary.get('total_income', 0):,.2f}")
    
    with col2:
        st.metric("📉 Total Expenses", f"€{summary.get('total_expenses', 0):,.2f}")
    
    with col3:
        st.metric("👥 Active Customers", summary.get('customer_count', 0))
    
    with col4:
        profit = summary.get('profit', 0)
        profit_delta = f"+{profit/summary.get('total_income', 1)*100:.1f}%" if summary.get('total_income', 0) > 0 else "0%"
        st.metric("💎 Net Profit", f"€{profit:,.2f}", profit_delta)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Monthly Performance")
        if 'monthly_trends' in data and data['monthly_trends']:
            # Process monthly trends
            trends_df = pd.DataFrame(data['monthly_trends'])
            
            # Separate income and expenses
            income_df = trends_df[trends_df['type'] == 'income']
            expense_df = trends_df[trends_df['type'] == 'expense']
            
            fig1 = go.Figure()
            
            if not income_df.empty:
                fig1.add_trace(go.Scatter(
                    x=income_df['month'],
                    y=income_df['total'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color='#8B5CF6', width=3)
                ))
            
            if not expense_df.empty:
                fig1.add_trace(go.Scatter(
                    x=expense_df['month'],
                    y=expense_df['total'],
                    mode='lines+markers',
                    name='Expenses',
                    line=dict(color='#10B981', width=3)
                ))
            
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#F1F5F9'
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No monthly trend data available yet")
    
    with col2:
        st.subheader("📊 Expense Distribution")
        if 'expense_categories' in data and data['expense_categories']:
            expense_data = pd.DataFrame(data['expense_categories'])
            
            fig2 = px.pie(expense_data, values='total', names='category', hole=0.4)
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#F1F5F9'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No expense category data available yet")
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    if 'recent_transactions' in data and data['recent_transactions']:
        transactions_df = pd.DataFrame(data['recent_transactions'])
        st.dataframe(transactions_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recent transactions available")
    
    # Top customers
    st.subheader("🏆 Top Customers")
    if 'top_customers' in data and data['top_customers']:
        customers_df = pd.DataFrame(data['top_customers'])
        # st.dataframe(customers_df, use_container_width=True, hide_index=True)
        
        # Sort by the spending column and take only the top 5 rows
        # customers_df = customers_df.sort_values(by='amount', ascending=False).head(5)        
        st.dataframe(customers_df.sort_values(by='total_spent', ascending=False).head(20), use_container_width=True, hide_index=True)
    else:
        st.info("No customer data available yet")
    
    # Quick actions
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("➕ Add Transaction", use_container_width=True):
            st.session_state.page = "Expenses"
            st.rerun()
    
    with action_cols[1]:
        if st.button("👤 Add Customer", use_container_width=True):
            st.session_state.page = "Customers"
            st.rerun()
    
    with action_cols[2]:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    
    with action_cols[3]:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

#================================================ START OF EXPENSES DEMO MODE =======================================================
# def show_expenses_page():
#     """Expenses management page"""
#     st.markdown('<h1 class="main-header">💰 Transaction Management</h1>', unsafe_allow_html=True)
    
#     tab1, tab2, tab3 = st.tabs(["➕ New Transaction", "📋 All Transactions", "📈 Analysis"])
    
#     with tab1:
#         with st.form("add_transaction"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 trans_type = st.selectbox("Transaction Type", ["Income", "Expense"])
#                 amount = st.number_input("Amount (€)", min_value=0.01, value=50.0)
#                 category = st.selectbox("Category", ["Materials", "Shipping", "Marketing", "Sales"])
            
#             with col2:
#                 date = st.date_input("Date", value=datetime.now())
#                 payment_method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Cash"])
#                 customer = st.selectbox("Customer/Supplier", ["Select...", "Maria Silva", "John Doe"])
            
#             description = st.text_area("Description")
            
#             if st.form_submit_button("💾 Save Transaction", use_container_width=True):
#                 st.success(f"✅ {trans_type} of €{amount:.2f} saved!")
    
#     with tab2:
#         st.subheader("Transaction History")
        
#         # Filters
#         col1, col2 = st.columns(2)
#         with col1:
#             filter_type = st.selectbox("Filter by Type", ["All", "Income", "Expense"])
#         with col2:
#             limit = st.slider("Show entries", 5, 50, 10)
        
#         # Sample data
#         transactions = pd.DataFrame({
#             'Date': pd.date_range(start='2024-11-01', periods=10, freq='D').strftime('%Y-%m-%d'),
#             'Type': ['Income', 'Income', 'Expense', 'Income', 'Expense', 'Income', 'Expense', 'Income', 'Expense', 'Income'],
#             'Category': ['Sales', 'Sales', 'Materials', 'Custom', 'Shipping', 'Sales', 'Marketing', 'Repair', 'Tools', 'Sales'],
#             'Description': ['Necklace', 'Earrings', 'Silver', 'Custom', 'Shipping', 'Bracelet', 'Ads', 'Repair', 'Tools', 'Ring'],
#             'Amount': [89.00, 45.50, -120.00, 200.00, -35.00, 75.25, -150.00, 45.00, -89.99, 55.00],
#             'Status': ['Completed', 'Completed', 'Paid', 'Completed', 'Pending', 'Completed', 'Paid', 'Completed', 'Paid', 'Completed']
#         })
        
#         st.dataframe(transactions.head(limit), use_container_width=True, hide_index=True)
    
#     with tab3:
#         st.subheader("Transaction Analysis")
        
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Total Income", "€1,250.75")
#         with col2:
#             st.metric("Total Expenses", "€-625.49")
#         with col3:
#             st.metric("Net Balance", "€625.26")
#================================================ END OF EXPENSES DEMO MODE =========================================================

# Expenses real backend mode
def show_expenses_page():
    """Expenses management page with dynamic dropdowns - FIXED VERSION"""
    st.markdown('<h1 class="main-header">💰 Transaction Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ New Transaction", "📋 All Transactions", "📈 Analysis"])
    
    # ========== TAB 1: NEW TRANSACTION ==========
    # with tab1:
    #     st.subheader("➕ Add New Transaction")
        
    #     # First, fetch dynamic data
    #     customers_list = ["Select Customer..."]
    #     suppliers_list = ["Select Supplier..."]
    #     categories_list = []
        
    #     try:
    #         headers = auth.get_auth_header()
    #         api_url = st.session_state.api_url
            
    #         # Fetch customers
    #         with st.spinner("🔄 Loading customers..."):
    #             response = requests.get(f"{api_url}/api/customers", headers=headers, timeout=5)
    #             if response.status_code == 200:
    #                 customers = response.json()
    #                 customers_list += [f"{c['name']} (ID: {c['id']})" for c in customers]
            
    #         # Fetch suppliers
    #         with st.spinner("🔄 Loading suppliers..."):
    #             response = requests.get(f"{api_url}/api/suppliers", headers=headers, timeout=5)
    #             if response.status_code == 200:
    #                 suppliers = response.json()
    #                 suppliers_list += [f"{s['name']} (ID: {s['id']})" for s in suppliers]
            
    #         # Fetch categories
    #         with st.spinner("🔄 Loading categories..."):
    #             response = requests.get(f"{api_url}/api/categories", headers=headers, timeout=3)
    #             if response.status_code == 200:
    #                 cat_data = response.json()
    #                 income_cats = cat_data.get('income_categories', [])
    #                 expense_cats = cat_data.get('expense_categories', [])
    #                 categories_list = list(set(income_cats + expense_cats))
                    
    #     except Exception as e:
    #         st.warning(f"⚠️ Could not fetch dynamic data: {str(e)}")
    #         # Default categories if API fails
    #         categories_list = ["Materials", "Shipping", "Marketing", "Packaging", "Tools", 
    #                          "Office Supplies", "Website", "Other", "Jewelry Sales", 
    #                          "Custom Orders", "Repairs", "Consultation", "Workshops"]
        
    #     # Transaction form
    #     with st.form("add_transaction", clear_on_submit=True):
    #         col1, col2 = st.columns(2)
            
    #         with col1:
    #             # Transaction type with session state
    #             if 'transaction_type' not in st.session_state:
    #                 st.session_state.transaction_type = "Income"
                
    #             trans_type = st.radio(
    #                 "Transaction Type", 
    #                 ["Income", "Expense"],
    #                 index=0 if st.session_state.transaction_type == "Income" else 1,
    #                 horizontal=True
    #             )
                
    #             # Update session state
    #             if trans_type != st.session_state.transaction_type:
    #                 st.session_state.transaction_type = trans_type
    #                 # Don't rerun here, let the user continue
                
    #             amount = st.number_input("Amount (€)", min_value=0.01, value=50.0, step=1.0)
                
    #             # Category selection
    #             if categories_list:
    #                 category = st.selectbox("Category", categories_list)
    #             else:
    #                 category = st.text_input("Category", placeholder="Enter category name")
            
    #         with col2:
    #             date = st.date_input("Date", value=datetime.now())
    #             payment_method = st.selectbox("Payment Method", 
    #                 ["Credit Card", "Bank Transfer", "Cash", "PayPal", "Other"])
                
    #             # Dynamic dropdown based on transaction type
    #             if trans_type == "Income":
    #                 st.markdown("**👤 Customer**")
    #                 customer = st.selectbox(
    #                     "Select Customer", 
    #                     customers_list,
    #                     key="customer_select",
    #                     label_visibility="collapsed"
    #                 )
    #                 supplier = None
    #             else:  # Expense
    #                 st.markdown("**🏭 Supplier**")
    #                 supplier = st.selectbox(
    #                     "Select Supplier", 
    #                     suppliers_list,
    #                     key="supplier_select", 
    #                     label_visibility="collapsed"
    #                 )
    #                 customer = None
            
    #         description = st.text_area("Description", placeholder="Enter transaction details...", 
    #                                  help="Optional: Add notes about this transaction")
            
    #         # Form buttons
    #         col1, col2, col3 = st.columns([2, 1, 1])
    #         with col1:
    #             submitted = st.form_submit_button(
    #                 f"💾 Save {trans_type}", 
    #                 use_container_width=True,
    #                 type="primary"
    #             )
    #         with col2:
    #             if st.form_submit_button("🔄 Clear Form", use_container_width=True):
    #                 # Clear form by rerunning
    #                 st.rerun()
    #         with col3:
    #             if st.form_submit_button("❌ Cancel", use_container_width=True):
    #                 st.info("Transaction cancelled")
            
    #         if submitted:
    #             # Validation
    #             validation_errors = []
                
    #             if amount <= 0:
    #                 validation_errors.append("Amount must be greater than 0")
    #             if trans_type == "Income" and customer == "Select Customer...":
    #                 validation_errors.append("Please select a customer for income transactions")
    #             if trans_type == "Expense" and supplier == "Select Supplier...":
    #                 validation_errors.append("Please select a supplier for expense transactions")
    #             if not category:
    #                 validation_errors.append("Category is required")
                
    #             if validation_errors:
    #                 for error in validation_errors:
    #                     st.error(f"❌ {error}")
    #             else:
    #                 # Prepare transaction data
    #                 transaction_data = {
    #                     "amount": float(amount),
    #                     "type": trans_type.lower(),
    #                     "category": category,
    #                     "description": description if description else None,
    #                     "transaction_date": date.isoformat(),
    #                     "payment_method": payment_method
    #                 }
                    
    #                 # Extract IDs from selection strings
    #                 try:
    #                     if trans_type == "Income" and customer != "Select Customer...":
    #                         # Extract customer ID from "Name (ID: X)"
    #                         customer_id = int(customer.split("(ID: ")[1].rstrip(")"))
    #                         transaction_data["customer_id"] = customer_id
                        
    #                     elif trans_type == "Expense" and supplier != "Select Supplier...":
    #                         # Extract supplier ID
    #                         supplier_id = int(supplier.split("(ID: ")[1].rstrip(")"))
    #                         transaction_data["supplier_id"] = supplier_id
                            
    #                 except Exception as e:
    #                     st.error(f"❌ Error parsing ID from selection: {str(e)}")
    #                     st.info(f"Customer string: {customer}" if customer else f"Supplier string: {supplier}")
    #                     return
                    
    #                 # Send to backend
    #                 try:
    #                     with st.spinner(f"Saving {trans_type.lower()}..."):
    #                         headers = auth.get_auth_header()
    #                         response = requests.post(
    #                             f"{st.session_state.api_url}/api/transactions",
    #                             json=transaction_data,
    #                             headers=headers,
    #                             timeout=10
    #                         )
                            
    #                         if response.status_code == 200:
    #                             saved_transaction = response.json()
    #                             st.success(f"✅ {trans_type} of €{amount:.2f} saved successfully!")
    #                             st.balloons()
                                
    #                             # Show success details
    #                             with st.expander("📋 Transaction Details", expanded=True):
    #                                 st.json(saved_transaction)
                                
    #                             # Auto-refresh after delay
    #                             time.sleep(2)
    #                             st.rerun()
                                
    #                         elif response.status_code == 422:
    #                             # Validation error from backend
    #                             error_data = response.json()
    #                             st.error(f"❌ Validation error: {error_data.get('detail', 'Unknown error')}")
    #                         else:
    #                             st.error(f"❌ Failed to save: {response.status_code} - {response.text[:200]}")
                                
    #                 except requests.exceptions.ConnectionError:
    #                     st.error("🔌 Could not connect to backend. Make sure server is running.")
    #                 except Exception as e:
    #                     st.error(f"❌ Error: {str(e)}")
    
    with tab1:
        st.subheader("➕ Add New Transaction")
        
        # First, fetch dynamic data
        customers_list = ["Select Customer..."]
        suppliers_list = ["Select Supplier..."]
        categories_list = []
        
        try:
            headers = auth.get_auth_header()
            api_url = st.session_state.api_url
            
            # Fetch customers
            with st.spinner("🔄 Loading customers..."):
                response = requests.get(f"{api_url}/api/customers", headers=headers, timeout=5)
                if response.status_code == 200:
                    customers = response.json()
                    customers_list += [f"{c['name']} (ID: {c['id']})" for c in customers]
            
            # Fetch suppliers
            with st.spinner("🔄 Loading suppliers..."):
                response = requests.get(f"{api_url}/api/suppliers", headers=headers, timeout=5)
                if response.status_code == 200:
                    suppliers = response.json()
                    suppliers_list += [f"{s['name']} (ID: {s['id']})" for s in suppliers]
            
            # Fetch categories
            with st.spinner("🔄 Loading categories..."):
                response = requests.get(f"{api_url}/api/categories", headers=headers, timeout=3)
                if response.status_code == 200:
                    cat_data = response.json()
                    income_cats = cat_data.get('income_categories', [])
                    expense_cats = cat_data.get('expense_categories', [])
                    categories_list = list(set(income_cats + expense_cats))
                    
        except Exception as e:
            st.warning(f"⚠️ Could not fetch dynamic data: {str(e)}")
            # Default categories if API fails
            categories_list = ["Materials", "Shipping", "Marketing", "Packaging", "Tools", 
                            "Office Supplies", "Website", "Other", "Jewelry Sales", 
                            "Custom Orders", "Repairs", "Consultation", "Workshops"]
        
        # Transaction form
        with st.form("add_transaction", clear_on_submit=True):
            # Transaction type at the top
            col_type1, col_type2, col_type3 = st.columns([1, 2, 1])
            with col_type2:
                if 'transaction_type' not in st.session_state:
                    st.session_state.transaction_type = "Income"
                
                trans_type = st.radio(
                    "Transaction Type", 
                    ["Income", "Expense"],
                    index=0 if st.session_state.transaction_type == "Income" else 1,
                    horizontal=True,
                    key="trans_type_radio"
                )
                
                # Update session state
                if trans_type != st.session_state.transaction_type:
                    st.session_state.transaction_type = trans_type
            
            # Main form columns
            col1, col2 = st.columns(2)
            
            with col1:
                amount = st.number_input("Amount (€)", min_value=0.01, value=50.0, step=1.0,
                                    help="Enter the transaction amount")
                
                # Category selection
                if categories_list:
                    category = st.selectbox("Category", categories_list, 
                                        help="Select or enter a category for this transaction")
                else:
                    category = st.text_input("Category", placeholder="Enter category name")
            
            with col2:
                date = st.date_input("Date", value=datetime.now(),
                                help="Transaction date")
                
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Bank Transfer", "Cash", "PayPal", "Other", "Bank Transfer"],
                    help="How was this transaction paid?")
            
            # ====== CUSTOMER & SUPPLIER SECTION - BOTH VISIBLE ======
            st.markdown("---")
            st.markdown("### 👥 Customer & Supplier Details")
            
            # Create two columns for Customer and Supplier
            cust_col, supp_col = st.columns(2)
            
            with cust_col:
                st.markdown(f"#### 👤 Customer {'✅' if trans_type == 'Income' else '⏸️'}")
                
                # Customer dropdown - enabled only for Income
                customer = st.selectbox(
                    "Select Customer", 
                    customers_list,
                    key="customer_select",
                    label_visibility="collapsed",
                    disabled=(trans_type == "Expense"),
                    help="Required for Income transactions" if trans_type == "Income" else "Disabled for Expense transactions"
                )
                
                # Show visual indicator
                if trans_type == "Income":
                    if customer == "Select Customer...":
                        st.warning("⚠️ Please select a customer for Income transaction")
                    else:
                        st.success("✅ Customer selected")
                else:
                    st.info("ℹ️ Customer selection disabled for Expenses")
            
            with supp_col:
                st.markdown(f"#### 🏭 Supplier {'✅' if trans_type == 'Expense' else '⏸️'}")
                
                # Supplier dropdown - enabled only for Expense
                supplier = st.selectbox(
                    "Select Supplier", 
                    suppliers_list,
                    key="supplier_select", 
                    label_visibility="collapsed",
                    disabled=(trans_type == "Income"),
                    help="Required for Expense transactions" if trans_type == "Expense" else "Disabled for Income transactions"
                )
                
                # Show visual indicator
                if trans_type == "Expense":
                    if supplier == "Select Supplier...":
                        st.warning("⚠️ Please select a supplier for Expense transaction")
                    else:
                        st.success("✅ Supplier selected")
                else:
                    st.info("ℹ️ Supplier selection disabled for Income")
            
            # Description
            st.markdown("---")
            description = st.text_area("Description", placeholder="Enter transaction details...", 
                                    help="Optional: Add notes about this transaction (e.g., product details, purpose, etc.)",
                                    height=100)
            
            # ====== VISUAL TYPE INDICATOR ======
            st.markdown("---")
            
            # Color-coded type indicator
            if trans_type == "Income":
                st.markdown(
                    '<div style="background-color: rgba(16, 185, 129, 0.2); padding: 15px; border-radius: 10px; border-left: 5px solid #10B981;">'
                    '<h4 style="color: #10B981; margin: 0;">📈 Income Transaction</h4>'
                    '<p style="margin: 5px 0 0 0; color: #94A3B8;">Money coming IN from a customer</p>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div style="background-color: rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 10px; border-left: 5px solid #EF4444;">'
                    '<h4 style="color: #EF4444; margin: 0;">📉 Expense Transaction</h4>'
                    '<p style="margin: 5px 0 0 0; color: #94A3B8;">Money going OUT to a supplier</p>'
                    '</div>',
                    unsafe_allow_html=True
                )
            
            # Form buttons
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                submitted = st.form_submit_button(
                    f"💾 Save {trans_type}", 
                    use_container_width=True,
                    type="primary"
                )
            with col2:
                if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                    # Clear form by rerunning
                    st.session_state.transaction_type = "Income"
                    st.rerun()
            with col3:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.info("Transaction cancelled")
            
            if submitted:
                # Validation
                validation_errors = []
                
                if amount <= 0:
                    validation_errors.append("❌ Amount must be greater than 0")
                
                if trans_type == "Income":
                    if customer == "Select Customer...":
                        validation_errors.append("❌ Please select a customer for Income transaction")
                    if supplier != "Select Supplier...":
                        st.warning("⚠️ Supplier selection will be ignored for Income transaction")
                
                if trans_type == "Expense":
                    if supplier == "Select Supplier...":
                        validation_errors.append("❌ Please select a supplier for Expense transaction")
                    if customer != "Select Customer...":
                        st.warning("⚠️ Customer selection will be ignored for Expense transaction")
                
                if not category:
                    validation_errors.append("❌ Category is required")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    # Prepare transaction data
                    transaction_data = {
                        "amount": float(amount),
                        "type": trans_type.lower(),
                        "category": category,
                        "description": description if description else None,
                        "transaction_date": date.isoformat(),
                        "payment_method": payment_method
                    }
                    
                    # Extract IDs from selection strings
                    try:
                        if trans_type == "Income":
                            # Extract customer ID from "Name (ID: X)"
                            customer_id = int(customer.split("(ID: ")[1].rstrip(")"))
                            transaction_data["customer_id"] = customer_id
                            transaction_data["supplier_id"] = None
                        
                        elif trans_type == "Expense":
                            # Extract supplier ID
                            supplier_id = int(supplier.split("(ID: ")[1].rstrip(")"))
                            transaction_data["supplier_id"] = supplier_id
                            transaction_data["customer_id"] = None
                            
                    except Exception as e:
                        st.error(f"❌ Error parsing ID from selection: {str(e)}")
                        st.info(f"Customer: {customer}" if trans_type == "Income" else f"Supplier: {supplier}")
                        return
                    
                    # Debug: Show what we're sending
                    with st.expander("🔍 Debug: Transaction Data", expanded=False):
                        st.json(transaction_data)
                    
                    # Send to backend
                    try:
                        with st.spinner(f"💾 Saving {trans_type.lower()}..."):
                            headers = auth.get_auth_header()
                            response = requests.post(
                                f"{st.session_state.api_url}/api/transactions",
                                json=transaction_data,
                                headers=headers,
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                saved_transaction = response.json()
                                
                                # Success message with details
                                success_col1, success_col2 = st.columns([3, 1])
                                with success_col1:
                                    st.success(f"✅ {trans_type} of €{amount:.2f} saved successfully!")
                                    
                                    # Show quick summary
                                    summary_html = f"""
                                    <div style="background-color: rgba(30, 41, 59, 0.8); padding: 15px; border-radius: 10px; margin-top: 10px;">
                                        <h4 style="color: #F1F5F9; margin: 0 0 10px 0;">📋 Transaction Summary</h4>
                                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                            <div><strong>Type:</strong> {trans_type}</div>
                                            <div><strong>Amount:</strong> €{amount:,.2f}</div>
                                            <div><strong>Category:</strong> {category}</div>
                                            <div><strong>Date:</strong> {date.strftime('%Y-%m-%d')}</div>
                                            <div><strong>Payment:</strong> {payment_method}</div>
                                            <div><strong>ID:</strong> {saved_transaction.get('id', 'N/A')}</div>
                                        </div>
                                    </div>
                                    """
                                    st.markdown(summary_html, unsafe_allow_html=True)
                                
                                with success_col2:
                                    st.balloons()
                                
                                # Auto-refresh after delay
                                time.sleep(3)
                                st.rerun()
                                
                            elif response.status_code == 422:
                                # Validation error from backend
                                error_data = response.json()
                                st.error(f"❌ Validation error: {error_data.get('detail', 'Unknown error')}")
                            else:
                                st.error(f"❌ Failed to save: {response.status_code} - {response.text[:200]}")
                                
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Could not connect to backend. Make sure server is running.")
                        st.info("Run: `uvicorn app.main:app --reload` in backend directory")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    
    # ========== TAB 2: ALL TRANSACTIONS ==========
    with tab2:
        st.subheader("📋 Transaction History")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            filter_type = st.selectbox("Type", ["All", "income", "expense"], key="filter_type")
        with col2:
            start_date = st.date_input("From", value=datetime.now() - timedelta(days=30), key="start_date")
        with col3:
            end_date = st.date_input("To", value=datetime.now(), key="end_date")
        with col4:
            limit = st.slider("Max rows", 10, 200, 50, key="limit_slider")
        
        # Fetch and display transactions
        try:
            with st.spinner("🔄 Loading transactions..."):
                headers = auth.get_auth_header()
                api_url = st.session_state.api_url
                
                # Build query params
                params = {"limit": limit}
                if filter_type != "All":
                    params["type"] = filter_type.lower()
                
                response = requests.get(
                    f"{api_url}/api/transactions",
                    headers=headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    transactions = response.json()
                    
                    # DEBUG: Show response structure
                    with st.expander("🔍 API Response Info", expanded=False):
                        if transactions:
                            st.write(f"Total transactions: {len(transactions)}")
                            st.json(transactions[0] if len(transactions) > 0 else {})
                    
                    if transactions:
                        # Convert to DataFrame
                        df = pd.DataFrame(transactions)
                        
                        # Handle date filtering
                        if 'transaction_date' in df.columns and not df.empty:
                            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
                            mask = (df['transaction_date'] >= pd.Timestamp(start_date)) & \
                                   (df['transaction_date'] <= pd.Timestamp(end_date))
                            df = df[mask]
                        
                        if not df.empty:
                            # Format for display
                            display_data = []
                            for _, row in df.iterrows():
                                # Format amount with color
                                amount = row.get('amount', 0)
                                amount_str = f"€{abs(amount):,.2f}"
                                
                                # Type with icon
                                trans_type = row.get('type', '').lower()
                                type_icon = "📈" if trans_type == 'income' else "📉"
                                type_display = f"{type_icon} {trans_type.title()}"
                                
                                # Date formatting
                                date_val = row.get('transaction_date')
                                date_str = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val)
                                
                                display_data.append({
                                    "ID": row.get('id', ''),
                                    "Date": date_str,
                                    "Type": type_display,
                                    "Category": row.get('category', ''),
                                    "Description": row.get('description', '')[:60],
                                    "Amount": amount_str,
                                    "Customer/Supplier": row.get('customer_id', row.get('supplier_id', '')),
                                    "Payment": row.get('payment_method', '')
                                })
                            
                            display_df = pd.DataFrame(display_data)
                            
                            # Display table
                            st.dataframe(
                                display_df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "ID": st.column_config.Column(width="small"),
                                    "Date": st.column_config.Column(width="small"),
                                    "Type": st.column_config.Column(width="small"),
                                    "Amount": st.column_config.Column(width="small"),
                                }
                            )
                            
                            # Statistics
                            total_income = sum(row['amount'] for _, row in df.iterrows() if row.get('type', '').lower() == 'income')
                            total_expense = sum(abs(row['amount']) for _, row in df.iterrows() if row.get('type', '').lower() == 'expense')
                            profit = total_income - total_expense
                            
                            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                            with stat_col1:
                                st.metric("📈 Total Income", f"€{total_income:,.2f}")
                            with stat_col2:
                                st.metric("📉 Total Expenses", f"€{total_expense:,.2f}")
                            with stat_col3:
                                st.metric("💰 Net Profit", f"€{profit:,.2f}", 
                                         delta=f"{(profit/(total_income if total_income > 0 else 1)*100):.1f}%")
                            with stat_col4:
                                st.metric("📊 Count", len(df))
                            
                            # Download option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv,
                                file_name=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                            
                        else:
                            st.info("📭 No transactions found in the selected date range")
                    else:
                        st.info("📭 No transactions found in database")
                        
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text[:200]}")
                    
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to backend API")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # ========== TAB 3: ANALYSIS ==========
    with tab3:
        st.subheader("📈 Transaction Analysis")
        
        # Create two columns for different analyses
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            st.markdown("#### 💰 Budget vs Actual")
            try:
                with st.spinner("Loading budget analysis..."):
                    headers = auth.get_auth_header()
                    response = requests.get(
                        f"{st.session_state.api_url}/api/budgets/analysis",
                        headers=headers,
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        analysis = response.json()
                        
                        if analysis:
                            # Summary metrics
                            total_budget = sum(item.get('budget_amount', 0) for item in analysis)
                            total_spent = sum(item.get('actual_spent', 0) for item in analysis)
                            total_remaining = total_budget - total_spent
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Budget", f"€{total_budget:,.2f}")
                            with col2:
                                st.metric("Total Spent", f"€{total_spent:,.2f}")
                            with col3:
                                st.metric("Remaining", f"€{total_remaining:,.2f}", 
                                         delta="Under" if total_remaining >= 0 else "Over")
                            
                            # Detailed breakdown
                            st.markdown("#### 📊 Budget Breakdown")
                            for item in analysis:
                                with st.expander(f"{item.get('budget_name', 'Unnamed')} - {item.get('status', 'N/A')}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.metric("Budget", f"€{item.get('budget_amount', 0):,.2f}")
                                        st.metric("Spent", f"€{item.get('actual_spent', 0):,.2f}")
                                    with col2:
                                        remaining = item.get('remaining', 0)
                                        st.metric("Remaining", f"€{remaining:,.2f}")
                                        percentage = item.get('percentage_used', 0)
                                        st.progress(min(percentage / 100, 1.0))
                                        st.caption(f"{percentage:.1f}% used")
                        else:
                            st.info("No budget data available")
                            
                    else:
                        st.info("Budget analysis endpoint not available")
                        
            except Exception as e:
                st.info(f"Budget analysis: {str(e)}")
        
        with analysis_col2:
            st.markdown("#### 📈 Monthly Trends")
            try:
                with st.spinner("Loading sales trends..."):
                    headers = auth.get_auth_header()
                    response = requests.get(
                        f"{st.session_state.api_url}/api/analytics/sales-trend",
                        headers=headers,
                        params={"months": 6},
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        trend_data = response.json()
                        
                        if trend_data:
                            # Create chart
                            trend_df = pd.DataFrame(trend_data)
                            fig = px.line(
                                trend_df, 
                                x='month', 
                                y='sales',
                                title='Monthly Sales Trend',
                                markers=True
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#F1F5F9'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Show stats
                            if len(trend_df) >= 2:
                                latest = trend_df.iloc[-1]['sales']
                                previous = trend_df.iloc[-2]['sales']
                                change = ((latest - previous) / previous * 100) if previous > 0 else 0
                                st.metric("Latest Month", f"€{latest:,.2f}", 
                                         delta=f"{change:.1f}%")
                        else:
                            st.info("No trend data available")
                            
                    else:
                        st.info("Sales trends endpoint not available")
                        
            except Exception as e:
                st.info(f"Sales trends: {str(e)}")
        
        # Additional analysis
        st.markdown("---")
        st.markdown("#### 🔍 Quick Insights")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            # Today's transactions
            try:
                today = datetime.now().date()
                headers = auth.get_auth_header()
                response = requests.get(
                    f"{st.session_state.api_url}/api/transactions",
                    headers=headers,
                    params={"limit": 100},
                    timeout=5
                )
                
                if response.status_code == 200:
                    transactions = response.json()
                    today_count = sum(1 for t in transactions 
                                    if pd.to_datetime(t.get('transaction_date', '')).date() == today)
                    st.metric("Today's Transactions", today_count)
                else:
                    st.metric("Today's Transactions", "N/A")
                    
            except:
                st.metric("Today's Transactions", "N/A")
        
        with insight_col2:
            # Top category
            try:
                headers = auth.get_auth_header()
                response = requests.get(
                    f"{st.session_state.api_url}/api/dashboard",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    dashboard_data = response.json()
                    expense_cats = dashboard_data.get('expense_categories', [])
                    if expense_cats:
                        top_cat = max(expense_cats, key=lambda x: x.get('total', 0))
                        st.metric("Top Expense", top_cat.get('category', 'N/A'))
                    else:
                        st.metric("Top Expense", "N/A")
                else:
                    st.metric("Top Expense", "N/A")
                    
            except:
                st.metric("Top Expense", "N/A")
        
        with insight_col3:
            # Recent activity
            st.metric("Last 7 Days", "Check Dashboard")

# Customers real backend data mode
def show_customers_page():
    """Customers management page with real backend data"""
    st.markdown('<h1 class="main-header">👥 Customer Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Customer Directory", "➕ Add Customer", "📊 Insights"])
    
    with tab1:
        search_query = st.text_input("🔍 Search customers...", placeholder="Name, email, or Instagram")
        
        try:
            # Fetch real customers from backend
            headers = auth.get_auth_header()
            api_url = st.session_state.api_url
            
            # Check if we should search or get all customers
            if search_query and len(search_query) >= 2:
                # Use search endpoint
                with st.spinner("🔍 Searching customers..."):
                    response = requests.get(
                        f"{api_url}/api/customers/search",
                        headers=headers,
                        params={"q": search_query, "limit": 50},
                        timeout=5
                    )
            else:
                # Get all customers
                with st.spinner("🔄 Loading customers..."):
                    response = requests.get(
                        f"{api_url}/api/customers",
                        headers=headers,
                        timeout=5
                    )
            
            if response.status_code == 200:
                customers_data = response.json()
                
                # DEBUG: Show what fields we actually get
                with st.expander("🔍 Debug: API Response Sample", expanded=False):
                    if customers_data:
                        st.json(customers_data[0] if len(customers_data) > 0 else {})
                        st.write(f"Total customers: {len(customers_data)}")
                
                if customers_data:
                    # Convert to DataFrame
                    customers_df = pd.DataFrame(customers_data)
                    
                    # DEBUG: Show available columns
                    st.caption(f"📊 Available columns: {', '.join(customers_df.columns.tolist())}")
                    
                    # Format columns - handle missing fields gracefully
                    if 'total_spent' in customers_df.columns:
                        customers_df['total_spent'] = customers_df['total_spent'].apply(lambda x: f"€{float(x):,.2f}")
                    
                    # Check for last_purchase field (might be missing or named differently)
                    if 'last_purchase' not in customers_df.columns:
                        # Check for alternative names
                        possible_date_fields = ['last_purchase_date', 'last_order_date', 'updated_at', 'created_at']
                        date_field_found = None
                        
                        for field in possible_date_fields:
                            if field in customers_df.columns:
                                date_field_found = field
                                break
                        
                        if date_field_found:
                            customers_df['last_purchase'] = customers_df[date_field_found]
                        else:
                            # If no date field found, use placeholder
                            customers_df['last_purchase'] = 'N/A'
                    
                    # Format date if present
                    if 'last_purchase' in customers_df.columns and customers_df['last_purchase'].notna().any():
                        try:
                            customers_df['last_purchase'] = pd.to_datetime(customers_df['last_purchase']).dt.strftime('%Y-%m-%d')
                        except:
                            # If date parsing fails, keep as is
                            pass
                    
                    # Create display DataFrame with safe field access
                    display_data = []
                    for _, row in customers_df.iterrows():
                        display_data.append({
                            "ID": row.get('id', 'N/A'),
                            "Name": row.get('name', 'N/A'),
                            "Email": row.get('email', 'N/A'),
                            "Instagram": f"@{row.get('instagram_handle', '')}" if row.get('instagram_handle') else '',
                            "Total Spent": row.get('total_spent', '€0.00'),
                            "Last Purchase": row.get('last_purchase', 'N/A'),
                            "Customer Since": row.get('customer_since', 'N/A') if 'customer_since' in row else 'N/A',
                            "Phone": row.get('phone', '') if 'phone' in row else ''
                        })
                    
                    display_df = pd.DataFrame(display_data)
                    
                    # Filter by search if needed
                    if search_query:
                        mask = (
                            display_df['Name'].str.contains(search_query, case=False, na=False) |
                            display_df['Email'].str.contains(search_query, case=False, na=False) |
                            display_df['Instagram'].str.contains(search_query, case=False, na=False)
                        )
                        display_df = display_df[mask]
                    
                    # Display with better formatting
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "ID": st.column_config.Column(width="small"),
                            "Total Spent": st.column_config.Column(width="medium"),
                            "Last Purchase": st.column_config.Column(width="medium"),
                            "Instagram": st.column_config.Column(width="small")
                        }
                    )
                    
                    # Show stats
                    st.caption(f"📊 Showing {len(display_df)} customers")
                    
                    # Quick actions for customers
                    if not display_df.empty:
                        st.subheader("🛠️ Quick Actions")
                        
                        action_col1, action_col2, action_col3 = st.columns(3)
                        
                        with action_col1:
                            if st.button("📥 Export to CSV", use_container_width=True):
                                csv = display_df.to_csv(index=False)
                                st.download_button(
                                    label="⬇️ Download CSV",
                                    data=csv,
                                    file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                        
                        with action_col2:
                            if st.button("📧 Email Selected", use_container_width=True):
                                st.info("Email functionality coming soon!")
                        
                        with action_col3:
                            if st.button("🔄 Refresh", use_container_width=True):
                                st.rerun()
                
                else:
                    st.info("📭 No customers found in database")
                    if search_query:
                        st.markdown(f"No customers matching **'{search_query}'**")
                    
                    # Show option to add customers
                    st.markdown("---")
                    st.subheader("👥 No Customers Yet")
                    st.markdown("""
                    **Get started by adding your first customer:**
                    1. Go to the **"➕ Add Customer"** tab
                    2. Fill in customer details
                    3. Save to database
                    4. Customers will appear here automatically
                    """)
            
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text[:200]}")
                # Fallback to demo data
                show_demo_customers(search_query)
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to backend")
            show_demo_customers(search_query)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())
            show_demo_customers(search_query)
    
    with tab2:
        with st.form("add_customer", clear_on_submit=True):
            st.subheader("➕ Add New Customer")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="Maria Silva")
                email = st.text_input("Email", placeholder="maria@email.com")
                phone = st.text_input("Phone", placeholder="+1234567890")
            
            with col2:
                instagram = st.text_input("Instagram Handle", placeholder="@maria_silva")
                customer_since = st.date_input("Customer Since", value=datetime.now())
                total_spent = st.number_input("Initial Total Spent (€)", min_value=0.0, value=0.0, step=10.0)
            
            notes = st.text_area("Notes", placeholder="Additional information about this customer...")
            
            submitted = st.form_submit_button("💾 Save Customer", use_container_width=True, type="primary")
            
            if submitted:
                if not name:
                    st.error("❌ Name is required!")
                else:
                    try:
                        # Prepare customer data
                        customer_data = {
                            "name": name,
                            "email": email if email else None,
                            "instagram_handle": instagram if instagram else None,
                            "total_spent": total_spent,
                            "customer_since": customer_since.isoformat()
                        }
                        
                        # Send to backend
                        headers = auth.get_auth_header()
                        response = requests.post(
                            f"{st.session_state.api_url}/api/customers",
                            json=customer_data,
                            headers=headers,
                            timeout=5
                        )
                        
                        if response.status_code == 200:
                            new_customer = response.json()
                            st.success(f"✅ Customer '{name}' added successfully! (ID: {new_customer['id']})")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to add customer: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.subheader("📊 Customer Insights")
        
        try:
            # Fetch customer analytics
            headers = auth.get_auth_header()
            response = requests.get(
                f"{st.session_state.api_url}/api/analytics/customer-segments",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                segments = response.json()
                
                # Display segment stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_customers = sum(segments[segment]['count'] for segment in segments)
                    st.metric("Total Customers", total_customers)
                
                with col2:
                    new_customers = segments.get('new', {}).get('count', 0)
                    st.metric("New Customers", new_customers)
                
                with col3:
                    vip_customers = segments.get('vip', {}).get('count', 0)
                    st.metric("VIP Customers", vip_customers)
                
                with col4:
                    total_revenue = sum(segments[segment]['total_spent'] for segment in segments)
                    st.metric("Total Revenue", f"€{total_revenue:,.2f}")
                
                # Customer segments visualization
                st.subheader("👥 Customer Segments")
                
                segments_data = []
                for segment, data in segments.items():
                    if data['count'] > 0:
                        segments_data.append({
                            'Segment': segment.title(),
                            'Count': data['count'],
                            'Avg. Spend': f"€{data.get('avg_spent', 0):,.2f}",
                            'Total Revenue': f"€{data.get('total_spent', 0):,.2f}"
                        })
                
                if segments_data:
                    segments_df = pd.DataFrame(segments_data)
                    st.dataframe(segments_df, use_container_width=True, hide_index=True)
                    
                    # Pie chart
                    fig = px.pie(
                        segments_df, 
                        values='Count', 
                        names='Segment',
                        title='Customer Distribution by Segment',
                        hole=0.3
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#F1F5F9'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No customer segment data available")
            
            else:
                # Fallback to demo insights
                show_demo_insights()
                
        except:
            # Fallback to demo insights
            show_demo_insights()

def show_demo_customers(search_query=None):
    """Fallback demo customers data"""
    st.warning("🎮 Using demo customer data")
    
    customers = pd.DataFrame({
        'ID': range(1, 11),
        'Name': ['Maria Silva', 'John Doe', 'Anna Smith', 'Luca Rossi', 'Sophie Chen',
                'Marcus Lee', 'Isabella Garcia', 'Oliver Smith', 'Chloe Williams', 'Noah Brown'],
        'Email': ['maria@email.com', 'john@email.com', 'anna@email.com', 'luca@email.com', 'sophie@email.com',
                 'marcus@email.com', 'bella@email.com', 'oliver@email.com', 'chloe@email.com', 'noah@email.com'],
        'Instagram': ['@maria_silva', '@john_jewelry', '@anna_sparkle', '@luca_designs', '@sophie_style',
                     '@marcus_creates', '@bella_jewelry', '@oliver_smith', '@chloe_designs', '@noah_brown'],
        'Total Spent': ['€1,250.75', '€890.50', '€2,100.00', '€750.25', '€1,850.00', 
                       '€620.80', '€1,450.30', '€980.45', '€1,120.60', '€830.25'],
        'Last Purchase': ['2024-12-10', '2024-12-05', '2024-12-01', '2024-11-28', '2024-11-25',
                         '2024-11-20', '2024-11-15', '2024-11-10', '2024-11-05', '2024-10-30']
    })
    
    if search_query:
        mask = (customers['Name'].str.contains(search_query, case=False) |
                customers['Email'].str.contains(search_query, case=False) |
                customers['Instagram'].str.contains(search_query, case=False))
        customers = customers[mask]
    
    st.dataframe(customers, use_container_width=True, hide_index=True)

def show_demo_insights():
    """Fallback demo insights"""
    st.warning("🎮 Using demo insights data")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", "124")
    with col2:
        st.metric("Avg. Spend", "€1,245.50")
    with col3:
        st.metric("Revenue", "€154,842")
    
    # Demo segments
    segments_data = [
        {'Segment': 'New', 'Count': 45, 'Avg. Spend': '€125.50', 'Total Revenue': '€5,647.50'},
        {'Segment': 'Regular', 'Count': 62, 'Avg. Spend': '€850.75', 'Total Revenue': '€52,746.50'},
        {'Segment': 'VIP', 'Count': 12, 'Avg. Spend': '€2,450.25', 'Total Revenue': '€29,403.00'},
        {'Segment': 'Premium', 'Count': 5, 'Avg. Spend': '€5,250.00', 'Total Revenue': '€26,250.00'}
    ]
    
    segments_df = pd.DataFrame(segments_data)
    st.dataframe(segments_df, use_container_width=True, hide_index=True)

# ========== MAIN APP FUNCTION ==========
def main_app():
    """Main application after login"""
    
    apply_dark_theme()
    
    username = auth.get_username()
    user_role = auth.get_user_role()
    
    if 'api_url' not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        # Logo and user info
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 3rem;">💎</div>
            <h2 style="margin: 0;">Shiny Jar</h2>
            <p style="color: #94A3B8; font-size: 0.9rem;">Jewelry CRM Suite</p>
            
            <div style="
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 0.75rem;
                margin: 1rem 0;
            ">
                <p style="margin: 0; font-weight: 600;">👤 {username}</p>
                <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">{user_role.title()}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Logout button - FIXED: No icon parameter
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # API Status
        try:
            response = requests.get(f"{st.session_state.api_url}/health", timeout=2)
            if response.status_code == 200:
                st.markdown('<div class="api-connected">✅ API Connected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="api-disconnected">❌ API Error</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="api-disconnected">🌐 API Not Connected</div>', unsafe_allow_html=True)
            if auth.is_demo_mode():
                st.info("🎮 Using demo data")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 📱 Navigation")
        
        if user_role == "customer":
            pages = ["My Dashboard", "My Orders", "My Invoices", "My Profile"]
            page_titles = ["📊 My Dashboard", "🛍️ My Orders", "💳 My Invoices", "👤 My Profile"]
        elif user_role == "supplier":
            pages = ["My Dashboard", "My Orders", "My Products", "My Payments", "My Profile"]
            page_titles = ["📊 My Dashboard", "📦 My Orders", "📋 My Products", "💰 My Payments", "👤 My Profile"]
        else:
            pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Inventory", "Budget", "Analytics", "Reports"]
            page_titles = ["📊 Dashboard", "💰 Expenses", "👥 Customers", "🏭 Suppliers", "📦 Inventory" "📋 Budget", "📈 Analytics", "📊 Reports"]
            page_icons = ["📊", "💰", "👥", "🏭", "📦", "📋", "📈", "📊"]
        
        if 'page' not in st.session_state:
            st.session_state.page = pages[0]
        
        # Navigation radio
        selected_title = st.radio("Choose page:", page_titles, label_visibility="collapsed")
        
        selected_page = pages[page_titles.index(selected_title)]
        
        if selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Settings
        with st.expander("⚙️ Settings"):
            new_url = st.text_input("API URL", value=st.session_state.api_url)
            if st.button("Update URL", use_container_width=True):
                st.session_state.api_url = new_url
                st.success("URL updated!")
    
    # ========== MAIN CONTENT ==========
    
    current_page = st.session_state.page
    
    # Route to appropriate page based on role
    if user_role == "customer":
        if current_page == "My Dashboard":
            if CUSTOMER_PAGES_AVAILABLE:
                show_customer_dashboard()
            else:
                st.info("👤 Customer Dashboard - Page module not loaded")
        elif current_page == "My Orders":
            if CUSTOMER_PAGES_AVAILABLE:
                show_customer_orders()
            else:
                st.info("🛍️ Customer Orders - Page module not loaded")
        elif current_page == "My Invoices":
            if CUSTOMER_PAGES_AVAILABLE:
                show_customer_invoices()
            else:
                st.info("💳 Customer Invoices - Page module not loaded")
        elif current_page == "My Profile":
            if CUSTOMER_PAGES_AVAILABLE:
                show_customer_profile()
            else:
                st.info("👤 Customer Profile - Page module not loaded")
    
    elif user_role == "supplier":
        if current_page == "My Dashboard":
            if SUPPLIER_PAGES_AVAILABLE:
                show_supplier_dashboard()
            else:
                st.info("🏭 Supplier Dashboard - Page module not loaded")
        elif current_page == "My Orders":
            if SUPPLIER_PAGES_AVAILABLE:
                show_supplier_orders()
            else:
                st.info("📦 Supplier Orders - Page module not loaded")
        elif current_page == "My Products":
            if SUPPLIER_PAGES_AVAILABLE:
                show_supplier_products()
            else:
                st.info("📋 Supplier Products - Page module not loaded")
        elif current_page == "My Payments":
            if SUPPLIER_PAGES_AVAILABLE:
                show_supplier_payments()
            else:
                st.info("💰 Supplier Payments - Page module not loaded")
        elif current_page == "My Profile":
            if SUPPLIER_PAGES_AVAILABLE:
                show_supplier_profile()
            else:
                st.info("🏢 Supplier Profile - Page module not loaded")
    
    # Update admin routing section:
    else:  # admin/demo user
        if current_page == "Dashboard":
            show_dashboard()
        elif current_page == "Expenses":
            show_expenses_page()
        elif current_page == "Customers":
            show_customers_page()
        elif current_page == "Suppliers":
            if PAGES_AVAILABLE:
                show_suppliers_page()
            else:
                st.info("🏭 Supplier Management")
        elif current_page == "Inventory":
            if INVENTORY_AVAILABLE:
                show_inventory_page()
            else:
                st.info("📦 Inventory Management")
        elif current_page == "Budget":
            if PAGES_AVAILABLE:
                show_budget_page()
            else:
                st.info("📋 Budget Management")
        elif current_page == "Analytics":
            if PAGES_AVAILABLE:
                show_analytics_page()
            else:
                st.info("📈 Advanced Analytics")
        elif current_page == "Reports":
            if PAGES_AVAILABLE:
                show_reports_page()
            else:
                st.info("📊 Professional Reports")

def show_customer_demo_dashboard():
    """Demo customer dashboard"""
    st.markdown('<h1 class="main-header">👤 Customer Portal</h1>', unsafe_allow_html=True)
    st.info("🎮 Demo Mode - Customer View")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", "€1,250.75")
    with col2:
        st.metric("Orders", "12")
    with col3:
        st.metric("Loyalty Points", "125")
    with col4:
        st.metric("Saved Items", "8")
    
    st.subheader("🛍️ Recent Orders")
    orders = pd.DataFrame({
        'Date': ['2024-12-10', '2024-12-05', '2024-11-28'],
        'Order #': ['ORD-00123', 'ORD-00122', 'ORD-00121'],
        'Items': ['Silver Necklace', 'Gold Earrings', 'Custom Bracelet'],
        'Amount': ['€89.00', '€145.50', '€220.00'],
        'Status': ['Delivered', 'Shipped', 'Delivered']
    })
    
    st.dataframe(orders, use_container_width=True, hide_index=True)

def show_supplier_demo_dashboard():
    """Demo supplier dashboard"""
    st.markdown('<h1 class="main-header">🏭 Supplier Portal</h1>', unsafe_allow_html=True)
    st.info("🎮 Demo Mode - Supplier View")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Revenue YTD", "€12,450")
    with col2:
        st.metric("Orders", "48")
    with col3:
        st.metric("Rating", "4.7/5")
    with col4:
        st.metric("On-time", "98%")
    
    st.subheader("📦 Recent Orders")
    orders = pd.DataFrame({
        'Date': ['2024-12-10', '2024-12-08', '2024-12-05'],
        'PO #': ['PO-2024-123', 'PO-2024-122', 'PO-2024-121'],
        'Items': ['Silver Chains', 'Gold Hooks', 'Crystals'],
        'Amount': ['€255.00', '€150.00', '€450.00'],
        'Status': ['Delivered', 'Shipped', 'Delivered']
    })
    
    st.dataframe(orders, use_container_width=True, hide_index=True)

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    if AUTH_AVAILABLE and not auth.is_authenticated():
        show_login_page()
    else:
        main_app()
