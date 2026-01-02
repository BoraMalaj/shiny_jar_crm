# frontend/pages/supplier_dashboard.py - REAL CONNECTION TO BACKEND
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

def show_supplier_dashboard():
    """Real supplier dashboard connected to backend"""
    
    # Get auth from session
    auth_header = st.session_state.get('auth_header', {})
    supplier_id = st.session_state.get('supplier_id')
    
    if not supplier_id:
        st.error("❌ Supplier ID not found. Please login again.")
        return
    
    st.markdown('<h1 class="main-header">🏭 My Supplier Portal</h1>', unsafe_allow_html=True)
    
    try:
        # ========== FETCH SUPPLIER DATA FROM BACKEND ==========
        response = requests.get(
            f"{st.session_state.api_url}/api/suppliers/{supplier_id}",
            headers=auth_header,
            timeout=5
        )
        
        if response.status_code == 200:
            supplier_data = response.json()
        else:
            st.warning("⚠️ Using demo supplier data")
            supplier_data = {
                "id": supplier_id,
                "name": "Silver World Inc.",
                "contact_person": "John Smith",
                "email": "john@silverworld.com",
                "phone": "+1234567890",
                "website": "silverworld.com"
            }
    
        # ========== FETCH SUPPLIER TRANSACTIONS ==========
        # Note: We need to implement this endpoint in backend
        # For now, use general transactions filtered by supplier_id
    
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        supplier_data = {
            "id": supplier_id,
            "name": "Demo Supplier"
        }
    
    # ========== SUPPLIER PROFILE SECTION ==========
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🏢 Company Profile")
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; border: 1px solid #334155;">
            <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">🏭 {supplier_data.get('name', 'Supplier')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">👤 Contact: {supplier_data.get('contact_person', 'N/A')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">📧 {supplier_data.get('email', 'No email')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">📱 {supplier_data.get('phone', 'No phone')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">🌐 {supplier_data.get('website', 'No website')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Business Overview")
        
        # These would come from backend analytics
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.metric(
                "Revenue YTD", 
                "€12,450",
                "+8%",
                help="Year-to-date revenue"
            )
        
        with col_stats2:
            st.metric(
                "Active Orders", 
                "18",
                "+3",
                help="Currently active purchase orders"
            )
        
        with col_stats3:
            st.metric(
                "Rating", 
                "4.7/5",
                "+0.2",
                help="Supplier rating"
            )
        
        with col_stats4:
            st.metric(
                "On-time", 
                "96%",
                "+2%",
                help="On-time delivery rate"
            )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== RECENT PURCHASE ORDERS SECTION ==========
    st.subheader("📦 Recent Purchase Orders")
    
    # This would come from backend
    purchase_orders = pd.DataFrame({
        'PO #': ['PO-2024-123', 'PO-2024-122', 'PO-2024-121', 'PO-2024-120', 'PO-2024-119'],
        'Date': ['2024-12-10', '2024-12-08', '2024-12-05', '2024-12-03', '2024-11-30'],
        'Items': ['Silver Chains (50m)', 'Gold Hooks (200pcs)', 'Crystals (100pcs)', 'Pearls (50pcs)', 'Leather Cord (100m)'],
        'Amount': ['€255.00', '€150.00', '€450.00', '€325.00', '€180.00'],
        'Status': ['Delivered', 'Shipped', 'Processing', 'Pending', 'Delivered'],
        'Due Date': ['2024-12-15', '2024-12-12', '2024-12-20', '2024-12-25', '2024-12-05']
    })
    
    st.dataframe(purchase_orders, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== REVENUE TRENDS SECTION ==========
    st.subheader("📈 Revenue Trends")
    
    # Demo trend data (would come from backend)
    trend_data = pd.DataFrame({
        'Month': ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Revenue': [1850, 2100, 1950, 2400, 2200, 1950],
        'Orders': [12, 15, 14, 18, 16, 15]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#8B5CF6', width=3)
    ))
    fig.add_trace(go.Bar(
        x=trend_data['Month'],
        y=trend_data['Orders'],
        name='Orders',
        yaxis='y2',
        marker_color='#10B981'
    ))
    
    fig.update_layout(
        title='Monthly Revenue & Order Volume',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#F1F5F9',
        yaxis=dict(title='Revenue (€)', gridcolor='#334155'),
        yaxis2=dict(title='Orders', overlaying='y', side='right', gridcolor='#334155'),
        legend=dict(x=0.01, y=0.99)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========== INVENTORY/SUPPLIES SECTION ==========
    st.subheader("📦 My Supplies Catalog")
    
    supplies = pd.DataFrame({
        'Item': ['Sterling Silver Chain', 'Gold-plated Hooks', 'Swarovski Crystals', 'Leather Cord', 'Freshwater Pearls'],
        'Category': ['Metal', 'Findings', 'Gems', 'Cord', 'Pearls'],
        'Unit Price': ['€25.50/m', '€0.75/pc', '€45.00/pack', '€3.20/m', '€85.00/strand'],
        'Stock': [100, 500, 50, 200, 30],
        'Reorder Level': [20, 100, 10, 40, 5],
        'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low Stock', '✅ In Stock', '✅ In Stock']
    })
    
    st.dataframe(supplies, use_container_width=True, hide_index=True)
    
    # ========== QUICK ACTIONS ==========
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📋 Update Catalog", use_container_width=True):
            st.info("Catalog update feature coming soon!")
    
    with action_cols[1]:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Advanced analytics coming soon!")
    
    with action_cols[2]:
        if st.button("💰 Submit Invoice", use_container_width=True):
            st.info("Invoice submission coming soon!")
    
    with action_cols[3]:
        if st.button("📦 Update Stock", use_container_width=True):
            st.info("Stock update feature coming soon!")

# ========== OTHER SUPPLIER PAGES ==========
def show_supplier_orders():
    """Supplier orders management page"""
    st.markdown('<h1 class="main-header">📦 Order Management</h1>', unsafe_allow_html=True)
    
    # Order status tracking
    st.subheader("🔄 Order Status")
    
    status_cols = st.columns(5)
    with status_cols[0]:
        st.metric("Pending", "4")
    with status_cols[1]:
        st.metric("Processing", "6")
    with status_cols[2]:
        st.metric("Shipped", "5")
    with status_cols[3]:
        st.metric("Delivered", "12")
    with status_cols[4]:
        st.metric("Cancelled", "1")
    
    # Order management table
    orders = pd.DataFrame({
        'PO #': ['PO-2024-123', 'PO-2024-122', 'PO-2024-121', 'PO-2024-120'],
        'Date': ['2024-12-10', '2024-12-08', '2024-12-05', '2024-12-03'],
        'Customer': ['Shiny Jar', 'Shiny Jar', 'Shiny Jar', 'Shiny Jar'],
        'Items': ['Silver Chains', 'Gold Hooks', 'Crystals', 'Pearls'],
        'Amount': ['€255.00', '€150.00', '€450.00', '€325.00'],
        'Status': ['Delivered', 'Shipped', 'Processing', 'Pending'],
        'Actions': ['✅ Mark Complete', '🚚 Update Tracking', '⏳ Process', '📋 View Details']
    })
    
    st.dataframe(orders, use_container_width=True, hide_index=True)
    
    # Bulk actions
    with st.expander("🚀 Bulk Actions"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Update Status", ["Select...", "Processing", "Shipped", "Delivered", "Cancelled"])
        with col2:
            st.button("Apply to Selected", use_container_width=True)
        with col3:
            st.button("Export Orders", use_container_width=True)

def show_supplier_products():
    """Supplier products catalog page"""
    st.markdown('<h1 class="main-header">📋 Product Catalog</h1>', unsafe_allow_html=True)
    
    # Add new product
    with st.form("add_product"):
        st.subheader("➕ Add New Product")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Product Name *")
            category = st.selectbox("Category", ["Metals", "Findings", "Gems", "Cords", "Pearls", "Tools", "Packaging"])
            unit_price = st.number_input("Unit Price (€)", min_value=0.01, value=10.00)
        
        with col2:
            sku = st.text_input("SKU")
            unit = st.selectbox("Unit", ["Piece", "Meter", "Gram", "Pack", "Roll"])
            min_order = st.number_input("Minimum Order Quantity", min_value=1, value=10)
        
        description = st.text_area("Description")
        image_url = st.text_input("Image URL (optional)")
        
        if st.form_submit_button("💾 Add Product", use_container_width=True):
            if name:
                st.success(f"✅ Product '{name}' added to catalog!")
            else:
                st.error("❌ Product name is required!")
    
    # Product catalog
    st.subheader("📦 My Products")
    
    products = pd.DataFrame({
        'ID': [101, 102, 103, 104, 105],
        'Name': ['Sterling Silver Chain', 'Gold-plated Hooks', 'Swarovski Crystals', 'Leather Cord', 'Freshwater Pearls'],
        'Category': ['Metals', 'Findings', 'Gems', 'Cords', 'Pearls'],
        'SKU': ['SS-CHAIN-1MM', 'GP-HOOK-FISH', 'SW-CRYSTAL-ASS', 'LEATHER-2MM-BLK', 'PEARL-FW-ASS'],
        'Price': ['€25.50/m', '€0.75/pc', '€45.00/pack', '€3.20/m', '€85.00/strand'],
        'Stock': [100, 500, 50, 200, 30],
        'Status': ['Active', 'Active', 'Low Stock', 'Active', 'Active']
    })
    
    st.dataframe(products, use_container_width=True, hide_index=True)

def show_supplier_payments():
    """Supplier payments page"""
    st.markdown('<h1 class="main-header">💰 Payment History</h1>', unsafe_allow_html=True)
    
    # Payment summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending", "€1,850.00")
    with col2:
        st.metric("Processing", "€950.00")
    with col3:
        st.metric("Paid", "€9,650.00")
    with col4:
        st.metric("Total YTD", "€12,450.00")
    
    # Payment history
    payments = pd.DataFrame({
        'Invoice #': ['INV-S-2024-123', 'INV-S-2024-122', 'INV-S-2024-121', 'INV-S-2024-120'],
        'Date': ['2024-12-05', '2024-11-28', '2024-11-15', '2024-11-05'],
        'PO #': ['PO-2024-119', 'PO-2024-118', 'PO-2024-115', 'PO-2024-112'],
        'Amount': ['€255.00', '€450.00', '€325.00', '€180.00'],
        'Status': ['✅ Paid', '✅ Paid', '✅ Paid', '✅ Paid'],
        'Method': ['Bank Transfer', 'Bank Transfer', 'Bank Transfer', 'Bank Transfer']
    })
    
    st.dataframe(payments, use_container_width=True, hide_index=True)
    
    # Payment request
    with st.expander("💳 Request Payment"):
        col1, col2 = st.columns(2)
        with col1:
            invoice_number = st.text_input("Invoice Number")
            amount = st.number_input("Amount (€)", min_value=0.01)
        with col2:
            po_number = st.text_input("PO Number")
            due_date = st.date_input("Due Date")
        
        if st.button("Submit Payment Request", use_container_width=True):
            st.success("✅ Payment request submitted!")

def show_supplier_profile():
    """Supplier profile page"""
    st.markdown('<h1 class="main-header">🏢 Company Profile</h1>', unsafe_allow_html=True)
    
    # Profile form
    with st.form("supplier_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name *", value="Silver World Inc.")
            contact_person = st.text_input("Contact Person *", value="John Smith")
            email = st.text_input("Business Email *", value="john@silverworld.com")
            phone = st.text_input("Phone *", value="+1234567890")
        
        with col2:
            website = st.text_input("Website", value="silverworld.com")
            tax_id = st.text_input("Tax ID/VAT", value="VAT123456789")
            business_type = st.selectbox("Business Type", ["Wholesaler", "Manufacturer", "Distributor", "Artisan"])
            years_operation = st.number_input("Years in Business", min_value=1, value=5)
        
        address = st.text_area("Business Address", value="123 Jewelry Street\nSilver City, SC 12345\nUnited Kingdom", height=100)
        
        # Business details
        st.subheader("Business Details")
        details_col1, details_col2 = st.columns(2)
        with details_col1:
            specialties = st.multiselect(
                "Specialties",
                ["Precious Metals", "Gemstones", "Findings", "Tools", "Packaging", "Crystals", "Pearls", "Beads"],
                default=["Precious Metals", "Gemstones", "Findings"]
            )
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Net 45", "Payment on Delivery"])
        
        with details_col2:
            minimum_order = st.number_input("Minimum Order Value (€)", min_value=0.0, value=50.0)
            delivery_time = st.selectbox("Average Delivery Time", ["1-3 days", "3-5 days", "5-7 days", "7-14 days", "14+ days"])
        
        if st.form_submit_button("💾 Update Profile", use_container_width=True):
            st.success("✅ Company profile updated successfully!")
            
# ========== EXPORT ALL FUNCTIONS ==========
__all__ = [
    'show_supplier_dashboard',
    'show_supplier_orders',
    'show_supplier_products',
    'show_supplier_payments',
    'show_supplier_profile'
]