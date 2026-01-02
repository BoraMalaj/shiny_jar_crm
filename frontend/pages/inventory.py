# frontend/pages/inventory.py - INVENTORY MANAGEMENT - FIXED VERSION (4 tabs)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import time

def show_inventory_page():
    """Inventory management page - FIXED VERSION"""
    st.markdown('<h1 class="main-header">📦 Inventory Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Items", "➕ Add Item", "📊 Analytics", "⚠️ Low Stock"])
    
    with tab1:
        show_inventory_items_tab()
    
    with tab2:
        show_add_item_tab()
    
    with tab3:
        show_inventory_analytics_tab()
    
    with tab4:
        show_low_stock_tab()


def show_inventory_items_tab():
    """Tab 1: All inventory items"""
    st.subheader("📋 Inventory Overview")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search items...", placeholder="Name, category",
                                    key="inv_search_tab1")
    
    with col2:
        category_filter = st.selectbox("Category", ["All", "Materials", "Packaging", "Tools", "Other"],
                                      key="inv_category_tab1")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True, key="inv_refresh_tab1"):
            st.rerun()
    
    try:
        # Fetch inventory from backend
        from auth import auth
        headers = auth.get_auth_header()
        api_url = st.session_state.get('api_url', 'http://localhost:8000')
        
        response = requests.get(f"{api_url}/api/inventory", headers=headers, timeout=10)
        
        if response.status_code == 200:
            items = response.json()
            
            if items:
                # Process items
                display_items = []
                for item in items:
                    quantity = item.get('quantity', 0)
                    reorder_level = item.get('reorder_level', 10)
                    
                    # Determine status
                    if quantity <= 0:
                        status = "🔴 Out"
                        status_color = "red"
                    elif quantity <= reorder_level:
                        status = "🟡 Low"
                        status_color = "orange"
                    else:
                        status = "🟢 Good"
                        status_color = "green"
                    
                    display_items.append({
                        "ID": item.get('id', ''),
                        "Name": item.get('name', ''),
                        "Category": item.get('category', ''),
                        "Quantity": quantity,
                        "Reorder Level": reorder_level,
                        "Unit Cost": f"€{item.get('unit_cost', 0):,.2f}",
                        "Total Value": f"€{quantity * item.get('unit_cost', 0):,.2f}",
                        "Status": status,
                        "Supplier": str(item.get('supplier_id', ''))
                    })
                
                # Apply filters
                filtered_items = display_items
                
                if search_query:
                    filtered_items = [item for item in filtered_items 
                                    if search_query.lower() in item['Name'].lower() 
                                    or search_query.lower() in item['Category'].lower()]
                
                if category_filter != "All":
                    filtered_items = [item for item in filtered_items 
                                    if item['Category'] == category_filter]
                
                if filtered_items:
                    df = pd.DataFrame(filtered_items)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Quick stats
                    total_value = sum(float(item['Total Value'].replace('€', '').replace(',', '')) 
                                    for item in filtered_items)
                    low_stock = sum(1 for item in filtered_items if "🔴" in item['Status'] or "🟡" in item['Status'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Items", len(filtered_items))
                    with col2:
                        st.metric("Total Value", f"€{total_value:,.2f}")
                    with col3:
                        st.metric("Need Attention", low_stock)
                else:
                    st.info("📭 No items match your filters")
            else:
                st.info("📭 No inventory items found")
        else:
            st.error(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def show_add_item_tab():
    """Tab 2: Add new inventory item"""
    st.subheader("➕ Add New Inventory Item")
    
    # Simple form for now
    with st.form("add_inventory_item_simple", clear_on_submit=True):
        name = st.text_input("Item Name *", placeholder="e.g., Sterling Silver Chain")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Materials", "Packaging", "Tools", "Other"])
            unit_cost = st.number_input("Unit Cost (€)", min_value=0.01, value=10.0, step=0.01)
        with col2:
            quantity = st.number_input("Initial Quantity", min_value=0, value=0, step=1)
            reorder_level = st.number_input("Reorder Level", min_value=1, value=10, step=1)
        
        description = st.text_area("Description", placeholder="Item details...", height=60)
        
        submitted = st.form_submit_button("💾 Save Item", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Item name is required")
            else:
                st.success(f"✅ Item '{name}' added!")
                st.info("Note: This is a demo. Connect to backend for real saving.")


def show_inventory_analytics_tab():
    """Tab 3: Inventory analytics"""
    st.subheader("📊 Inventory Analytics")
    
    st.info("📈 Inventory analytics coming soon!")
    
    # Placeholder analytics
    st.write("""
    ### Planned Analytics:
    
    - **Stock Value Trends**
    - **Turnover Rates**
    - **Category Performance**
    - **Supplier Analysis**
    - **Demand Forecasting**
    """)
    
    # Demo chart
    data = pd.DataFrame({
        'Category': ['Materials', 'Packaging', 'Tools', 'Other'],
        'Value': [5000, 1200, 800, 400],
        'Items': [45, 12, 8, 5]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.pie(data, values='Value', names='Category', title='Value by Category')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(data, x='Category', y='Items', title='Items by Category')
        st.plotly_chart(fig2, use_container_width=True)


def show_low_stock_tab():
    """Tab 4: Low stock alerts"""
    st.subheader("⚠️ Low Stock & Reorder Alerts")
    
    # Demo low stock items
    low_stock_items = [
        {"Name": "Sterling Silver Chain", "Current": 5, "Reorder": 20, "Need": 15, "Supplier": "Silver World"},
        {"Name": "Gold-plated Hooks", "Current": 8, "Reorder": 50, "Need": 42, "Supplier": "Golden Beads"},
        {"Name": "Swarovski Crystals", "Current": 3, "Reorder": 25, "Need": 22, "Supplier": "Crystal Palace"},
        {"Name": "Velvet Boxes", "Current": 12, "Reorder": 40, "Need": 28, "Supplier": "Packaging Solutions"}
    ]
    
    if low_stock_items:
        df = pd.DataFrame(low_stock_items)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.warning(f"⚠️ **{len(low_stock_items)} items need reordering!**")
        
        # Generate reorder list
        if st.button("📋 Generate Purchase Order", use_container_width=True):
            po_text = "PURCHASE ORDER - Shiny Jar\n" + "="*40 + "\n"
            for item in low_stock_items:
                po_text += f"\n{item['Name']}: Order {item['Need']} units from {item['Supplier']}"
            
            st.text_area("Purchase Order Draft", po_text, height=200)
    else:
        st.success("✅ All items are well stocked!")


def generate_inventory_report():
    """Generate inventory report - FIXED"""
    st.markdown('<h1 class="main-header">📄 Inventory Report</h1>', unsafe_allow_html=True)
    
    # Report parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox("Report Type", 
                                 ["Stock Levels", "Low Stock", "Valuation", "Turnover"])
    
    with col2:
        as_of_date = st.date_input("As of Date", value=datetime.now())
    
    with col3:
        format_type = st.selectbox("Format", ["Screen", "PDF", "CSV"])
    
    # Generate report button
    if st.button("📊 Generate Report", use_container_width=True, type="primary"):
        st.success(f"✅ Generating {report_type} report for {as_of_date}...")
        
        # Demo report content
        st.markdown("""
        ### 📋 Inventory Summary Report
        **Date:** {date}  
        **Type:** {type} Report  
        **Generated:** {now}
        
        ---
        
        #### Key Metrics:
        - **Total Items:** 125
        - **Total Value:** €15,842.50
        - **Low Stock Items:** 8
        - **Out of Stock:** 2
        - **Avg. Stock Value:** €126.74
        
        ---
        
        #### Top 5 Items by Value:
        1. **Diamond Beads** - €2,450.00
        2. **Gold Chains** - €1,850.00  
        3. **Silver Sheets** - €1,250.00
        4. **Pearl Strands** - €980.00
        5. **Crystal Packs** - €750.00
        
        ---
        
        #### Recommendations:
        1. Reorder **Sterling Silver Chain** (only 5 left)
        2. Check **Gold-plated Hooks** stock (8 left)
        3. Consider bulk purchase of **Packaging Boxes**
        """.format(date=as_of_date, type=report_type, now=datetime.now().strftime("%Y-%m-%d %H:%M")))
        
        if format_type == "PDF":
            st.info("📄 PDF export functionality coming soon!")
        elif format_type == "CSV":
            st.info("📥 CSV export functionality coming soon!")
