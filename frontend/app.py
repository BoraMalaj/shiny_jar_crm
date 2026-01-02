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
    from pages.budget import show_budget_page           #, show_budget_alerts, show_budget_analysis, show_budget_overview, show_create_budget
    from pages.suppliers import show_suppliers_page     #, show_add_supplier, show_all_suppliers, show_purchase_history, show_supplier_performance
    from pages.analytics import show_analytics_page     #, show_business_intelligence, show_customer_insights, show_profit_analysis, show_sales_forecasting
    from pages.reports import show_reports_page         #, show_custom_reports, show_customer_reports, show_financial_reports, show_supplier_reports
    # from pages.inventory import show_inventory_page, generate_inventory_report
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

#========== PAGE FUNCTIONS ==========

#=========== Demo Dashboard ==========
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
#=========== End of Demo Dashboard ===========

# Quick actions handling
def handle_quick_action(action, item_id=None):
    """Handle quick action buttons - placeholder"""
    if action == "receive":
        st.session_state.inventory_action = "receive"
        if item_id:
            st.session_state.receiving_item_id = item_id
        st.info("📥 Redirecting to Receive Stock tab...")
    elif action == "adjust":
        st.session_state.inventory_action = "adjust"
        if item_id:
            st.session_state.adjusting_item_id = item_id
        st.info("📤 Redirecting to Adjust Stock...")
    elif action == "view_alerts":
        st.info("🔔 Redirecting to Low Stock tab...")
    # we can add more actions usting the logic above, as needed

#=========================================
# Dashboard area - real data from backend
#=========================================

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

#==================================================================================
# Customers area - directory, management and insights
#==================================================================================

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

#==================================================================================
# Transactions area - expenses by supplier and incomings by customer plus analysis
#==================================================================================

def show_expenses_page():
    """Expenses management page - CLEAN 5-TAB VERSION"""
    st.markdown('<h1 class="main-header">💰 Transaction Management</h1>', unsafe_allow_html=True)
    
    # 5 Tabs as per your brilliant suggestion
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 New Income", 
        "📉 New Expense", 
        "📋 All Transactions",
        "📈 Income Analysis",
        "📊 Expense Analysis"
    ])
    
    # ========== TAB 1: NEW INCOME ==========
    with tab1:
        show_new_income_form()
    
    # ========== TAB 2: NEW EXPENSE ==========
    with tab2:
        show_new_expense_form()
    
    # ========== TAB 3: ALL TRANSACTIONS ==========
    with tab3:
        show_all_transactions()
    
    # ========== TAB 4: INCOME ANALYSIS ==========
    with tab4:
        show_income_analysis()
    
    # ========== TAB 5: EXPENSE ANALYSIS ==========
    with tab5:
        show_expense_analysis()


# ========== HELPER FUNCTIONS ==========

def show_new_income_form():
    """Dedicated income form - clean and focused"""
    st.subheader("💰 Add New Income")
    st.info("📈 Record money coming IN from customers")
    
    # Fetch data
    customers_list = ["Select Customer..."]
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
        
        # Fetch income categories
        with st.spinner("🔄 Loading categories..."):
            response = requests.get(f"{api_url}/api/categories", headers=headers, timeout=3)
            if response.status_code == 200:
                cat_data = response.json()
                categories_list = cat_data.get('income_categories', [])
                
    except Exception as e:
        st.warning(f"⚠️ Could not fetch data: {str(e)}")
        categories_list = ["Jewelry Sales", "Custom Orders", "Repairs", "Consultation", "Workshops", "Other"]
    
    # Income form
    with st.form("add_income", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (€)", min_value=0.01, value=50.0, step=1.0,
                                   key="income_amount")
            
            # Customer selection
            customer = st.selectbox(
                "Customer *", 
                customers_list,
                key="income_customer",
                help="Select the customer who made this purchase"
            )
        
        with col2:
            date = st.date_input("Date", value=datetime.now(), key="income_date")
            
            payment_method = st.selectbox("Payment Method", 
                ["Credit Card", "Bank Transfer", "Cash", "PayPal", "Other"],
                key="income_payment")
            
            # Category for income
            if categories_list:
                category = st.selectbox("Category", categories_list, key="income_category")
            else:
                category = st.text_input("Category", placeholder="Income category", key="income_category_text")
        
        description = st.text_area("Description", placeholder="What was sold? Order details...", 
                                 key="income_desc", height=80)
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Income", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if customer == "Select Customer...":
                st.error("❌ Please select a customer")
            elif amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                # Prepare data
                transaction_data = {
                    "amount": float(amount),
                    "type": "income",
                    "category": category,
                    "description": description if description else None,
                    "transaction_date": date.isoformat(),
                    "payment_method": payment_method
                }
                
                # Extract customer ID
                try:
                    customer_id = int(customer.split("(ID: ")[1].rstrip(")"))
                    transaction_data["customer_id"] = customer_id
                except:
                    st.error("❌ Error parsing customer ID")
                    return
                
                # Save to backend
                save_transaction(transaction_data, "Income")


def show_new_expense_form():
    """Dedicated expense form - clean and focused"""
    st.subheader("📉 Add New Expense")
    st.info("💰 Record money going OUT to suppliers")
    
    # Fetch data
    suppliers_list = ["Select Supplier..."]
    categories_list = []
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        # Fetch suppliers
        with st.spinner("🔄 Loading suppliers..."):
            response = requests.get(f"{api_url}/api/suppliers", headers=headers, timeout=5)
            if response.status_code == 200:
                suppliers = response.json()
                suppliers_list += [f"{s['name']} (ID: {s['id']})" for s in suppliers]
        
        # Fetch expense categories
        with st.spinner("🔄 Loading categories..."):
            response = requests.get(f"{api_url}/api/categories", headers=headers, timeout=3)
            if response.status_code == 200:
                cat_data = response.json()
                categories_list = cat_data.get('expense_categories', [])
                
    except Exception as e:
        st.warning(f"⚠️ Could not fetch data: {str(e)}")
        categories_list = ["Materials", "Shipping", "Packaging", "Marketing", "Tools", 
                         "Office Supplies", "Website", "Other"]
    
    # Expense form
    with st.form("add_expense", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (€)", min_value=0.01, value=50.0, step=1.0,
                                   key="expense_amount")
            
            # Supplier selection
            supplier = st.selectbox(
                "Supplier *", 
                suppliers_list,
                key="expense_supplier",
                help="Select the supplier for this expense"
            )
        
        with col2:
            date = st.date_input("Date", value=datetime.now(), key="expense_date")
            
            payment_method = st.selectbox("Payment Method", 
                ["Credit Card", "Bank Transfer", "Cash", "PayPal", "Other"],
                key="expense_payment")
            
            # Category for expense
            if categories_list:
                category = st.selectbox("Category", categories_list, key="expense_category")
            else:
                category = st.text_input("Category", placeholder="Expense category", key="expense_category_text")
        
        description = st.text_area("Description", placeholder="What was purchased? Expense details...", 
                                 key="expense_desc", height=80)
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Expense", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if supplier == "Select Supplier...":
                st.error("❌ Please select a supplier")
            elif amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                # Prepare data
                transaction_data = {
                    "amount": float(amount),
                    "type": "expense",
                    "category": category,
                    "description": description if description else None,
                    "transaction_date": date.isoformat(),
                    "payment_method": payment_method
                }
                
                # Extract supplier ID
                try:
                    supplier_id = int(supplier.split("(ID: ")[1].rstrip(")"))
                    transaction_data["supplier_id"] = supplier_id
                except:
                    st.error("❌ Error parsing supplier ID")
                    return
                
                # Save to backend
                save_transaction(transaction_data, "Expense")


