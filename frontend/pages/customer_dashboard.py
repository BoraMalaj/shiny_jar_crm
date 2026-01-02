# frontend/pages/customer_dashboard.py - REAL CONNECTION TO BACKEND
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# Customer Dashboard Backend real Data
def show_customer_dashboard():
    """Customer dashboard with real backend data"""
    st.markdown('<h1 class="main-header">👤 Customer Portal</h1>', unsafe_allow_html=True)
    
    # Get customer ID from session
    customer_id = st.session_state.get('customer_id')
    username = auth.get_username()
    
    if auth.is_demo_mode():
        st.info("🎮 Demo Mode - Using sample data")
        show_customer_demo_data()
        return
    
    if not customer_id:
        st.warning("⚠️ No customer ID found in session. Using demo data.")
        show_customer_demo_data()
        return
    
    try:
        headers = auth.get_auth_header()
        api_url = st.session_state.api_url
        
        # Fetch customer dashboard data
        with st.spinner("🔄 Loading your dashboard..."):
            response = requests.get(
                f"{api_url}/api/customers/{customer_id}/dashboard",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                display_customer_real_data(data, customer_id)
            elif response.status_code == 404:
                st.error("❌ Customer profile not found in database")
                show_customer_demo_data()
            elif response.status_code == 403:
                st.error("⛔ You don't have permission to view this customer data")
                show_customer_demo_data()
            else:
                st.error(f"❌ API Error {response.status_code}")
                show_customer_demo_data()
                
    except requests.exceptions.ConnectionError:
        st.error("🔌 Could not connect to backend")
        show_customer_demo_data()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        show_customer_demo_data()

def display_customer_real_data(data, customer_id):
    """Display real customer data from backend"""
    customer = data.get('customer', {})
    stats = data.get('stats', {})
    recent_orders = data.get('recent_orders', [])
    
    # Welcome message
    st.success(f"✅ Welcome back, **{customer.get('name', 'Customer')}**!")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Spent", f"€{customer.get('total_spent', 0):,.2f}")
    with col2:
        st.metric("📦 Total Orders", stats.get('order_count', 0))
    with col3:
        avg_order = stats.get('avg_order_value', 0)
        st.metric("📊 Avg Order", f"€{avg_order:,.2f}")
    with col4:
        tier = stats.get('loyalty_tier', 'New')
        st.metric("🏆 Loyalty Tier", tier)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Recent Orders Section
    st.subheader("🛍️ Recent Orders")
    
    if recent_orders:
        # Create DataFrame for orders
        orders_df = pd.DataFrame(recent_orders)
        
        # Format columns
        if 'date' in orders_df.columns:
            orders_df['date'] = pd.to_datetime(orders_df['date']).dt.strftime('%Y-%m-%d')
        if 'amount' in orders_df.columns:
            orders_df['amount'] = orders_df['amount'].apply(lambda x: f"€{x:,.2f}")
        
        # Display
        st.dataframe(
            orders_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.Column(visible=False),
                "description": st.column_config.Column(width="large"),
            }
        )
        
        # View all orders button
        if st.button("📋 View All Orders", use_container_width=True):
            st.session_state.page = "My Orders"
            st.rerun()
    else:
        st.info("📭 No recent orders found")
        st.markdown("""
        **Next Steps:**
        - Browse our collection in the shop
        - Place your first order
        - Contact support if you need help
        """)
    
    # Customer Info
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("👤 Your Information")
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown(f"""
        **Name:** {customer.get('name', 'N/A')}  
        **Email:** {customer.get('email', 'N/A')}  
        **Customer Since:** {customer.get('customer_since', 'N/A')}
        """)
    
    with info_col2:
        st.markdown(f"""
        **Instagram:** @{customer.get('instagram_handle', 'N/A')}  
        **Last Purchase:** {customer.get('last_purchase', 'Never')}  
        **Customer ID:** {customer_id}
        """)
    
    # Quick Actions
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(3)
    with action_cols[0]:
        if st.button("🛒 Browse Shop", use_container_width=True):
            st.info("🛍️ Online shop coming soon!")
    
    with action_cols[1]:
        if st.button("📞 Contact Support", use_container_width=True):
            st.info("📧 Email: support@shinyjar.com")
    
    with action_cols[2]:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

