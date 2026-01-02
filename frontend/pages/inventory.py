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


# frontend/pages/inventory.py - INVENTORY MANAGEMENT
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import requests
# from datetime import datetime

# def show_inventory_page():
#     """Inventory management page"""
#     st.markdown('<h1 class="main-header">📦 Inventory Management</h1>', unsafe_allow_html=True)
    
#     tab1, tab2, tab3, tab4 = st.tabs(["📋 All Items", "➕ Add Item", "📊 Analytics", "⚠️ Low Stock"])
    
#     with tab1:
#         st.subheader("Inventory Overview")
        
#         # Fetch inventory from backend
#         try:
#             response = requests.get(
#                 f"{st.session_state.api_url}/api/inventory",
#                 headers=st.session_state.get('auth_header', {}),
#                 timeout=5
#             )
            
#             if response.status_code == 200:
#                 inventory_data = response.json()
#             else:
#                 inventory_data = []
#                 st.warning("⚠️ Could not fetch inventory data")
#         except:
#             inventory_data = []
#             st.warning("⚠️ Using demo inventory data")
        
#         if inventory_data:
#             inventory_df = pd.DataFrame(inventory_data)
#         else:
#             # Demo data
#             inventory_df = pd.DataFrame({
#                 'id': range(1, 11),
#                 'name': [
#                     'Sterling Silver Chain', 'Gold-plated Earring Hooks', 'Swarovski Crystals',
#                     'Leather Cord', 'Freshwater Pearls', 'Amethyst Beads', 'Silver Clasps',
#                     'Jewelry Boxes', 'Pliers Set', 'Shipping Boxes'
#                 ],
#                 'category': ['Materials', 'Materials', 'Materials', 'Materials', 'Materials',
#                            'Materials', 'Materials', 'Packaging', 'Tools', 'Shipping'],
#                 'unit_cost': [25.50, 0.75, 45.00, 3.20, 85.00, 32.00, 2.50, 1.80, 45.00, 0.60],
#                 'quantity': [100, 500, 50, 200, 30, 40, 300, 200, 10, 500],
#                 'reorder_level': [20, 100, 10, 40, 5, 8, 50, 40, 2, 100],
#                 'supplier': ['Silver World', 'Golden Beads', 'Crystal Palace', 'Leather Crafts',
#                            'Pearl Paradise', 'Gemstone Co.', 'Metal Findings', 'Packaging Solutions',
#                            'Tool Masters', 'Shipping Express']
#             })
        
#         # Display inventory
#         if not inventory_df.empty:
#             # Calculate inventory value
#             inventory_df['total_value'] = inventory_df['unit_cost'] * inventory_df['quantity']
            
#             # Add status column
#             def get_status(row):
#                 if row['quantity'] <= 0:
#                     return '❌ Out of Stock'
#                 elif row['quantity'] <= row.get('reorder_level', 10):
#                     return '⚠️ Low Stock'
#                 else:
#                     return '✅ In Stock'
            
#             inventory_df['status'] = inventory_df.apply(get_status, axis=1)
            
#             # Display table
#             display_cols = ['name', 'category', 'quantity', 'unit_cost', 'total_value', 'status', 'supplier']
#             st.dataframe(
#                 inventory_df[display_cols].rename(columns={
#                     'name': 'Item Name',
#                     'category': 'Category',
#                     'quantity': 'Qty',
#                     'unit_cost': 'Unit Cost (€)',
#                     'total_value': 'Total Value (€)',
#                     'status': 'Status',
#                     'supplier': 'Supplier'
#                 }),
#                 use_container_width=True,
#                 hide_index=True
#             )
            
#             # Summary stats
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 total_items = len(inventory_df)
#                 st.metric("Total Items", total_items)
            
#             with col2:
#                 total_value = inventory_df['total_value'].sum()
#                 st.metric("Total Value", f"€{total_value:,.2f}")
            
#             with col3:
#                 low_stock = len(inventory_df[inventory_df['status'] == '⚠️ Low Stock'])
#                 st.metric("Low Stock", low_stock, delta_color="inverse")
            
#             with col4:
#                 out_of_stock = len(inventory_df[inventory_df['status'] == '❌ Out of Stock'])
#                 st.metric("Out of Stock", out_of_stock, delta_color="inverse")
#         else:
#             st.info("📭 No inventory items found")
    
#     with tab2:
#         st.subheader("Add New Inventory Item")
        