def save_transaction(transaction_data, trans_type):
    """Save transaction to backend - reusable function"""
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
                st.success(f"✅ {trans_type} of €{transaction_data['amount']:.2f} saved!")
                st.balloons()
                
                # Show success card
                st.markdown(f"""
                <div style="background-color: rgba(30, 41, 59, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4 style="color: #F1F5F9; margin: 0 0 10px 0;">✅ Transaction Saved</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem;">
                        <div><strong>ID:</strong> {saved_transaction.get('id', 'N/A')}</div>
                        <div><strong>Type:</strong> {trans_type}</div>
                        <div><strong>Amount:</strong> €{transaction_data['amount']:,.2f}</div>
                        <div><strong>Category:</strong> {transaction_data['category']}</div>
                        <div><strong>Date:</strong> {transaction_data['transaction_date'][:10]}</div>
                        <div><strong>Payment:</strong> {transaction_data['payment_method']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-refresh
                time.sleep(3)
                st.rerun()
                
            elif response.status_code == 422:
                error_data = response.json()
                st.error(f"❌ Validation error: {error_data.get('detail', 'Unknown error')}")
            else:
                st.error(f"❌ Failed to save: {response.status_code} - {response.text[:200]}")
                
    except requests.exceptions.ConnectionError:
        st.error("🔌 Could not connect to backend. Make sure server is running.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_all_transactions():
    """Show all transactions with filtering"""
    st.subheader("📋 All Transactions")
    
    # Filters in columns
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
    
    with col1:
        trans_type = st.selectbox("Type", ["All", "Income", "Expense"], key="filter_type_all")
    
    with col2:
        start_date = st.date_input("From", value=datetime.now() - timedelta(days=30), key="start_date_all")
    
    with col3:
        end_date = st.date_input("To", value=datetime.now(), key="end_date_all")
    
    with col4:
        limit = st.selectbox("Rows", [50, 100, 200, 500], index=0, key="limit_all")
    
    with col5:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Customer/Supplier search
    search_query = st.text_input("🔍 Search by customer/supplier name...", 
                               placeholder="Enter name to search...",
                               key="search_all")
    
    # Fetch transactions
    try:
        with st.spinner("🔄 Loading transactions..."):
            headers = auth.get_auth_header()
            api_url = st.session_state.api_url
            
            # Get all transactions first
            response = requests.get(
                f"{api_url}/api/transactions",
                headers=headers,
                params={"limit": 1000},  # Get more for filtering
                timeout=10
            )
            
            if response.status_code == 200:
                transactions = response.json()
                
                if transactions:
                    # Convert to DataFrame
                    df = pd.DataFrame(transactions)
                    
                    # Filter by type
                    if trans_type != "All":
                        df = df[df['type'].str.lower() == trans_type.lower()]
                    
                    # Filter by date
                    if 'transaction_date' in df.columns:
                        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
                        mask = (df['transaction_date'] >= pd.Timestamp(start_date)) & \
                               (df['transaction_date'] <= pd.Timestamp(end_date))
                        df = df[mask]
                    
                    # Filter by search query
                    if search_query:
                        # We need to fetch customer/supplier names (backend might not include them)
                        # For now, filter by ID or other visible fields
                        mask = (
                            df['category'].str.contains(search_query, case=False, na=False) |
                            df['description'].str.contains(search_query, case=False, na=False)
                        )
                        df = df[mask]
                    
                    # Limit rows
                    df = df.head(limit)
                    
                    if not df.empty:
                        # Format for display
                        display_data = []
                        for _, row in df.iterrows():
                            amount = row.get('amount', 0)
                            trans_type = row.get('type', '').lower()
                            
                            display_data.append({
                                "ID": row.get('id', ''),
                                "Date": row.get('transaction_date').strftime('%Y-%m-%d') if hasattr(row.get('transaction_date'), 'strftime') else str(row.get('transaction_date', '')),
                                "Type": f"📈 {trans_type.title()}" if trans_type == 'income' else f"📉 {trans_type.title()}",
                                "Category": row.get('category', ''),
                                "Description": (row.get('description', '')[:50] + '...') if row.get('description') and len(row.get('description')) > 50 else row.get('description', ''),
                                "Amount": f"€{abs(amount):,.2f}",
                                "Customer ID": row.get('customer_id', ''),
                                "Supplier ID": row.get('supplier_id', '')
                            })
                        
                        display_df = pd.DataFrame(display_data)
                        
                        # Display table
                        st.dataframe(
                            display_df,
                            use_container_width=True,
                            hide_index=True,
                            height=400
                        )
                        
                        # Stats
                        total_income = sum(row['amount'] for _, row in df.iterrows() if row.get('type', '').lower() == 'income')
                        total_expense = sum(abs(row['amount']) for _, row in df.iterrows() if row.get('type', '').lower() == 'expense')
                        
                        stat_col1, stat_col2, stat_col3 = st.columns(3)
                        with stat_col1:
                            st.metric("📈 Total Income", f"€{total_income:,.2f}")
                        with stat_col2:
                            st.metric("📉 Total Expenses", f"€{total_expense:,.2f}")
                        with stat_col3:
                            profit = total_income - total_expense
                            st.metric("💰 Net Profit", f"€{profit:,.2f}")
                        
                        # Download
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"all_transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    else:
                        st.info("📭 No transactions found with current filters")
                else:
                    st.info("📭 No transactions in database")
            else:
                st.error(f"❌ API Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_income_analysis():
    """Income-focused analysis"""
    st.subheader("📈 Income Analysis")
    st.info("Analysis of all income transactions")
    
    # Placeholder for now - we'll implement full analysis
    st.write("""
    ### 💡 Income Analytics Coming Soon:
    
    - **Monthly income trends**
    - **Top customers by revenue**
    - **Income by category breakdown**
    - **Seasonal patterns**
    - **Revenue forecasts**
    
    This tab will show detailed analysis of all income transactions.
    """)
    
    # Quick stats
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/transactions",
            headers=headers,
            params={"type": "income", "limit": 1000},
            timeout=5
        )
        
        if response.status_code == 200:
            incomes = response.json()
            if incomes:
                total_income = sum(t['amount'] for t in incomes)
                avg_income = total_income / len(incomes) if len(incomes) > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Income", f"€{total_income:,.2f}")
                with col2:
                    st.metric("Transaction Count", len(incomes))
                with col3:
                    st.metric("Average Income", f"€{avg_income:,.2f}")
    except:
        pass


def show_expense_analysis():
    """Expense-focused analysis"""
    st.subheader("📊 Expense Analysis")
    st.info("Analysis of all expense transactions")
    
    # Placeholder for now - we'll implement full analysis
    st.write("""
    ### 💡 Expense Analytics Coming Soon:
    
    - **Monthly expense trends**
    - **Top suppliers by cost**
    - **Expense by category breakdown**
    - **Cost optimization insights**
    - **Budget vs actual comparison**
    
    This tab will show detailed analysis of all expense transactions.
    """)
    
    # Quick stats
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/transactions",
            headers=headers,
            params={"type": "expense", "limit": 1000},
            timeout=5
        )
        
        if response.status_code == 200:
            expenses = response.json()
            if expenses:
                total_expense = sum(abs(t['amount']) for t in expenses)
                avg_expense = total_expense / len(expenses) if len(expenses) > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Expenses", f"€{total_expense:,.2f}")
                with col2:
                    st.metric("Transaction Count", len(expenses))
                with col3:
                    st.metric("Average Expense", f"€{avg_expense:,.2f}")
    except:
        pass

#=====================================================
# Suppliers area - directory, management, analytics
#=====================================================

def show_suppliers_page():
    """Complete Suppliers Management Page"""
    st.markdown('<h1 class="main-header">🏭 Supplier Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Supplier Directory", "➕ Add Supplier", "📊 Supplier Analytics"])
    
    with tab1:
        show_supplier_directory()
    
    with tab2:
        show_add_supplier_form()
    
    with tab3:
        show_supplier_analytics()


def show_supplier_directory():
    """Show all suppliers with search and actions"""
    st.subheader("📋 Supplier Directory")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search suppliers...", placeholder="Name, email, contact person",
                                    key="supp_search")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True, key="supp_refresh"):
            st.rerun()
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        with st.spinner("🔄 Loading suppliers..."):
            response = requests.get(f"{api_url}/api/suppliers", headers=headers, timeout=10)
            
            if response.status_code == 200:
                suppliers = response.json()
                
                if suppliers:
                    # Create display data
                    display_data = []
                    for supplier in suppliers:
                        display_data.append({
                            "ID": supplier.get('id', ''),
                            "Name": supplier.get('name', ''),
                            "Contact Person": supplier.get('contact_person', ''),
                            "Email": supplier.get('email', ''),
                            "Phone": supplier.get('phone', ''),
                            "Website": supplier.get('website', ''),
                            "Address": (supplier.get('address', '')[:30] + '...') if supplier.get('address') and len(supplier.get('address')) > 30 else supplier.get('address', ''),
                            "Notes": (supplier.get('notes', '')[:30] + '...') if supplier.get('notes') and len(supplier.get('notes')) > 30 else supplier.get('notes', ''),
                            "Created": supplier.get('created_at', '')[:10] if supplier.get('created_at') else ''
                        })
                    
                    # Apply search filter
                    if search_query:
                        filtered_data = [s for s in display_data 
                                       if search_query.lower() in s['Name'].lower()
                                       or search_query.lower() in s['Email'].lower()
                                       or search_query.lower() in s['Contact Person'].lower()]
                    else:
                        filtered_data = display_data
                    
                    if filtered_data:
                        df = pd.DataFrame(filtered_data)
                        
                        # Display table
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "ID": st.column_config.Column(width="small"),
                                "Name": st.column_config.Column(width="medium"),
                                "Contact Person": st.column_config.Column(width="medium"),
                                "Email": st.column_config.Column(width="medium"),
                                "Phone": st.column_config.Column(width="small"),
                            }
                        )
                        
                        # Supplier actions
                        st.subheader("🛠️ Supplier Actions")
                        
                        if not df.empty:
                            # Select supplier for actions
                            supplier_options = [f"{row['Name']} (ID: {row['ID']})" for _, row in df.iterrows()]
                            selected_supplier = st.selectbox(
                                "Select supplier to manage:",
                                ["Choose a supplier..."] + supplier_options,
                                key="supplier_select_action"
                            )
                            
                            if selected_supplier != "Choose a supplier...":
                                try:
                                    supplier_id = int(selected_supplier.split("(ID: ")[1].rstrip(")"))
                                    
                                    action_cols = st.columns(3)
                                    with action_cols[0]:
                                        if st.button("👁️ View Details", use_container_width=True,
                                                    key=f"view_supp_{supplier_id}"):
                                            show_supplier_details(supplier_id)
                                    
                                    with action_cols[1]:
                                        if st.button("📦 View Products", use_container_width=True,
                                                    key=f"products_supp_{supplier_id}"):
                                            show_supplier_products(supplier_id)
                                    
                                    with action_cols[2]:
                                        if st.button("🗑️ Delete", use_container_width=True, type="secondary",
                                                    key=f"delete_supp_{supplier_id}"):
                                            # Confirmation handled separately
                                            st.session_state.deleting_supplier_id = supplier_id
                                            st.session_state.deleting_supplier_name = selected_supplier
                                    
                                    # Delete confirmation
                                    if ('deleting_supplier_id' in st.session_state and 
                                        st.session_state.deleting_supplier_id == supplier_id):
                                        st.warning(f"⚠️ Confirm deletion of {st.session_state.deleting_supplier_name}")
                                        confirm_col1, confirm_col2 = st.columns(2)
                                        with confirm_col1:
                                            if st.button("✅ Yes, Delete", use_container_width=True,
                                                        key=f"confirm_supp_del_{supplier_id}"):
                                                delete_response = requests.delete(
                                                    f"{api_url}/api/suppliers/{supplier_id}",
                                                    headers=headers,
                                                    timeout=5
                                                )
                                                if delete_response.status_code == 200:
                                                    st.success("✅ Supplier deleted!")
                                                    # Clear session state
                                                    if 'deleting_supplier_id' in st.session_state:
                                                        del st.session_state.deleting_supplier_id
                                                    if 'deleting_supplier_name' in st.session_state:
                                                        del st.session_state.deleting_supplier_name
                                                    time.sleep(1)
                                                    st.rerun()
                                                else:
                                                    st.error(f"❌ Failed to delete: {delete_response.text}")
                                        with confirm_col2:
                                            if st.button("❌ Cancel", use_container_width=True,
                                                        key=f"cancel_supp_del_{supplier_id}"):
                                                # Clear session state
                                                if 'deleting_supplier_id' in st.session_state:
                                                    del st.session_state.deleting_supplier_id
                                                if 'deleting_supplier_name' in st.session_state:
                                                    del st.session_state.deleting_supplier_name
                                                st.rerun()
                                except:
                                    st.warning("Could not parse supplier ID")
                        
                        # Export
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Export to CSV",
                            data=csv,
                            file_name=f"suppliers_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True,
                            key="export_supp_csv"
                        )
                    else:
                        st.info("📭 No suppliers match your search")
                else:
                    st.info("📭 No suppliers found in database")
            
            else:
                st.error(f"❌ API Error: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_add_supplier_form():
    """Form to add new supplier"""
    st.subheader("➕ Add New Supplier")
    
    with st.form("add_supplier", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Company Name *", placeholder="e.g., Silver World Inc.")
            contact_person = st.text_input("Contact Person", placeholder="e.g., John Smith")
            email = st.text_input("Email", placeholder="contact@company.com")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+1234567890")
            website = st.text_input("Website", placeholder="https://company.com")
        
        address = st.text_area("Address", placeholder="Full company address...", height=60)
        notes = st.text_area("Notes", placeholder="Payment terms, delivery notes, quality ratings...", height=80)
        
        submitted = st.form_submit_button("💾 Save Supplier", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Company name is required")
            else:
                supplier_data = {
                    "name": name,
                    "contact_person": contact_person if contact_person else None,
                    "email": email if email else None,
                    "phone": phone if phone else None,
                    "website": website if website else None,
                    "address": address if address else None,
                    "notes": notes if notes else None
                }
                
                try:
                    headers = auth.get_auth_header()
                    response = requests.post(
                        f"{st.session_state.api_url}/api/suppliers",
                        json=supplier_data,
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        saved_supplier = response.json()
                        st.success(f"✅ Supplier '{name}' added successfully!")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to save: {response.status_code} - {response.text[:200]}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_supplier_analytics():
    """Supplier analytics and performance"""
    st.subheader("📊 Supplier Analytics")
    st.info("Supplier performance metrics and analytics coming soon!")
    
    # Placeholder for now
    st.write("""
    ### 📈 Planned Analytics:
    
    - **Supplier Performance Ratings**
    - **Order Frequency & Volume**
    - **Delivery Time Analysis**
    - **Cost Comparison**
    - **Quality Ratings**
    - **Payment Terms Analysis**
    """)
    
    # Quick stats if available
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/suppliers",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            suppliers = response.json()
            if suppliers:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Suppliers", len(suppliers))
                with col2:
                    with_contact = sum(1 for s in suppliers if s.get('contact_person'))
                    st.metric("With Contact", with_contact)
                with col3:
                    with_email = sum(1 for s in suppliers if s.get('email'))
                    st.metric("With Email", with_email)
    except:
        pass


def show_supplier_details(supplier_id):
    """Show detailed supplier information"""
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/suppliers/{supplier_id}/dashboard",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            supplier = data.get('supplier', {})
            
            st.markdown(f"### 🏭 {supplier.get('name', 'Supplier Details')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **ID:** {supplier.get('id', 'N/A')}  
                **Name:** {supplier.get('name', 'N/A')}  
                **Contact:** {supplier.get('contact_person', 'N/A')}  
                **Email:** {supplier.get('email', 'N/A')}  
                **Phone:** {supplier.get('phone', 'N/A')}  
                **Website:** {supplier.get('website', 'N/A')}  
                """)
            
            with col2:
                stats = data.get('stats', {})
                st.metric("Total Revenue", f"€{stats.get('total_revenue', 0):,.2f}")
                st.metric("Order Count", stats.get('order_count', 0))
                st.metric("Avg Order", f"€{stats.get('avg_order_value', 0):,.2f}")
                st.metric("Rating", f"{stats.get('rating', 0)}/5")
        
        else:
            # Fallback to basic supplier info
            response = requests.get(
                f"{st.session_state.api_url}/api/suppliers",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                suppliers = response.json()
                supplier = next((s for s in suppliers if s.get('id') == supplier_id), None)
                
                if supplier:
                    st.markdown(f"### 🏭 {supplier.get('name', 'Supplier')}")
                    st.json(supplier)
                else:
                    st.error("Supplier not found")
            else:
                st.error(f"Failed to load supplier: {response.status_code}")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_supplier_products(supplier_id):
    """Show products from a specific supplier"""
    st.info(f"Products from supplier ID: {supplier_id}")
    
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/inventory",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            items = response.json()
            supplier_items = [item for item in items if item.get('supplier_id') == supplier_id]
            
            if supplier_items:
                st.write(f"**Found {len(supplier_items)} items from this supplier:**")
                
                for item in supplier_items:
                    with st.expander(f"📦 {item.get('name')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Category:** {item.get('category', 'N/A')}")
                            st.write(f"**Quantity:** {item.get('quantity', 0)}")
                        with col2:
                            st.write(f"**Unit Cost:** €{item.get('unit_cost', 0):,.2f}")
                            st.write(f"**Reorder Level:** {item.get('reorder_level', 10)}")
            else:
                st.info("No inventory items linked to this supplier")
        else:
            st.error(f"Failed to load inventory: {response.status_code}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

#===================================
# Inventory area - 6 tabs
#===================================

def show_inventory_page():
    """Complete Inventory Management System - 6 TAB VERSION WITH TAB SWITCHING"""
    st.markdown('<h1 class="main-header">📦 Inventory Management</h1>', unsafe_allow_html=True)
    
    # Check if we need to switch to a specific tab
    default_tab = 0  # Default to first tab
    
    # Map tab names to indices
    tab_names = ["📊 Dashboard", "📋 All Items", "➕ Add Item", 
                 "📥 Stock Movements", "🔔 Low Stock", "📈 Analytics"]
    
    # Check session state for tab switching
    if 'inventory_tab' in st.session_state:
        target_tab = st.session_state.inventory_tab
        if target_tab in tab_names:
            default_tab = tab_names.index(target_tab)
        # Clear after use
        del st.session_state.inventory_tab
    
    # 6 Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_names)
    
    # Use the selected tab
    tabs = [tab1, tab2, tab3, tab4, tab5, tab6]
    
    with tabs[default_tab]:
        if default_tab == 0:
            show_inventory_dashboard()
        elif default_tab == 1:
            show_all_inventory_items()
        elif default_tab == 2:
            show_add_inventory_item()
        elif default_tab == 3:
            show_stock_movements()
        elif default_tab == 4:
            show_low_stock_alerts()
        elif default_tab == 5:
            show_inventory_analytics()
    
    # Also render content for other tabs if they're selected
    # (Streamlit needs all tab content to be defined)
    with tab1:
        if default_tab != 0:
            show_inventory_dashboard()
    
    with tab2:
        if default_tab != 1:
            show_all_inventory_items()
    
    with tab3:
        if default_tab != 2:
            show_add_inventory_item()
    
    with tab4:
        if default_tab != 3:
            show_stock_movements()
    
    with tab5:
        if default_tab != 4:
            show_low_stock_alerts()
    
    with tab6:
        if default_tab != 5:
            show_inventory_analytics()


# ========== INVENTORY HELPER FUNCTIONS ==========

def show_inventory_dashboard():
    """Inventory dashboard with overview stats"""
    st.subheader("📊 Inventory Dashboard")
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        with st.spinner("🔄 Loading inventory data..."):
            # Get all inventory items
            response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=10)
            
            if response.status_code == 200:
                inventory_items = response.json()
                
                if inventory_items:
                    # Calculate statistics
                    total_items = len(inventory_items)
                    total_value = sum(item.get('unit_cost', 0) * item.get('quantity', 0) for item in inventory_items)
                    low_stock_count = sum(1 for item in inventory_items 
                                         if item.get('quantity', 0) <= item.get('reorder_level', 10))
                    out_of_stock = sum(1 for item in inventory_items if item.get('quantity', 0) <= 0)
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📦 Total Items", total_items)
                    with col2:
                        st.metric("💰 Total Value", f"€{total_value:,.2f}")
                    with col3:
                        st.metric("🔔 Low Stock", low_stock_count, 
                                 delta=f"-{out_of_stock} out of stock" if out_of_stock > 0 else None)
                    with col4:
                        avg_cost = total_value / sum(item.get('quantity', 1) for item in inventory_items) if total_items > 0 else 0
                        st.metric("📊 Avg Cost", f"€{avg_cost:,.2f}")
                    
                    st.markdown("---")
                    
                    # Top 5 most valuable items
                    st.subheader("💎 Top 5 Most Valuable Items")
                    items_with_value = []
                    for item in inventory_items:
                        value = item.get('unit_cost', 0) * item.get('quantity', 0)
                        items_with_value.append({
                            "ID": item.get('id', ''),
                            "Name": item.get('name', ''),
                            "Quantity": item.get('quantity', 0),
                            "Unit Cost": f"€{item.get('unit_cost', 0):,.2f}",
                            "Total Value": f"€{value:,.2f}",
                            "Category": item.get('category', ''),
                            "Status": "🟢 In Stock" if item.get('quantity', 0) > item.get('reorder_level', 10) 
                                     else "🟡 Low" if item.get('quantity', 0) > 0 
                                     else "🔴 Out"
                        })
                    
                    # Sort by value (descending)
                    items_with_value.sort(key=lambda x: float(x['Total Value'].replace('€', '').replace(',', '')), reverse=True)
                    
                    if items_with_value:
                        top_items_df = pd.DataFrame(items_with_value[:5])
                        st.dataframe(top_items_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No inventory items found")
                    
                    # Quick charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Stock Distribution")
                        if inventory_items:
                            # Create pie chart by category
                            categories = {}
                            for item in inventory_items:
                                cat = item.get('category', 'Uncategorized')
                                categories[cat] = categories.get(cat, 0) + item.get('quantity', 0)
                            
                            if categories:
                                cat_df = pd.DataFrame({
                                    'Category': list(categories.keys()),
                                    'Quantity': list(categories.values())
                                })
                                
                                fig = px.pie(cat_df, values='Quantity', names='Category', hole=0.3)
                                fig.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font_color='#F1F5F9'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("📈 Stock Status")
                        if inventory_items:
                            status_counts = {
                                "In Stock": sum(1 for item in inventory_items if item.get('quantity', 0) > item.get('reorder_level', 10)),
                                "Low Stock": sum(1 for item in inventory_items if 0 < item.get('quantity', 0) <= item.get('reorder_level', 10)),
                                "Out of Stock": sum(1 for item in inventory_items if item.get('quantity', 0) <= 0)
                            }
                            
                            status_df = pd.DataFrame({
                                'Status': list(status_counts.keys()),
                                'Count': list(status_counts.values())
                            })
                            
                            fig = px.bar(status_df, x='Status', y='Count', color='Status',
                                       color_discrete_map={
                                           'In Stock': '#10B981',
                                           'Low Stock': '#F59E0B',
                                           'Out of Stock': '#EF4444'
                                       })
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#F1F5F9',
                                showlegend=False
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Check also in the quick actions otherwhere
                    # Quick actions - FIXED VERSION
                    st.markdown("---")
                    st.subheader("⚡ Quick Actions")

                    action_cols = st.columns(4)

                    with action_cols[0]:
                        if st.button("📥 Receive Stock", use_container_width=True, key="dash_receive"):
                            st.session_state.inventory_tab = "📥 Stock Movements"  # Set which tab to show
                            st.rerun()

                    with action_cols[1]:
                        if st.button("📤 Adjust Stock", use_container_width=True, key="dash_adjust"):
                            st.session_state.inventory_tab = "📥 Stock Movements"
                            st.session_state.movement_type = "adjust"
                            st.rerun()

                    with action_cols[2]:
                        if st.button("🔔 View Alerts", use_container_width=True, key="dash_alerts"):
                            st.session_state.inventory_tab = "🔔 Low Stock"
                            st.rerun()

                    with action_cols[3]:
                        if st.button("🔄 Refresh", use_container_width=True, key="dash_refresh"):
                            st.rerun()
                    
                else:
                    st.info("📭 No inventory items found. Add your first item!")
                    st.markdown("""
                    **Getting Started:**
                    1. Go to **"➕ Add Item"** tab
                    2. Add your jewelry materials and supplies
                    3. Set reorder levels for automatic alerts
                    4. Track stock movements
                    """)
            
            else:
                st.error(f"❌ Failed to load inventory: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure backend is running and inventory endpoints are available")


def show_all_inventory_items():
    """Display all inventory items with search and filters - FIXED VERSION"""
    st.subheader("📋 All Inventory Items")
    
    # Search and filters
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search items...", placeholder="Name, category, supplier",
                                    key="inv_search")
    
    with col2:
        category_filter = st.selectbox("Category", ["All"] + get_inventory_categories(),
                                      key="inv_category")
    
    with col3:
        status_filter = st.selectbox("Status", ["All", "In Stock", "Low Stock", "Out of Stock"],
                                    key="inv_status")
    
    with col4:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True, key="inv_refresh"):
            st.rerun()
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        with st.spinner("🔄 Loading inventory..."):
            response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=10)
            
            if response.status_code == 200:
                inventory_items = response.json()
                
                # DEBUG: Show what we get
                with st.expander("🔍 Debug: First Item", expanded=False):
                    if inventory_items:
                        st.json(inventory_items[0] if len(inventory_items) > 0 else {})
                
                if inventory_items:
                    # Process and filter items
                    display_items = []
                    for item in inventory_items:
                        # Calculate status
                        quantity = item.get('quantity', 0)
                        reorder_level = item.get('reorder_level', 10)
                        
                        if quantity <= 0:
                            status = "🔴 Out of Stock"
                            status_class = "out"
                        elif quantity <= reorder_level:
                            status = "🟡 Low Stock"
                            status_class = "low"
                        else:
                            status = "🟢 In Stock"
                            status_class = "in"
                        
                        # Calculate total value
                        total_value = quantity * item.get('unit_cost', 0)
                        
                        # Get supplier - handle both 'supplier' and 'supplier_id' fields
                        supplier_field = item.get('supplier', item.get('supplier_id', ''))
                        
                        display_items.append({
                            "ID": item.get('id', ''),
                            "Name": item.get('name', ''),
                            "Category": item.get('category', ''),
                            "Quantity": quantity,
                            "Reorder Level": reorder_level,
                            "Unit Cost": f"€{item.get('unit_cost', 0):,.2f}",
                            "Total Value": f"€{total_value:,.2f}",
                            "Status": status,
                            "Status Class": status_class,
                            "Supplier": str(supplier_field),  # Convert to string to avoid errors
                            "Last Updated": item.get('updated_at', '')[:10] if item.get('updated_at') else ''
                        })
                    
                    # Apply filters
                    filtered_items = display_items
                    
                    if search_query:
                        filtered_items = [item for item in filtered_items 
                                        if search_query.lower() in item['Name'].lower() 
                                        or search_query.lower() in item['Category'].lower()
                                        or search_query.lower() in item['Supplier'].lower()]
                    
                    if category_filter != "All":
                        filtered_items = [item for item in filtered_items 
                                        if item['Category'] == category_filter]
                    
                    if status_filter != "All":
                        status_map = {
                            "In Stock": "🟢 In Stock",
                            "Low Stock": "🟡 Low Stock", 
                            "Out of Stock": "🔴 Out of Stock"
                        }
                        filtered_items = [item for item in filtered_items 
                                        if item['Status'] == status_map[status_filter]]
                    
                    if filtered_items:
                        # Create DataFrame
                        df = pd.DataFrame(filtered_items)
                        
                        # Display with formatting
                        st.dataframe(
                            df[['ID', 'Name', 'Category', 'Quantity', 'Reorder Level', 
                                'Unit Cost', 'Total Value', 'Status', 'Supplier', 'Last Updated']],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "ID": st.column_config.Column(width="small"),
                                "Quantity": st.column_config.Column(width="small"),
                                "Unit Cost": st.column_config.Column(width="small"),
                                "Total Value": st.column_config.Column(width="small"),
                                "Status": st.column_config.Column(width="small"),
                                "Supplier": st.column_config.Column(width="small"),
                            }
                        )
                        
                        # Item actions - REMOVE DUPLICATE BUTTON ISSUE
                        st.subheader("🛠️ Item Actions")
                        
                        if not df.empty:
                            # Select item for actions with UNIQUE key
                            item_options = [f"{row['Name']} (ID: {row['ID']})" for _, row in df.iterrows()]
                            selected_item = st.selectbox(
                                "Select item to manage:",
                                ["Choose an item..."] + item_options,
                                key="item_select_action"  # UNIQUE KEY
                            )
                            
                            if selected_item != "Choose an item...":
                                # Extract item ID
                                try:
                                    item_id = int(selected_item.split("(ID: ")[1].rstrip(")"))
                                    
                                    action_cols = st.columns(4)
                                    with action_cols[0]:
                                        if st.button("👁️ View Details", use_container_width=True, 
                                                    key=f"view_{item_id}"):  # UNIQUE KEY
                                            show_item_details(item_id)
                                    
                                    with action_cols[1]:
                                        if st.button("✏️ Edit", use_container_width=True, 
                                                    key=f"edit_{item_id}"):  # UNIQUE KEY
                                            st.session_state.editing_item_id = item_id
                                            st.rerun()
                                    
                                    with action_cols[2]:
                                        if st.button("📥 Receive Stock", use_container_width=True, 
                                                    key=f"receive_{item_id}"):  # UNIQUE KEY
                                            st.session_state.receiving_item_id = item_id
                                            st.rerun()
                                    
                                    with action_cols[3]:
                                        if st.button("🗑️ Delete", use_container_width=True, type="secondary",
                                                    key=f"delete_{item_id}"):  # UNIQUE KEY
                                            # Use session state for confirmation
                                            st.session_state.deleting_item_id = item_id
                                            st.session_state.deleting_item_name = selected_item
                                    
                                    # Show confirmation if deleting
                                    if 'deleting_item_id' in st.session_state and st.session_state.deleting_item_id == item_id:
                                        st.warning(f"⚠️ Confirm deletion of {st.session_state.deleting_item_name}")
                                        confirm_col1, confirm_col2 = st.columns(2)
                                        with confirm_col1:
                                            if st.button("✅ Yes, Delete", use_container_width=True, 
                                                        key=f"confirm_del_{item_id}"):
                                                delete_response = requests.delete(
                                                    f"{api_url}/api/inventory/{item_id}",
                                                    headers=headers,
                                                    timeout=5
                                                )
                                                if delete_response.status_code == 200:
                                                    st.success("✅ Item deleted!")
                                                    # Clear session state
                                                    if 'deleting_item_id' in st.session_state:
                                                        del st.session_state.deleting_item_id
                                                    if 'deleting_item_name' in st.session_state:
                                                        del st.session_state.deleting_item_name
                                                    time.sleep(1)
                                                    st.rerun()
                                                else:
                                                    st.error(f"❌ Failed to delete: {delete_response.text}")
                                        with confirm_col2:
                                            if st.button("❌ Cancel", use_container_width=True, 
                                                        key=f"cancel_del_{item_id}"):
                                                # Clear session state
                                                if 'deleting_item_id' in st.session_state:
                                                    del st.session_state.deleting_item_id
                                                if 'deleting_item_name' in st.session_state:
                                                    del st.session_state.deleting_item_name
                                                st.rerun()
                                except Exception as e:
                                    st.warning(f"Could not parse item ID: {str(e)}")
                        
                        # Export option with UNIQUE key
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Export to CSV",
                            data=csv,
                            file_name=f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True,
                            key="export_inv_csv"  # UNIQUE KEY
                        )
                    else:
                        st.info("📭 No items match your filters")
                else:
                    st.info("📭 No inventory items found")
            else:
                st.error(f"❌ API Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def get_inventory_categories():
    """Get unique inventory categories"""
    try:
        headers = auth.get_auth_header()
        response = requests.get(f"{st.session_state.api_url}/api/inventory", headers=headers, timeout=5)
        if response.status_code == 200:
            items = response.json()
            categories = set(item.get('category', '') for item in items if item.get('category'))
            return sorted(list(categories))
    except:
        pass
    return []


def show_add_inventory_item():
    """Form to add new inventory item"""
    st.subheader("➕ Add New Inventory Item")
    
    # Fetch suppliers for dropdown
    suppliers_list = ["Select Supplier..."]
    try:
        headers = auth.get_auth_header()
        response = requests.get(f"{st.session_state.api_url}/api/suppliers", headers=headers, timeout=5)
        if response.status_code == 200:
            suppliers = response.json()
            suppliers_list += [f"{s['name']} (ID: {s['id']})" for s in suppliers]
    except:
        st.warning("Could not load suppliers")
    
    with st.form("add_inventory_item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Item Name *", placeholder="e.g., Sterling Silver Chain")
            category = st.text_input("Category *", placeholder="e.g., Materials, Packaging, Tools")
            description = st.text_area("Description", placeholder="Item details, specifications...", height=80)
        
        with col2:
            unit_cost = st.number_input("Unit Cost (€) *", min_value=0.01, value=10.0, step=0.01)
            quantity = st.number_input("Initial Quantity *", min_value=0, value=0, step=1)
            reorder_level = st.number_input("Reorder Level *", min_value=1, value=10, step=1,
                                          help="Alert when stock reaches this level")
            supplier = st.selectbox("Supplier", suppliers_list)
        
        submitted = st.form_submit_button("💾 Save Item", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not name or not category:
                st.error("❌ Name and Category are required")
            elif unit_cost <= 0:
                st.error("❌ Unit cost must be greater than 0")
            elif reorder_level < 1:
                st.error("❌ Reorder level must be at least 1")
            else:
                # Prepare item data
                item_data = {
                    "name": name,
                    "category": category,
                    "description": description if description else None,
                    "unit_cost": float(unit_cost),
                    "quantity": int(quantity),
                    "reorder_level": int(reorder_level)
                }
                
                # Add supplier if selected
                if supplier != "Select Supplier...":
                    try:
                        supplier_id = int(supplier.split("(ID: ")[1].rstrip(")"))
                        item_data["supplier_id"] = supplier_id
                    except:
                        st.warning("Could not parse supplier ID")
                
                # Save to backend
                try:
                    headers = auth.get_auth_header()
                    response = requests.post(
                        f"{st.session_state.api_url}/api/inventory",
                        json=item_data,
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        saved_item = response.json()
                        st.success(f"✅ Item '{name}' added successfully!")
                        
                        # Show success card
                        st.markdown(f"""
                        <div style="background-color: rgba(30, 41, 59, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0;">
                            <h4 style="color: #F1F5F9; margin: 0 0 10px 0;">✅ Inventory Item Saved</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem;">
                                <div><strong>ID:</strong> {saved_item.get('id', 'N/A')}</div>
                                <div><strong>Name:</strong> {name}</div>
                                <div><strong>Category:</strong> {category}</div>
                                <div><strong>Quantity:</strong> {quantity}</div>
                                <div><strong>Unit Cost:</strong> €{unit_cost:,.2f}</div>
                                <div><strong>Reorder Level:</strong> {reorder_level}</div>
                                <div><strong>Total Value:</strong> €{quantity * unit_cost:,.2f}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                        
                    else:
                        st.error(f"❌ Failed to save: {response.status_code} - {response.text[:200]}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_stock_movements():
    """Track stock movements (receiving, adjusting, transferring)"""
    st.subheader("📥 Stock Movements")
    
    # Movement type selector
    movement_type = st.radio(
        "Movement Type:",
        ["📥 Receive Stock", "📤 Adjust Stock", "🔄 Transfer Stock"],
        horizontal=True
    )
    
    if movement_type == "📥 Receive Stock":
        show_receive_stock_form()
    elif movement_type == "📤 Adjust Stock":
        show_adjust_stock_form()
    else:
        show_transfer_stock_form()


def show_receive_stock_form():
    """Form for receiving stock (adding to inventory) - FIXED"""
    st.markdown("#### 📥 Receive New Stock")
    
    # Get inventory items for dropdown
    items_list = ["Select Item..."]
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=5)
        if response.status_code == 200:
            items = response.json()
            items_list += [f"{item['name']} (ID: {item['id']})" for item in items]
    except:
        st.warning("Could not load inventory items")
    
    with st.form("receive_stock", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            item = st.selectbox("Item *", items_list, key="receive_item")
            quantity = st.number_input("Quantity Received *", min_value=1, value=10, step=1, key="receive_qty")
            # FIX: Change value from 0.0 to 0.01 or None
            unit_cost = st.number_input("Unit Cost (€)", min_value=0.01, value=None, step=0.01,
                                      help="Leave empty to use existing unit cost", key="receive_cost")
        
        with col2:
            date = st.date_input("Receipt Date", value=datetime.now(), key="receive_date")
            reference = st.text_input("Reference Number", placeholder="PO-12345, Invoice #, etc.", key="receive_ref")
            notes = st.text_area("Notes", placeholder="Supplier, quality notes, etc.", height=60, key="receive_notes")
        
        # FIX: Add a proper submit button
        submit_col1, submit_col2 = st.columns([3, 1])
        with submit_col1:
            submitted = st.form_submit_button("📥 Receive Stock", use_container_width=True, type="primary")
        
        with submit_col2:
            if st.form_submit_button("🔄 Clear", use_container_width=True):
                st.rerun()
        
        if submitted:
            if item == "Select Item...":
                st.error("❌ Please select an item")
            elif quantity <= 0:
                st.error("❌ Quantity must be greater than 0")
            else:
                try:
                    # Extract item ID
                    item_id = int(item.split("(ID: ")[1].rstrip(")"))
                    
                    # Prepare stock movement data
                    movement_data = {
                        "item_id": item_id,
                        "quantity": quantity,
                        "movement_type": "receive",
                        "reference": reference if reference else None,
                        "notes": notes if notes else None,
                        "date": date.isoformat()
                    }
                    
                    if unit_cost and unit_cost > 0:
                        movement_data["unit_cost"] = float(unit_cost)
                    
                    # In a real app, you'd have a stock movements API endpoint
                    # For now, update the inventory item directly
                    st.info(f"📦 Receiving {quantity} units of {item.split(' (ID:')[0]}")
                    
                    # Get current item
                    response = requests.get(
                        f"{api_url}/api/inventory/{item_id}",
                        headers=headers,
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        current_item = response.json()
                        
                        # Update quantity
                        update_data = {
                            "quantity": current_item.get('quantity', 0) + quantity
                        }
                        
                        # Update unit cost if provided
                        if unit_cost and unit_cost > 0:
                            update_data["unit_cost"] = float(unit_cost)
                            update_data["updated_at"] = datetime.utcnow().isoformat()
                        
                        # Send update
                        update_response = requests.put(
                            f"{api_url}/api/inventory/{item_id}",
                            json=update_data,
                            headers=headers,
                            timeout=5
                        )
                        
                        if update_response.status_code == 200:
                            st.success(f"✅ Received {quantity} units!")
                            st.balloons()
                            
                            # Show success summary
                            st.markdown(f"""
                            <div style="background-color: rgba(30, 41, 59, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0;">
                                <h4 style="color: #F1F5F9; margin: 0 0 10px 0;">✅ Stock Received</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem;">
                                    <div><strong>Item:</strong> {item.split(' (ID:')[0]}</div>
                                    <div><strong>Quantity:</strong> {quantity}</div>
                                    <div><strong>New Total:</strong> {current_item.get('quantity', 0) + quantity}</div>
                                    <div><strong>Date:</strong> {date.strftime('%Y-%m-%d')}</div>
                                    <div><strong>Reference:</strong> {reference or 'N/A'}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update inventory: {update_response.status_code}")
                    else:
                        st.error(f"❌ Failed to get item details: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_adjust_stock_form():
    """Form for adjusting stock (corrections, damage, loss)"""
    st.markdown("#### 📤 Adjust Stock Levels")
    st.info("Use for corrections, damaged goods, or inventory discrepancies")
    
    # Similar form to receive stock but with adjustment type
    st.write("Adjustment form coming soon!")


def show_transfer_stock_form():
    """Form for transferring stock between locations"""
    st.markdown("#### 🔄 Transfer Stock")
    st.info("Transfer items between different storage locations or shops")
    
    st.write("Transfer functionality coming soon!")


def show_low_stock_alerts():
    """Show items that are low on stock or out of stock"""
    st.subheader("🔔 Low Stock Alerts")
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        with st.spinner("🔄 Checking stock levels..."):
            response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=10)
            
            if response.status_code == 200:
                inventory_items = response.json()
                
                # Categorize items
                out_of_stock = []
                low_stock = []
                healthy_stock = []
                
                for item in inventory_items:
                    quantity = item.get('quantity', 0)
                    reorder_level = item.get('reorder_level', 10)
                    
                    if quantity <= 0:
                        out_of_stock.append(item)
                    elif quantity <= reorder_level:
                        low_stock.append(item)
                    else:
                        healthy_stock.append(item)
                
                # Display alerts
                if out_of_stock:
                    st.error(f"## 🔴 {len(out_of_stock)} ITEMS OUT OF STOCK")
                    
                    for item in out_of_stock:
                        with st.expander(f"❌ {item.get('name')} - OUT OF STOCK", expanded=True):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Current Stock", item.get('quantity', 0))
                            with col2:
                                st.metric("Reorder Level", item.get('reorder_level', 10))
                            with col3:
                                if st.button(f"🛒 Reorder {item.get('name')[:20]}...", key=f"reorder_{item.get('id')}"):
                                    st.info(f"Reorder {item.get('name')} - Contact supplier")
                
                if low_stock:
                    st.warning(f"## 🟡 {len(low_stock)} ITEMS LOW ON STOCK")
                    
                    low_stock_df = []
                    for item in low_stock:
                        low_stock_df.append({
                            "ID": item.get('id', ''),
                            "Name": item.get('name', ''),
                            "Current": item.get('quantity', 0),
                            "Reorder Level": item.get('reorder_level', 10),
                            "Need": item.get('reorder_level', 10) - item.get('quantity', 0),
                            "Unit Cost": f"€{item.get('unit_cost', 0):,.2f}",
                            "Supplier": f"ID: {item.get('supplier_id', 'N/A')}"
                        })
                    
                    if low_stock_df:
                        df = pd.DataFrame(low_stock_df)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Generate reorder list
                        if st.button("📋 Generate Reorder List", use_container_width=True):
                            reorder_list = "\n".join([f"- {row['Name']}: Need {row['Need']} more" for _, row in df.iterrows()])
                            st.text_area("Reorder List", reorder_list, height=150)
                
                if not out_of_stock and not low_stock:
                    st.success("## 🟢 ALL ITEMS ARE WELL STOCKED!")
                    st.balloons()
                    st.info("No low stock alerts at this time. Good job!")
                
                # Show healthy items count
                if healthy_stock:
                    st.markdown(f"### 🟢 {len(healthy_stock)} items are well stocked")
            
            else:
                st.error(f"❌ Failed to load inventory: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_inventory_analytics():
    """Inventory analytics and insights"""
    st.subheader("📈 Inventory Analytics")
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        with st.spinner("🔄 Loading analytics..."):
            response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=10)
            
            if response.status_code == 200:
                inventory_items = response.json()
                
                if inventory_items:
                    # Calculate key metrics
                    total_items = len(inventory_items)
                    total_quantity = sum(item.get('quantity', 0) for item in inventory_items)
                    total_value = sum(item.get('unit_cost', 0) * item.get('quantity', 0) for item in inventory_items)
                    avg_turnover = 0  # Would need transaction history
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total SKUs", total_items)
                    with col2:
                        st.metric("Total Units", total_quantity)
                    with col3:
                        st.metric("Total Value", f"€{total_value:,.2f}")
                    with col4:
                        st.metric("Avg Stock Value", f"€{total_value/total_items:,.2f}" if total_items > 0 else "€0")
                    
                    st.markdown("---")
                    
                    # Value by category
                    st.subheader("💰 Value by Category")
                    
                    category_value = {}
                    for item in inventory_items:
                        cat = item.get('category', 'Uncategorized')
                        value = item.get('unit_cost', 0) * item.get('quantity', 0)
                        category_value[cat] = category_value.get(cat, 0) + value
                    
                    if category_value:
                        cat_df = pd.DataFrame({
                            'Category': list(category_value.keys()),
                            'Value': list(category_value.values())
                        }).sort_values('Value', ascending=False)
                        
                        fig = px.bar(cat_df, x='Category', y='Value', 
                                   title='Inventory Value by Category',
                                   color='Value')
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#F1F5F9'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # ABC Analysis (Pareto)
                    st.subheader("📊 ABC Analysis (Pareto)")
                    st.info("Classify items by value contribution (Coming Soon)")
                    
                    # Stock turnover forecast
                    st.subheader("📈 Stock Forecast")
                    st.info("Predict future stock needs based on sales history (Coming Soon)")
                    
                    # Recommendations
                    st.subheader("💡 Recommendations")
                    
                    recommendations = []
                    
                    # Check for slow movers (quantity high but no sales)
                    for item in inventory_items:
                        quantity = item.get('quantity', 0)
                        reorder_level = item.get('reorder_level', 10)
                        
                        if quantity > reorder_level * 3:  # 3x reorder level
                            recommendations.append(f"**{item.get('name')}** might be overstocked (has {quantity}, reorder at {reorder_level})")
                    
                    if recommendations:
                        for rec in recommendations[:5]:  # Show top 5
                            st.warning(rec)
                    else:
                        st.success("✅ Inventory levels look good!")
                
                else:
                    st.info("📭 No inventory data for analytics")
            
            else:
                st.error(f"❌ Failed to load data: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_item_details(item_id):
    """Show detailed view of an inventory item"""
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/inventory/{item_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            item = response.json()
            
            st.markdown(f"### 👁️ {item.get('name', 'Item Details')}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **ID:** {item.get('id', 'N/A')}  
                **Name:** {item.get('name', 'N/A')}  
                **Category:** {item.get('category', 'N/A')}  
                **Description:** {item.get('description', 'N/A')}  
                **Supplier ID:** {item.get('supplier_id', 'N/A')}  
                **Created:** {item.get('created_at', 'N/A')[:10] if item.get('created_at') else 'N/A'}  
                **Updated:** {item.get('updated_at', 'N/A')[:10] if item.get('updated_at') else 'N/A'}  
                """)
            
            with col2:
                quantity = item.get('quantity', 0)
                reorder_level = item.get('reorder_level', 10)
                unit_cost = item.get('unit_cost', 0)
                total_value = quantity * unit_cost
                
                st.metric("Current Stock", quantity)
                st.metric("Reorder Level", reorder_level)
                st.metric("Unit Cost", f"€{unit_cost:,.2f}")
                st.metric("Total Value", f"€{total_value:,.2f}")
                
                # Stock status
                if quantity <= 0:
                    st.error("🔴 OUT OF STOCK")
                elif quantity <= reorder_level:
                    st.warning(f"🟡 LOW STOCK (Need {reorder_level - quantity} more)")
                else:
                    st.success(f"🟢 IN STOCK ({quantity - reorder_level} above reorder level)")
        
        else:
            st.error(f"Failed to load item details: {response.status_code}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Adding debug function temporarily
def debug_inventory_api():
    """Debug what the inventory API returns"""
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{st.session_state.api_url}/api/inventory",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            items = response.json()
            if items:
                st.write("📋 **First inventory item fields:**")
                st.json(items[0])
                st.write("🔑 **All field names:**")
                st.write(list(items[0].keys()))
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ========== MAIN APP FUNCTION ==========
def main_app():
    """Main application after login"""
    
    apply_dark_theme()
    
    username = auth.get_username()
    user_role = auth.get_user_role()
    
    if 'api_url' not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"
    
    # # ========== SIDEBAR ==========
    # with st.sidebar:
    #     # Logo and user info
    #     st.markdown(f"""
    #     <div style="text-align: center; padding: 1.5rem 0;">
    #         <div style="font-size: 3rem;">💎</div>
    #         <h2 style="margin: 0;">Shiny Jar</h2>
    #         <p style="color: #94A3B8; font-size: 0.9rem;">Jewelry CRM Suite</p>
            
    #         <div style="
    #             background: rgba(30, 41, 59, 0.8);
    #             border: 1px solid #334155;
    #             border-radius: 12px;
    #             padding: 0.75rem;
    #             margin: 1rem 0;
    #         ">
    #             <p style="margin: 0; font-weight: 600;">👤 {username}</p>
    #             <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">{user_role.title()}</p>
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)
        
    #     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
    #     # Logout button - FIXED: No icon parameter
    #     if st.button("🚪 Logout", use_container_width=True):
    #         auth.logout()
        
    #     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
    #     # API Status
    #     try:
    #         response = requests.get(f"{st.session_state.api_url}/health", timeout=2)
    #         if response.status_code == 200:
    #             st.markdown('<div class="api-connected">✅ API Connected</div>', unsafe_allow_html=True)
    #         else:
    #             st.markdown('<div class="api-disconnected">❌ API Error</div>', unsafe_allow_html=True)
    #     except:
    #         st.markdown('<div class="api-disconnected">🌐 API Not Connected</div>', unsafe_allow_html=True)
    #         if auth.is_demo_mode():
    #             st.info("🎮 Using demo data")
        
    #     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
    #     # Navigation
    #     st.markdown("### 📱 Navigation")
        
    #     if user_role == "customer":
    #         pages = ["My Dashboard", "My Orders", "My Invoices", "My Profile"]
    #         page_titles = ["📊 My Dashboard", "🛍️ My Orders", "💳 My Invoices", "👤 My Profile"]
    #     elif user_role == "supplier":
    #         pages = ["My Dashboard", "My Orders", "My Products", "My Payments", "My Profile"]
    #         page_titles = ["📊 My Dashboard", "📦 My Orders", "📋 My Products", "💰 My Payments", "👤 My Profile"]
    #     # else:
    #     #     pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Inventory", "Budget", "Analytics", "Reports"]
    #     #     page_titles = ["📊 Dashboard", "💰 Expenses", "👥 Customers", "🏭 Suppliers", "📦 Inventory" "📋 Budget", "📈 Analytics", "📊 Reports"]
    #     #     page_icons = ["📊", "💰", "👥", "🏭", "📦", "📋", "📈", "📊"]
    #     else:  # admin user
    #         pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Inventory", "Budget", "Analytics", "Reports"]
    #         page_titles = ["📊 Dashboard", "💰 Expenses", "👥 Customers", "🏭 Suppliers", 
    #                     "📦 Inventory", "📋 Budget", "📈 Analytics", "📊 Reports"]
    #         page_icons = ["📊", "💰", "👥", "🏭", "📦", "📋", "📈", "📊"]
        
    #     if 'page' not in st.session_state:
    #         st.session_state.page = pages[0]
        
    #     # Navigation radio
    #     selected_title = st.radio("Choose page:", page_titles, label_visibility="collapsed")
        
    #     selected_page = pages[page_titles.index(selected_title)]
        
    #     if selected_page != st.session_state.page:
    #         st.session_state.page = selected_page
    #         st.rerun()
        
    #     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
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
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            auth.logout()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # API Status (keep your existing code)
        # ...
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ========== FIXED NAVIGATION ==========
        st.markdown("### 📱 Navigation")
        
        if user_role == "customer":
            pages = ["My Dashboard", "My Orders", "My Invoices", "My Profile"]
            page_titles = ["📊 My Dashboard", "🛍️ My Orders", "💳 My Invoices", "👤 My Profile"]
        elif user_role == "supplier":
            pages = ["My Dashboard", "My Orders", "My Products", "My Payments", "My Profile"]
            page_titles = ["📊 My Dashboard", "📦 My Orders", "📋 My Products", "💰 My Payments", "👤 My Profile"]
        else:  # admin/demo user
            # FIXED: Correct page order and titles
            pages = ["Dashboard", "Expenses", "Customers", "Suppliers", "Inventory", "Budget", "Analytics", "Reports"]
            page_titles = ["📊 Dashboard", "💰 Expenses", "👥 Customers", "🏭 Suppliers", 
                        "📦 Inventory", "📋 Budget", "📈 Analytics", "📊 Reports"]
        
        if 'page' not in st.session_state:
            st.session_state.page = pages[0]
        
        # Navigation radio - FIXED: Use unique keys
        selected_title = st.radio(
            "Choose page:", 
            page_titles, 
            index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
            key="nav_radio_" + user_role  # Unique key per role
        )
        
        # Get the corresponding page from selected title
        selected_page = pages[page_titles.index(selected_title)]
        
        # Update session state if changed
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
    
    
    else:  # admin/demo user
        if current_page == "Dashboard":
            show_dashboard()
        elif current_page == "Expenses":
            show_expenses_page()
        elif current_page == "Customers":
            show_customers_page()
        elif current_page == "Suppliers":
            show_suppliers_page()
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