# def show_customer_demo_data():
#     """Fallback demo data for customer"""
#     # ... keep existing demo customer dashboard code - check below the name of the demo dashboard method ...

# Customer Dashboard Demo Data
def show_customer_demo_dashboard():
    """Real customer dashboard connected to backend"""
    
    # Get auth from session
    auth_header = st.session_state.get('auth_header', {})
    customer_id = st.session_state.get('customer_id')
    
    if not customer_id:
        st.error("❌ Customer ID not found. Please login again.")
        return
    
    st.markdown('<h1 class="main-header">👤 My Customer Portal</h1>', unsafe_allow_html=True)
    
    try:
        # ========== FETCH CUSTOMER DATA FROM BACKEND ==========
        response = requests.get(
            f"{st.session_state.api_url}/api/customers/{customer_id}",
            headers=auth_header,
            timeout=5
        )
        
        if response.status_code == 200:
            customer_data = response.json()
        else:
            st.warning("⚠️ Using demo customer data")
            customer_data = {
                "id": customer_id,
                "name": "Maria Silva",
                "email": "maria@email.com",
                "instagram_handle": "@maria_jewelry",
                "total_spent": 1250.75,
                "customer_since": "2023-01-15",
                "last_purchase": "2024-12-10"
            }
    
        # ========== FETCH CUSTOMER TRANSACTIONS ==========
        transactions_response = requests.get(
            f"{st.session_state.api_url}/api/customers/{customer_id}/transactions",
            headers=auth_header,
            timeout=5
        )
        
        if transactions_response.status_code == 200:
            transactions_data = transactions_response.json().get('transactions', [])
        else:
            transactions_data = []
    
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        customer_data = {
            "id": customer_id,
            "name": "Demo Customer",
            "total_spent": 1250.75
        }
        transactions_data = []
    
    # ========== CUSTOMER PROFILE SECTION ==========
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 My Profile")
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; border: 1px solid #334155;">
            <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">👤 {customer_data.get('name', 'Customer')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">📧 {customer_data.get('email', 'No email')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">📱 {customer_data.get('instagram_handle', 'No Instagram')}</p>
            <p style="color: #94A3B8; margin: 0.5rem 0;">🎯 Customer since: {customer_data.get('customer_since', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💰 Spending Overview")
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric(
                "Total Spent", 
                f"€{customer_data.get('total_spent', 0):.2f}",
                help="Total amount spent with us"
            )
        
        with col_stats2:
            # Calculate average order value
            total_spent = customer_data.get('total_spent', 0)
            order_count = len(transactions_data) if transactions_data else 1
            avg_order = total_spent / order_count if order_count > 0 else 0
            st.metric(
                "Avg. Order", 
                f"€{avg_order:.2f}",
                help="Average value per order"
            )
        
        with col_stats3:
            st.metric(
                "Orders", 
                len(transactions_data),
                help="Total number of orders"
            )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== RECENT ORDERS SECTION ==========
    st.subheader("🛍️ My Recent Orders")
    
    if transactions_data:
        orders_df = pd.DataFrame(transactions_data)
        
        # Format the data
        if not orders_df.empty:
            orders_df['date'] = pd.to_datetime(orders_df.get('date', orders_df.get('transaction_date', '')))
            orders_df['date_str'] = orders_df['date'].dt.strftime('%Y-%m-%d')
            orders_df['amount_formatted'] = orders_df['amount'].apply(lambda x: f"€{x:.2f}")
            
            st.dataframe(
                orders_df[['date_str', 'description', 'amount_formatted', 'status']].rename(
                    columns={'date_str': 'Date', 'description': 'Description', 
                            'amount_formatted': 'Amount', 'status': 'Status'}
                ),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📭 No orders found")
    else:
        # Fallback demo data
        demo_orders = pd.DataFrame({
            'Date': ['2024-12-10', '2024-12-05', '2024-11-28'],
            'Order #': ['ORD-00123', 'ORD-00122', 'ORD-00121'],
            'Items': ['Silver Necklace', 'Gold Earrings Set', 'Custom Bracelet'],
            'Amount': ['€89.00', '€145.50', '€220.00'],
            'Status': ['Delivered', 'Shipped', 'Delivered']
        })
        
        st.dataframe(demo_orders, use_container_width=True, hide_index=True)
        st.caption("ℹ️ Demo data - Connect to backend for real orders")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ========== SPENDING TRENDS SECTION ==========
    st.subheader("📈 My Spending Trends")
    
    if transactions_data and len(transactions_data) > 1:
        # Create monthly spending trend
        trend_df = pd.DataFrame(transactions_data)
        trend_df['month'] = pd.to_datetime(trend_df['date']).dt.to_period('M')
        monthly_spending = trend_df.groupby('month')['amount'].sum().reset_index()
        monthly_spending['month_str'] = monthly_spending['month'].astype(str)
        
        fig = px.bar(
            monthly_spending,
            x='month_str',
            y='amount',
            title='Monthly Spending',
            labels={'month_str': 'Month', 'amount': 'Amount (€)'},
            color='amount',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#F1F5F9'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Demo chart
        trend_data = pd.DataFrame({
            'Month': ['Sep', 'Oct', 'Nov', 'Dec'],
            'Spending': [280, 320, 450, 380]
        })
        
        fig = px.line(
            trend_data,
            x='Month',
            y='Spending',
            title='Monthly Spending Trend',
            markers=True
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#F1F5F9'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("ℹ️ Demo chart - Connect to backend for real trends")
    
    # ========== WISHLIST & SAVED ITEMS SECTION ==========
    st.subheader("💝 My Wishlist")
    
    wishlist_cols = st.columns(3)
    
    with wishlist_cols[0]:
        st.markdown("""
        <div style="background: #1E293B; padding: 1rem; border-radius: 12px; border: 1px solid #334155; text-align: center;">
            <div style="font-size: 2rem;">💎</div>
            <p style="font-weight: 600; margin: 0.5rem 0;">Silver Necklace</p>
            <p style="color: #8B5CF6; font-weight: 600;">€89.00</p>
        </div>
        """, unsafe_allow_html=True)
    
    with wishlist_cols[1]:
        st.markdown("""
        <div style="background: #1E293B; padding: 1rem; border-radius: 12px; border: 1px solid #334155; text-align: center;">
            <div style="font-size: 2rem;">✨</div>
            <p style="font-weight: 600; margin: 0.5rem 0;">Gold Earrings</p>
            <p style="color: #8B5CF6; font-weight: 600;">€145.50</p>
        </div>
        """, unsafe_allow_html=True)
    
    with wishlist_cols[2]:
        st.markdown("""
        <div style="background: #1E293B; padding: 1rem; border-radius: 12px; border: 1px solid #334155; text-align: center;">
            <div style="font-size: 2rem;">🔮</div>
            <p style="font-weight: 600; margin: 0.5rem 0;">Crystal Bracelet</p>
            <p style="color: #8B5CF6; font-weight: 600;">€75.00</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== QUICK ACTIONS ==========
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📦 Track Order", use_container_width=True):
            st.info("Order tracking feature coming soon!")
    
    with action_cols[1]:
        if st.button("📧 Contact Support", use_container_width=True):
            st.info("Support contact: support@shinyjar.com")
    
    with action_cols[2]:
        if st.button("🔄 Request Return", use_container_width=True):
            st.info("Return request form coming soon!")
    
    with action_cols[3]:
        if st.button("⭐ Write Review", use_container_width=True):
            st.info("Review system coming soon!")

# ========== OTHER CUSTOMER PAGES ==========
def show_customer_orders():
    """Customer orders page"""
    st.markdown('<h1 class="main-header">🛍️ My Orders</h1>', unsafe_allow_html=True)
    
    # Fetch real orders from backend
    auth_header = st.session_state.get('auth_header', {})
    customer_id = st.session_state.get('customer_id')
    
    if customer_id:
        try:
            response = requests.get(
                f"{st.session_state.api_url}/api/customers/{customer_id}/transactions",
                headers=auth_header,
                timeout=5
            )
            
            if response.status_code == 200:
                orders_data = response.json().get('transactions', [])
                
                if orders_data:
                    orders_df = pd.DataFrame(orders_data)
                    
                    # Display orders
                    st.dataframe(
                        orders_df[['date', 'description', 'amount', 'status']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("📭 You have no orders yet")
            else:
                st.warning("⚠️ Could not fetch orders from backend")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Please login as customer")
    
    # Order filters
    with st.expander("🔍 Filter Orders"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Status", ["All", "Pending", "Shipped", "Delivered", "Cancelled"])
        with col2:
            st.selectbox("Time Period", ["All Time", "Last 30 Days", "Last 3 Months", "Last Year"])

def show_customer_invoices():
    """Customer invoices page"""
    st.markdown('<h1 class="main-header">💳 My Invoices</h1>', unsafe_allow_html=True)
    
    # Invoice data
    invoices = pd.DataFrame({
        'Invoice #': ['INV-2024-123', 'INV-2024-122', 'INV-2024-121'],
        'Date': ['2024-12-10', '2024-12-05', '2024-11-28'],
        'Amount': ['€89.00', '€145.50', '€220.00'],
        'Status': ['Paid', 'Paid', 'Paid'],
        'Download': ['📥 Download', '📥 Download', '📥 Download']
    })
    
    st.dataframe(invoices, use_container_width=True, hide_index=True)
    
    # Invoice summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Invoices", "12")
    with col2:
        st.metric("Total Paid", "€4,254.75")
    with col3:
        st.metric("Outstanding", "€0.00")

def show_customer_profile():
    """Customer profile page"""
    st.markdown('<h1 class="main-header">👤 My Profile</h1>', unsafe_allow_html=True)
    
    # Fetch customer data from backend
    auth_header = st.session_state.get('auth_header', {})
    customer_id = st.session_state.get('customer_id')
    
    if customer_id:
        try:
            response = requests.get(
                f"{st.session_state.api_url}/api/customers/{customer_id}",
                headers=auth_header,
                timeout=5
            )
            
            if response.status_code == 200:
                customer = response.json()
            else:
                customer = {}
                st.warning("⚠️ Could not fetch profile data")
                
        except Exception as e:
            customer = {}
            st.error(f"❌ Error: {str(e)}")
    else:
        customer = {}
        st.error("❌ Please login as customer")
    
    # Profile form
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=customer.get('name', ''))
            email = st.text_input("Email", value=customer.get('email', ''))
            phone = st.text_input("Phone", value=customer.get('phone', ''))
        
        with col2:
            instagram = st.text_input("Instagram", value=customer.get('instagram_handle', ''))
            address = st.text_area("Address", value=customer.get('address', ''), height=100)
        
        # Preferences
        st.subheader("Preferences")
        pref_col1, pref_col2 = st.columns(2)
        with pref_col1:
            newsletter = st.checkbox("📧 Newsletter", value=True)
            promotions = st.checkbox("🎁 Promotions", value=True)
        with pref_col2:
            sms_notifications = st.checkbox("📱 SMS Notifications", value=False)
            order_updates = st.checkbox("📦 Order Updates", value=True)
        
        if st.form_submit_button("💾 Save Profile", use_container_width=True):
            st.success("✅ Profile updated successfully!")
            
# ========== EXPORT ALL FUNCTIONS ==========
__all__ = [
    'show_customer_dashboard',
    'display_customer_real_data',
    'show_customer_demo_dashboard',
    'show_customer_orders', 
    'show_customer_invoices',
    'show_customer_profile'
]



# # frontend/pages/customer_dashboard.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import requests
# from datetime import datetime, timedelta

# def show_customer_dashboard():
#     """Customer-specific dashboard"""
    
#     # Apply styling
#     from styles import apply_global_styles
#     apply_global_styles()
    
#     st.markdown('<h1 class="main-header">👤 My Customer Dashboard</h1>', unsafe_allow_html=True)
    
#     # Get customer ID from session (you'll need to implement this)
#     customer_id = st.session_state.get('customer_id', 1)
#     api_url = st.session_state.get('api_url', 'http://localhost:8000')
    
#     # Tabs for customer view
#     tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🛍️ My Orders", "💳 Invoices", "⭐ Favorites"])
    
#     with tab1:
#         show_customer_overview(customer_id, api_url)
    
#     with tab2:
#         show_my_orders(customer_id, api_url)
    
#     with tab3:
#         show_my_invoices(customer_id, api_url)
    
#     with tab4:
#         show_my_favorites()

# def show_customer_overview(customer_id, api_url):
#     """Customer overview with their stats"""
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#         <div class="metric-card">
#             <div style="font-size: 2rem;">💰</div>
#             <div style="font-size: 1.8rem; font-weight: 700;">€1,250</div>
#             <div style="color: #64748B; font-size: 0.9rem;">Total Spent</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="metric-card">
#             <div style="font-size: 2rem;">🛒</div>
#             <div style="font-size: 1.8rem; font-weight: 700;">12</div>
#             <div style="color: #64748B; font-size: 0.9rem;">Total Orders</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="metric-card">
#             <div style="font-size: 2rem;">⭐</div>
#             <div style="font-size: 1.8rem; font-weight: 700;">4.8</div>
#             <div style="color: #64748B; font-size: 0.9rem;">Avg. Rating</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="metric-card">
#             <div style="font-size: 2rem;">🎁</div>
#             <div style="font-size: 1.8rem; font-weight: 700;">3</div>
#             <div style="color: #64748B; font-size: 0.9rem;">Loyalty Points</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.divider()
    
#     # Customer spending chart
#     st.subheader("📈 My Spending Trend")
    
#     # Sample data
#     spending_data = pd.DataFrame({
#         'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
#         'Amount': [150, 200, 180, 250, 300, 280, 320, 290, 350, 400, 380, 420]
#     })
    
#     fig = px.area(
#         spending_data,
#         x='Month',
#         y='Amount',
#         title='Monthly Spending (€)',
#         color_discrete_sequence=['#8B5CF6']
#     )
    
#     fig.update_layout(
#         height=400,
#         plot_bgcolor='white',
#         paper_bgcolor='white'
#     )
    
#     st.plotly_chart(fig, use_container_width=True)
    
#     # Recent activity
#     st.subheader("📋 Recent Activity")
    
#     activity_data = pd.DataFrame({
#         'Date': ['2024-12-10', '2024-12-05', '2024-11-28', '2024-11-20'],
#         'Activity': ['Order Completed', 'Review Submitted', 'Order Shipped', 'Product Viewed'],
#         'Details': ['Silver Necklace', '⭐⭐⭐⭐⭐', 'Tracking: #TRK12345', 'Gold Earrings'],
#         'Status': ['<span class="status-success">Completed</span>', 
#                   '<span class="status-success">Submitted</span>',
#                   '<span class="status-success">Delivered</span>',
#                   '<span class="status-warning">Viewed</span>']
#     })
    
#     # Convert to HTML for styled status
#     st.markdown(activity_data.to_html(escape=False, index=False), unsafe_allow_html=True)

# def show_my_orders(customer_id, api_url):
#     """Display customer's order history"""
    
#     st.subheader("🛍️ My Order History")
    
#     # Search and filter
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Processing", "Shipped", "Delivered", "Cancelled"])
#     with col2:
#         date_range = st.selectbox("Date Range", ["Last 30 days", "Last 3 months", "Last 6 months", "All time"])
#     with col3:
#         sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Highest Amount", "Lowest Amount"])
    
#     # Sample order data
#     orders = pd.DataFrame({
#         'Order ID': ['ORD-00123', 'ORD-00122', 'ORD-00121', 'ORD-00120', 'ORD-00119'],
#         'Date': ['2024-12-10', '2024-12-05', '2024-11-28', '2024-11-20', '2024-11-15'],
#         'Items': ['Silver Necklace', 'Gold Earrings Set', 'Custom Bracelet', 'Pearl Set', 'Birthstone Ring'],
#         'Amount': ['€89.00', '€145.50', '€220.00', '€189.99', '€75.25'],
#         'Status': ['<span class="status-success">Delivered</span>',
#                   '<span class="status-warning">Shipped</span>',
#                   '<span class="status-success">Delivered</span>',
#                   '<span class="status-warning">Processing</span>',
#                   '<span class="status-success">Delivered</span>'],
#         'Actions': ['📦 Track', '📝 Review', '🔄 Reorder', '📞 Contact', '📦 Track']
#     })
    
#     # Apply filters
#     if status_filter != "All":
#         # Filter logic here
#         pass
    
#     # Display orders
#     st.markdown(orders.to_html(escape=False, index=False), unsafe_allow_html=True)
    
#     # Order statistics
#     st.divider()
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         total_orders = len(orders)
#         st.metric("Total Orders", total_orders)
#     with col2:
#         avg_order = 145.75  # Calculate from data
#         st.metric("Average Order", f"€{avg_order:.2f}")
#     with col3:
#         repeat_rate = "68%"
#         st.metric("Repeat Rate", repeat_rate)
    
#     # Export button
#     if st.button("📥 Export Order History", use_container_width=True):
#         st.success("Order history exported!")

# def show_my_invoices(customer_id, api_url):
#     """Display customer invoices"""
    
#     st.subheader("💳 My Invoices & Receipts")
    
#     # Invoice list
#     invoices = pd.DataFrame({
#         'Invoice #': ['INV-2024-123', 'INV-2024-122', 'INV-2024-121', 'INV-2024-120'],
#         'Date': ['2024-12-10', '2024-12-05', '2024-11-28', '2024-11-20'],
#         'Amount': ['€89.00', '€145.50', '€220.00', '€189.99'],
#         'Status': ['<span class="status-success">Paid</span>',
#                   '<span class="status-success">Paid</span>',
#                   '<span class="status-success">Paid</span>',
#                   '<span class="status-success">Paid</span>'],
#         'Download': ['📄 PDF', '📄 PDF', '📄 PDF', '📄 PDF']
#     })
    
#     st.markdown(invoices.to_html(escape=False, index=False), unsafe_allow_html=True)
    
#     # Payment methods
#     st.subheader("💳 Payment Methods")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("""
#         <div class="custom-card">
#             <h4>💳 Credit Card</h4>
#             <p>**** **** **** 1234</p>
#             <p>Expires: 12/2025</p>
#             <button style="background: #8B5CF6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
#                 Update
#             </button>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="custom-card">
#             <h4>📱 PayPal</h4>
#             <p>customer@email.com</p>
#             <p>Connected</p>
#             <button style="background: #8B5CF6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
#                 Manage
#             </button>
#         </div>
#         """, unsafe_allow_html=True)

# def show_my_favorites():
#     """Display customer's favorite/wishlist items"""
    
#     st.subheader("⭐ My Favorites & Wishlist")
    
#     # Sample favorite items
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center;">
#             <div style="font-size: 3rem;">💎</div>
#             <h4>Silver Necklace</h4>
#             <p>€89.00</p>
#             <button style="background: #10B981; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; width: 100%;">
#                 Add to Cart
#             </button>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center;">
#             <div style="font-size: 3rem;">✨</div>
#             <h4>Gold Earrings</h4>
#             <p>€145.50</p>
#             <button style="background: #10B981; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; width: 100%;">
#                 Add to Cart
#             </button>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center;">
#             <div style="font-size: 3rem;">🌟</div>
#             <h4>Pearl Bracelet</h4>
#             <p>€189.99</p>
#             <button style="background: #10B981; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; width: 100%;">
#                 Add to Cart
#             </button>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center;">
#             <div style="font-size: 3rem;">💍</div>
#             <h4>Custom Ring</h4>
#             <p>€220.00</p>
#             <button style="background: #10B981; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; width: 100%;">
#                 Add to Cart
#             </button>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Price alerts
#     st.subheader("🔔 Price Alerts")
    
#     alerts = pd.DataFrame({
#         'Item': ['Silver Necklace', 'Gold Earrings', 'Pearl Bracelet'],
#         'Current Price': ['€89.00', '€145.50', '€189.99'],
#         'Target Price': ['€75.00', '€120.00', '€160.00'],
#         'Status': ['<span class="status-warning">Waiting</span>',
#                   '<span class="status-success">Matched!</span>',
#                   '<span class="status-warning">Waiting</span>']
#     })
    
#     st.markdown(alerts.to_html(escape=False, index=False), unsafe_allow_html=True)