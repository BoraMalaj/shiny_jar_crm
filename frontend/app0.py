import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Shiny Jar Business Suite",
    page_icon="💎",
    layout="wide"
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
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.title("💎 Shiny Jar")
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
    
    # Navigation
    page = st.radio("Navigation", ["Dashboard", "Expenses", "Customers", "Analytics"])
    
    st.markdown("---")
    st.caption(f"Backend: {st.session_state.api_url}")

# Page routing
if page == "Dashboard":
    st.markdown('<h1 class="main-header">📊 Dashboard</h1>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", "€2,450", "+12%")
    
    with col2:
        st.metric("Total Expenses", "€890", "-5%")
    
    with col3:
        st.metric("Active Customers", "124", "+8")
    
    with col4:
        st.metric("Profit", "€1,560", "+15%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Transactions")
        try:
            response = requests.get(f"{st.session_state.api_url}/api/transactions")
            if response.status_code == 200:
                transactions = response.json()["transactions"]
                df = pd.DataFrame(transactions)
                st.dataframe(df.head(10), use_container_width=True)
            else:
                st.info("No transactions yet. Add some!")
        except:
            st.info("Connect to backend to see transactions")
    
    with col2:
        st.subheader("Expense Distribution")
        # Sample chart
        data = pd.DataFrame({
            'Category': ['Materials', 'Shipping', 'Marketing', 'Packaging'],
            'Amount': [450, 120, 180, 140]
        })
        fig = px.pie(data, values='Amount', names='Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Expense", use_container_width=True):
            st.session_state.page = "Expenses"
            st.rerun()
    
    with col2:
        if st.button("👤 Add Customer", use_container_width=True):
            st.session_state.page = "Customers"
            st.rerun()
    
    with col3:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "Analytics"
            st.rerun()

elif page == "Expenses":
    st.markdown('<h1 class="main-header">💰 Expense Management</h1>', unsafe_allow_html=True)
    
    # Add expense form
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (€)", min_value=0.0, step=0.01)
            category = st.selectbox("Category", ["Materials", "Shipping", "Marketing", "Packaging", "Other"])
        
        with col2:
            transaction_type = st.selectbox("Type", ["expense", "income"])
            description = st.text_area("Description")
        
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted and amount > 0:
            transaction_data = {
                "amount": amount,
                "type": transaction_type,
                "category": category,
                "description": description
            }
            
            try:
                response = requests.post(f"{st.session_state.api_url}/api/transactions", json=transaction_data)
                if response.status_code == 200:
                    st.success("✅ Transaction added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add transaction")
            except:
                st.error("❌ Backend unavailable")
    
    # Expense list
    st.subheader("📋 Recent Transactions")
    try:
        response = requests.get(f"{st.session_state.api_url}/api/transactions")
        if response.status_code == 200:
            transactions = response.json()["transactions"]
            if transactions:
                df = pd.DataFrame(transactions)
                st.dataframe(df, use_container_width=True)
                
                # Summary
                col1, col2 = st.columns(2)
                with col1:
                    total_expenses = df[df['type'] == 'expense']['amount'].sum()
                    st.metric("Total Expenses", f"€{total_expenses:.2f}")
                with col2:
                    total_income = df[df['type'] == 'income']['amount'].sum()
                    st.metric("Total Income", f"€{total_income:.2f}")
            else:
                st.info("No transactions yet. Add your first one!")
    except:
        st.info("Connect to backend to see transactions")

elif page == "Customers":
    st.markdown('<h1 class="main-header">👥 Customer CRM</h1>', unsafe_allow_html=True)
    
    # Add customer form
    with st.form("add_customer"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Customer Name")
            email = st.text_input("Email")
        
        with col2:
            instagram = st.text_input("Instagram Handle")
            phone = st.text_input("Phone")
        
        submitted = st.form_submit_button("Add Customer")
        
        if submitted and name:
            st.success(f"✅ Customer {name} added (simulated)")
            # In a real app, you would send this to the backend
    
    # Customer list
    st.subheader("📋 Customer Directory")
    try:
        response = requests.get(f"{st.session_state.api_url}/api/customers")
        if response.status_code == 200:
            customers = response.json()["customers"]
            if customers:
                df = pd.DataFrame(customers)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No customers yet. Add your first customer!")
        else:
            # Show sample data
            sample_customers = [
                {"id": 1, "name": "Maria Silva", "instagram": "maria_silva", "email": "maria@email.com", "total_spent": 250.00},
                {"id": 2, "name": "John Doe", "instagram": "john_jewelry", "email": "john@email.com", "total_spent": 180.00},
                {"id": 3, "name": "Anna Smith", "instagram": "anna_sparkle", "email": "anna@email.com", "total_spent": 320.00},
            ]
            df = pd.DataFrame(sample_customers)
            st.dataframe(df, use_container_width=True)
            st.info("Showing sample data. Connect to backend for real data.")
    except:
        st.info("Connect to backend to see customers")

elif page == "Analytics":
    st.markdown('<h1 class="main-header">📈 Analytics & Reports</h1>', unsafe_allow_html=True)
    
    # Sample analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Revenue")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [1500, 1800, 2200, 1900, 2400, 2800]
        expenses = [800, 850, 900, 820, 950, 1000]
        
        df = pd.DataFrame({
            'Month': months,
            'Revenue': revenue,
            'Expenses': expenses
        })
        
        fig = px.line(df, x='Month', y=['Revenue', 'Expenses'], 
                     title='Monthly Performance', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Customer Spending")
        customers = ['Customer A', 'Customer B', 'Customer C', 'Customer D', 'Customer E']
        spending = [320, 280, 450, 190, 310]
        
        df2 = pd.DataFrame({
            'Customer': customers,
            'Spending (€)': spending
        })
        
        fig2 = px.bar(df2, x='Customer', y='Spending (€)', 
                      title='Top Customers', color='Spending (€)')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Export options
    st.subheader("📤 Export Reports")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as PDF", use_container_width=True):
            st.success("PDF export simulated")
    
    with col2:
        if st.button("📊 Export as Excel", use_container_width=True):
            st.success("Excel export simulated")
    
    with col3:
        if st.button("📈 Export as CSV", use_container_width=True):
            st.success("CSV export simulated")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "💎 Shiny Jar Business Suite | Built with ❤️ for University Project"
    "</div>",
    unsafe_allow_html=True
)