#         with st.form("add_inventory_item", clear_on_submit=True):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 name = st.text_input("Item Name *", placeholder="e.g., Sterling Silver Chain")
#                 category = st.selectbox(
#                     "Category *",
#                     ["Materials", "Packaging", "Tools", "Shipping", "Office Supplies", "Other"]
#                 )
#                 unit_cost = st.number_input(
#                     "Unit Cost (€) *",
#                     min_value=0.01,
#                     value=10.00,
#                     step=0.01,
#                     format="%.2f"
#                 )
            
#             with col2:
#                 quantity = st.number_input("Initial Quantity *", min_value=0, value=10)
#                 reorder_level = st.number_input("Reorder Level *", min_value=1, value=10)
#                 supplier = st.text_input("Supplier", placeholder="e.g., Silver World Inc.")
            
#             description = st.text_area(
#                 "Description",
#                 placeholder="Item specifications, notes...",
#                 height=100
#             )
            
#             col_submit1, col_submit2 = st.columns([2, 1])
#             with col_submit1:
#                 submitted = st.form_submit_button("💾 Save Item", type="primary", use_container_width=True)
#             with col_submit2:
#                 st.form_submit_button("🗑️ Clear", type="secondary", use_container_width=True)
            
#             if submitted:
#                 if not name:
#                     st.error("❌ Item name is required!")
#                 elif unit_cost <= 0:
#                     st.error("❌ Unit cost must be greater than 0")
#                 else:
#                     # Prepare data for backend
#                     item_data = {
#                         "name": name,
#                         "category": category,
#                         "unit_cost": float(unit_cost),
#                         "quantity": int(quantity),
#                         "reorder_level": int(reorder_level),
#                         "supplier": supplier,
#                         "description": description
#                     }
                    
#                     try:
#                         response = requests.post(
#                             f"{st.session_state.api_url}/api/inventory",
#                             json=item_data,
#                             headers=st.session_state.get('auth_header', {}),
#                             timeout=5
#                         )
                        
#                         if response.status_code == 200:
#                             st.success(f"✅ Item '{name}' added successfully!")
#                             st.balloons()
#                         else:
#                             st.error(f"❌ Failed to add item: {response.text}")
#                     except Exception as e:
#                         st.success(f"✅ Item '{name}' added (demo mode)!")
#                         st.balloons()
    
#     with tab3:
#         st.subheader("Inventory Analytics")
        
#         if 'inventory_df' in locals() and not inventory_df.empty:
#             # Category distribution
#             st.subheader("Inventory by Category")
            
#             category_dist = inventory_df.groupby('category')['total_value'].sum().reset_index()
            
#             fig1 = px.pie(
#                 category_dist,
#                 values='total_value',
#                 names='category',
#                 title='Inventory Value by Category',
#                 hole=0.4
#             )
            
#             fig1.update_layout(
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font_color='#F1F5F9'
#             )
            
#             st.plotly_chart(fig1, use_container_width=True)
            
#             # Top 10 items by value
#             st.subheader("Top 10 Items by Inventory Value")
            
#             top_items = inventory_df.nlargest(10, 'total_value')
            
#             fig2 = px.bar(
#                 top_items,
#                 x='name',
#                 y='total_value',
#                 title='Most Valuable Inventory Items',
#                 color='total_value',
#                 color_continuous_scale='viridis',
#                 labels={'name': 'Item', 'total_value': 'Value (€)'}
#             )
            
#             fig2.update_layout(
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font_color='#F1F5F9',
#                 xaxis_tickangle=-45
#             )
            
#             st.plotly_chart(fig2, use_container_width=True)
            
#             # Inventory aging (demo - would need purchase dates in real app)
#             st.subheader("Inventory Turnover")
            
#             turnover_data = pd.DataFrame({
#                 'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
#                 'Items Sold': [45, 52, 48, 61, 55, 68],
#                 'Items Received': [50, 60, 45, 55, 65, 70]
#             })
            
#             fig3 = go.Figure()
#             fig3.add_trace(go.Scatter(
#                 x=turnover_data['Month'],
#                 y=turnover_data['Items Sold'],
#                 mode='lines+markers',
#                 name='Items Sold',
#                 line=dict(color='#8B5CF6', width=3)
#             ))
#             fig3.add_trace(go.Scatter(
#                 x=turnover_data['Month'],
#                 y=turnover_data['Items Received'],
#                 mode='lines+markers',
#                 name='Items Received',
#                 line=dict(color='#10B981', width=3)
#             ))
            
#             fig3.update_layout(
#                 title='Inventory Turnover Trend',
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font_color='#F1F5F9'
#             )
            
#             st.plotly_chart(fig3, use_container_width=True)
#         else:
#             st.info("📊 Load inventory data to see analytics")
    
#     with tab4:
#         st.subheader("Low Stock & Reorder Alerts")
        
