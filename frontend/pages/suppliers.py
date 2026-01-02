# frontend/pages/suppliers.py
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import time

def show_suppliers_page():
    st.markdown('<h1 class="main-header">🏭 Supplier Management</h1>', unsafe_allow_html=True)
    
    api_url = st.session_state.get('api_url', 'http://localhost:8000')
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Suppliers", "➕ Add Supplier", "💰 Purchase History", "📊 Performance"])
    
    with tab1:
        show_all_suppliers(api_url)
    
    with tab2:
        show_add_supplier(api_url)
    
    with tab3:
        show_purchase_history(api_url)
    
    with tab4:
        show_supplier_performance(api_url)

def show_all_suppliers(api_url):
    st.subheader("Supplier Directory")
    
    try:
        response = requests.get(f"{api_url}/api/suppliers")
        
        if response.status_code == 200:
            suppliers = response.json()
            
            if suppliers:
                df = pd.DataFrame(suppliers)
                
                # Search and filter
                col1, col2 = st.columns([3, 1])
                with col1:
                    search_term = st.text_input("Search suppliers...", key="supplier_search")
                with col2:
                    sort_by = st.selectbox("Sort by", ["Name A-Z", "Name Z-A", "Recent"])
                
                # Filter and sort
                if search_term:
                    mask = df['name'].str.contains(search_term, case=False, na=False) | \
                           df['email'].str.contains(search_term, case=False, na=False) | \
                           df['contact_person'].str.contains(search_term, case=False, na=False)
                    df = df[mask]
                
                if sort_by == "Name A-Z":
                    df = df.sort_values('name')
                elif sort_by == "Name Z-A":
                    df = df.sort_values('name', ascending=False)
                
                # Display suppliers
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Supplier Name", width="medium"),
                        "contact_person": st.column_config.TextColumn("Contact", width="small"),
                        "email": st.column_config.TextColumn("Email", width="medium"),
                        "phone": st.column_config.TextColumn("Phone", width="small"),
                        "website": st.column_config.LinkColumn("Website", width="small")
                    }
                )
                
                # Supplier actions
                st.subheader("Supplier Actions")
                if suppliers:
                    selected_supplier = st.selectbox(
                        "Select Supplier",
                        options=[f"{s['id']}: {s['name']}" for s in suppliers],
                        key="supplier_select"
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("👀 View Details", use_container_width=True):
                            if selected_supplier:
                                supplier_id = int(selected_supplier.split(":")[0])
                                st.session_state.view_supplier_id = supplier_id
                                st.rerun()
                    
                    with col2:
                        if st.button("✏️ Edit", use_container_width=True):
                            if selected_supplier:
                                supplier_id = int(selected_supplier.split(":")[0])
                                st.session_state.edit_supplier_id = supplier_id
                    
                    with col3:
                        if st.button("🗑️ Delete", use_container_width=True, type="secondary"):
                            if selected_supplier:
                                supplier_id = int(selected_supplier.split(":")[0])
                                with st.popover("⚠️ Confirm Delete"):
                                    st.warning(f"Delete {selected_supplier.split(':')[1]}?")
                                    if st.button("Confirm Delete", type="primary"):
                                        try:
                                            delete_response = requests.delete(f"{api_url}/api/suppliers/{supplier_id}")
                                            if delete_response.status_code == 200:
                                                st.success("Supplier deleted!")
                                                time.sleep(1)
                                                st.rerun()
                                            else:
                                                st.error("Delete failed")
                                        except:
                                            st.error("Connection error")
            else:
                st.info("No suppliers found. Add your first supplier!")
        else:
            st.error("Failed to load suppliers")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_add_supplier(api_url):
    st.subheader("Add New Supplier")
    
    with st.form("add_supplier_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Company Name *", placeholder="Silver World Inc.")
            contact_person = st.text_input("Contact Person", placeholder="John Smith")
            email = st.text_input("Email", placeholder="contact@company.com")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+1234567890")
            website = st.text_input("Website", placeholder="https://company.com")
            address = st.text_area("Address", placeholder="Street, City, Country")
        
        notes = st.text_area("Notes", placeholder="Payment terms, preferred contact method...")
        
        submitted = st.form_submit_button("Add Supplier", type="primary", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("Company name is required!")
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
                    response = requests.post(f"{api_url}/api/suppliers", json=supplier_data)
                    
                    if response.status_code == 200:
                        st.success(f"✅ Supplier {name} added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Failed to add supplier: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")

def show_purchase_history(api_url):
    st.subheader("Purchase History by Supplier")
    
    try:
        # Get suppliers
        suppliers_response = requests.get(f"{api_url}/api/suppliers")
        # Get transactions (expenses)
        transactions_response = requests.get(f"{api_url}/api/transactions", params={"type": "expense", "limit": 1000})
        
        if suppliers_response.status_code == 200 and transactions_response.status_code == 200:
            suppliers = suppliers_response.json()
            transactions = transactions_response.json()
            
            if suppliers and transactions:
                suppliers_df = pd.DataFrame(suppliers)
                transactions_df = pd.DataFrame(transactions)
                
                # Check if transactions have supplier_id
                if 'supplier_id' in transactions_df.columns:
                    # Merge with supplier data
                    merged_df = pd.merge(
                        transactions_df,
                        suppliers_df,
                        left_on='supplier_id',
                        right_on='id',
                        how='left',
                        suffixes=('_transaction', '_supplier')
                    )
                    
                    # Group by supplier
                    supplier_spending = merged_df.groupby(['supplier_id', 'name']).agg({
                        'amount': ['sum', 'count'],
                        'date': ['min', 'max']
                    }).reset_index()
                    
                    # Flatten column names
                    supplier_spending.columns = ['supplier_id', 'supplier_name', 'total_spent', 'transaction_count', 'first_purchase', 'last_purchase']
                    
                    # Display summary
                    st.dataframe(
                        supplier_spending[['supplier_name', 'total_spent', 'transaction_count', 'first_purchase', 'last_purchase']],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "supplier_name": "Supplier",
                            "total_spent": st.column_config.NumberColumn("Total Spent", format="€%.2f"),
                            "transaction_count": "Purchase Count",
                            "first_purchase": "First Purchase",
                            "last_purchase": "Last Purchase"
                        }
                    )
                    
                    # Spending chart
                    st.subheader("Supplier Spending Analysis")
                    
                    fig = px.bar(
                        supplier_spending.nlargest(10, 'total_spent'),
                        x='supplier_name',
                        y='total_spent',
                        title='Top 10 Suppliers by Spending',
                        color='total_spent',
                        color_continuous_scale='Viridis',
                        labels={'supplier_name': 'Supplier', 'total_spent': 'Total Spent (€)'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Select supplier for detailed view
                    selected_supplier = st.selectbox(
                        "View detailed purchases for:",
                        options=[f"{s['id']}: {s['name']}" for s in suppliers],
                        key="supplier_detail_select"
                    )
                    
                    if selected_supplier:
                        supplier_id = int(selected_supplier.split(":")[0])
                        supplier_transactions = merged_df[merged_df['supplier_id'] == supplier_id]
                        
                        if not supplier_transactions.empty:
                            st.subheader(f"Purchase History: {selected_supplier.split(':')[1]}")
                            
                            # Handle date field
                            if 'transaction_date' in supplier_transactions.columns:
                                display_transactions = supplier_transactions[['transaction_date', 'amount', 'category', 'description']].copy()
                                display_transactions['transaction_date'] = pd.to_datetime(display_transactions['transaction_date']).dt.strftime('%Y-%m-%d')
                            else:
                                display_transactions = supplier_transactions[['date', 'amount', 'category', 'description']].copy()
                                display_transactions['date'] = pd.to_datetime(display_transactions['date']).dt.strftime('%Y-%m-%d')
                            
                            display_transactions['amount'] = display_transactions['amount'].apply(lambda x: f"€{x:,.2f}")
                            
                            st.dataframe(
                                display_transactions,
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            # Statistics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                total = supplier_transactions['amount'].sum()
                                st.metric("Total Spent", f"€{total:,.2f}")
                            with col2:
                                avg = supplier_transactions['amount'].mean()
                                st.metric("Average Purchase", f"€{avg:,.2f}")
                            with col3:
                                count = len(supplier_transactions)
                                st.metric("Total Purchases", count)
                        else:
                            st.info("No purchases recorded for this supplier")
                else:
                    st.info("No supplier purchase data available. Transactions may not be linked to suppliers yet.")
            else:
                st.info("No supplier or transaction data available")
        else:
            st.error("Could not load data")
    except Exception as e:
        st.error(f"Error loading purchase history: {str(e)}")

def show_supplier_performance(api_url):
    st.subheader("Supplier Performance Metrics")
    
    st.info("""
    **Key Performance Indicators for Suppliers:**
    
    1. **Reliability Score** - On-time delivery and order accuracy
    2. **Cost Efficiency** - Price competitiveness and discounts
    3. **Quality Rating** - Product quality and consistency
    4. **Payment Terms** - Credit period and flexibility
    5. **Communication** - Responsiveness and support
    """)
    
    # Performance scoring template
    st.subheader("Supplier Evaluation Form")
    
    with st.form("supplier_evaluation_form"):
        supplier_name = st.selectbox("Select Supplier", ["Supplier A", "Supplier B", "Supplier C"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            reliability = st.slider("Reliability (1-10)", 1, 10, 7)
            cost_efficiency = st.slider("Cost Efficiency (1-10)", 1, 10, 6)
            quality = st.slider("Quality (1-10)", 1, 10, 8)
        
        with col2:
            payment_terms = st.slider("Payment Terms (1-10)", 1, 10, 5)
            communication = st.slider("Communication (1-10)", 1, 10, 7)
            overall = st.slider("Overall Satisfaction (1-10)", 1, 10, 7)
        
        comments = st.text_area("Comments & Notes")
        
        if st.form_submit_button("Submit Evaluation"):
            st.success("Evaluation submitted! (This would save to database in production)")
    
    # Supplier comparison chart (sample data)
    st.subheader("Supplier Comparison")
    
    comparison_data = {
        'Supplier': ['Silver World', 'Golden Beads', 'Crystal Palace', 'Leather Crafts'],
        'Reliability': [9, 7, 8, 6],
        'Cost': [7, 9, 6, 8],
        'Quality': [8, 7, 9, 7],
        'Overall': [8, 7.7, 7.7, 7]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        df_comparison,
        x='Supplier',
        y=['Reliability', 'Cost', 'Quality'],
        barmode='group',
        title='Supplier Performance Comparison',
        labels={'value': 'Score (1-10)', 'variable': 'Metric'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    st.plotly_chart(fig, use_container_width=True)