# frontend/pages/customer_portal.py
import streamlit as st
import pandas as pd
import requests
from auth import auth

def show_customer_portal():
    st.markdown('<h1 class="main-header">👤 Customer Portal</h1>', unsafe_allow_html=True)
    
    api_url = st.session_state.get('api_url', 'http://localhost:8000')
    
    # Get current customer ID (you'd map username to customer_id)
    customer_id = get_current_customer_id(auth.get_username())
    
    if customer_id:
        tab1, tab2, tab3 = st.tabs(["📦 My Orders", "💰 My Invoices", "👤 My Profile"])
        
        with tab1:
            show_my_orders(api_url, customer_id)
        
        with tab2:
            show_my_invoices(api_url, customer_id)
        
        with tab3:
            show_my_profile(api_url, customer_id)
    else:
        st.error("Customer profile not found")

def get_current_customer_id(username):
    """Map username to customer ID"""
    # In a real app, you'd query the database
    # For demo, return a default ID
    return 1

def show_my_orders(api_url, customer_id):
    st.subheader("🛍️ My Purchase History")
    
    try:
        # Get transactions for this customer
        headers = auth.get_auth_header()
        response = requests.get(
            f"{api_url}/api/transactions",
            params={"customer_id": customer_id, "type": "income"},
            headers=headers
        )
        
        if response.status_code == 200:
            orders = response.json()
            
            if orders:
                df = pd.DataFrame(orders)
                
                # Display orders
                st.dataframe(
                    df[['date', 'amount', 'category', 'description']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "date": "Date",
                        "amount": st.column_config.NumberColumn("Amount", format="€%.2f"),
                        "category": "Category",
                        "description": "Description"
                    }
                )
                
                # Order summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_spent = df['amount'].sum()
                    st.metric("Total Spent", f"€{total_spent:,.2f}")
                with col2:
                    order_count = len(df)
                    st.metric("Orders", order_count)
                with col3:
                    avg_order = total_spent / order_count if order_count > 0 else 0
                    st.metric("Avg Order", f"€{avg_order:,.2f}")
            else:
                st.info("No orders found")
        else:
            st.error("Failed to load orders")
    
    except Exception as e:
        st.error(f"Error loading orders: {str(e)}")