#         if 'inventory_df' in locals() and not inventory_df.empty:
#             # Filter low stock items
#             low_stock_df = inventory_df[
#                 (inventory_df['quantity'] <= inventory_df.get('reorder_level', 10)) |
#                 (inventory_df['quantity'] == 0)
#             ].copy()
            
#             if not low_stock_df.empty:
#                 # Calculate need to order
#                 low_stock_df['need_to_order'] = low_stock_df.apply(
#                     lambda row: max(row.get('reorder_level', 10) * 2 - row['quantity'], 0),
#                     axis=1
#                 )
                
#                 # Add estimated cost
#                 low_stock_df['estimated_cost'] = low_stock_df['need_to_order'] * low_stock_df['unit_cost']
                
#                 st.warning(f"⚠️ **{len(low_stock_df)} items need attention**")
                
#                 # Display low stock items
#                 display_cols = ['name', 'category', 'quantity', 'reorder_level', 'need_to_order', 'estimated_cost', 'supplier']
#                 st.dataframe(
#                     low_stock_df[display_cols].rename(columns={
#                         'name': 'Item Name',
#                         'category': 'Category',
#                         'quantity': 'Current Qty',
#                         'reorder_level': 'Reorder Level',
#                         'need_to_order': 'Need to Order',
#                         'estimated_cost': 'Est. Cost (€)',
#                         'supplier': 'Supplier'
#                     }),
#                     use_container_width=True,
#                     hide_index=True
#                 )
                
#                 # Reorder summary
#                 st.subheader("Reorder Summary")
                
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     total_to_order = low_stock_df['need_to_order'].sum()
#                     st.metric("Total Items to Order", total_to_order)
                
#                 with col2:
#                     total_cost = low_stock_df['estimated_cost'].sum()
#                     st.metric("Estimated Cost", f"€{total_cost:.2f}")
                
#                 with col3:
#                     unique_suppliers = low_stock_df['supplier'].nunique()
#                     st.metric("Suppliers Needed", unique_suppliers)
                
#                 # Generate purchase order
#                 st.subheader("Generate Purchase Order")
                
#                 if st.button("📋 Generate PO for All Items", use_container_width=True):
#                     po_content = "PURCHASE ORDER\n================\n\n"
#                     po_content += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
#                     po_content += f"Supplier: Multiple\n\n"
#                     po_content += "ITEMS TO ORDER:\n"
                    
#                     for _, row in low_stock_df.iterrows():
#                         po_content += f"- {row['name']}: {row['need_to_order']} units @ €{row['unit_cost']:.2f} each = €{row['estimated_cost']:.2f}\n"
                    
#                     po_content += f"\nTOTAL ESTIMATED COST: €{total_cost:.2f}"
                    
#                     st.download_button(
#                         label="📥 Download Purchase Order",
#                         data=po_content,
#                         file_name="purchase_order.txt",
#                         mime="text/plain"
#                     )
#             else:
#                 st.success("✅ All inventory items are sufficiently stocked!")
#         else:
#             st.info("📊 No inventory data available")

# # Inventory reports
# def generate_inventory_report():
#     """Generate inventory report"""
#     st.markdown('<h1 class="main-header">📄 Inventory Report</h1>', unsafe_allow_html=True)
    
#     # Report parameters
#     col1, col2 = st.columns(2)
#     with col1:
#         report_type = st.selectbox(
#             "Report Type",
#             ["Stock Status", "Valuation", "Turnover", "Supplier Analysis"]
#         )
#     with col2:
#         date_range = st.selectbox(
#             "Date Range",
#             ["Current", "Last Month", "Last Quarter", "Last Year", "Custom"]
#         )
    
#     # Generate report
#     if st.button("📊 Generate Report", use_container_width=True):
#         st.info("📄 Report generation feature coming soon!")
        
#         # Placeholder for report content
#         report_data = pd.DataFrame({
#             'Category': ['Materials', 'Packaging', 'Tools', 'Shipping'],
#             'Total Items': [45, 12, 8, 15],
#             'Total Value': [12500, 850, 1200, 450],
#             'Low Stock Items': [3, 1, 0, 2]
#         })
        
#         st.dataframe(report_data, use_container_width=True)
        
#         # Export options
#         col_export1, col_export2 = st.columns(2)
#         with col_export1:
#             if st.button("📥 Export to CSV", use_container_width=True):
#                 csv = report_data.to_csv(index=False)
#                 st.download_button(
#                     label="Download CSV",
#                     data=csv,
#                     file_name="inventory_report.csv",
#                     mime="text/csv"
#                 )
        
#         with col_export2:
#             if st.button("🖨️ Print Report", use_container_width=True):
#                 st.info("Print functionality would open print dialog")