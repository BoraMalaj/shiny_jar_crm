# frontend/pages/budget.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, date, timedelta
import calendar
import time

def show_budget_page():
    st.markdown('<h1 class="main-header">💰 Budget Management</h1>', unsafe_allow_html=True)
    
    # API URL from session state
    api_url = st.session_state.get('api_url', 'http://localhost:8000')
    
    # Tabs for different budget views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Overview", "➕ Create Budget", "📈 Budget Analysis", "🚨 Alerts"])
    
    with tab1:
        show_budget_overview(api_url)
    
    with tab2:
        show_create_budget(api_url)
    
    with tab3:
        show_budget_analysis(api_url)
    
    with tab4:
        show_budget_alerts(api_url)

def show_budget_overview(api_url):
    """Display current budgets with status indicators"""
    st.subheader("Current Budgets")
    
    try:
        # Fetch budgets
        budgets_response = requests.get(f"{api_url}/api/budgets")
        analysis_response = requests.get(f"{api_url}/api/budgets/analysis")
        
        if budgets_response.status_code == 200 and analysis_response.status_code == 200:
            budgets = budgets_response.json()
            analysis = analysis_response.json()
            
            if budgets:
                # Create DataFrame with analysis data
                budget_dict = {b['id']: b for b in budgets}
                analysis_dict = {a['budget_id']: a for a in analysis}
                
                # Combine data
                combined_data = []
                for budget in budgets:
                    analysis_info = analysis_dict.get(budget['id'], {})
                    combined_data.append({
                        **budget,
                        **analysis_info
                    })
                
                df = pd.DataFrame(combined_data)
                
                # Display metrics row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_budget = df['amount'].sum()
                    st.metric("Total Budget", f"€{total_budget:,.2f}")
                
                with col2:
                    total_spent = df['actual_spent'].sum() if 'actual_spent' in df.columns else 0
                    st.metric("Total Spent", f"€{total_spent:,.2f}")
                
                with col3:
                    remaining = total_budget - total_spent
                    st.metric("Remaining", f"€{remaining:,.2f}")
                
                with col4:
                    if 'percentage_used' in df.columns:
                        avg_utilization = df['percentage_used'].mean() if len(df) > 0 else 0
                        st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
                    else:
                        st.metric("Avg Utilization", "0%")
                
                # Budget cards
                st.subheader("Budget Details")
                for _, row in df.iterrows():
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            # Budget name and category
                            category_name = row.get('category', f"Category {row.get('category_id', 'N/A')}")
                            st.markdown(f"**{row['name']}** - {category_name}")
                            st.caption(f"Period: {row['period']} | €{row['amount']:,.2f}")
                            
                            # Progress bar if we have percentage_used
                            if 'percentage_used' in row:
                                progress = min(row['percentage_used'] / 100, 1)
                                color = "green" if progress < 0.7 else "orange" if progress < 0.9 else "red"
                                st.progress(float(progress), text=f"{row['percentage_used']:.1f}% used")
                        
                        with col2:
                            # Status indicator
                            status = row.get('status', 'unknown')
                            if status == 'over':
                                st.error("OVER BUDGET")
                            elif status == 'on_track':
                                st.success("ON TRACK")
                            else:
                                st.info("UNDER BUDGET")
                        
                        with col3:
                            # Quick actions
                            if st.button("📊", key=f"view_{row['id']}"):
                                st.session_state.selected_budget = row['id']
                            if st.button("✏️", key=f"edit_{row['id']}"):
                                st.session_state.edit_budget = row['id']
                
                # Budget summary chart
                st.subheader("Budget Status Overview")
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Budget',
                    x=df['name'],
                    y=df['amount'],
                    marker_color='lightblue'
                ))
                
                if 'actual_spent' in df.columns:
                    fig.add_trace(go.Bar(
                        name='Actual Spent',
                        x=df['name'],
                        y=df['actual_spent'],
                        marker_color='coral'
                    ))
                
                fig.update_layout(
                    barmode='group',
                    title='Budget vs Actual Spending',
                    xaxis_title='Budget',
                    yaxis_title='Amount (€)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.info("No budgets created yet. Create your first budget!")
        
        else:
            st.error("Could not load budget data")
    
    except Exception as e:
        st.error(f"Error loading budgets: {str(e)}")

def show_create_budget(api_url):
    """Form to create new budgets"""
    st.subheader("Create New Budget")
    
    with st.form("create_budget_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Budget Name *", placeholder="Monthly Materials Budget")
            amount = st.number_input("Budget Amount (€) *", min_value=0.01, step=10.0, value=100.0)
            
            # Get categories for selection
            try:
                categories_response = requests.get(f"{api_url}/api/categories")
                if categories_response.status_code == 200:
                    categories_data = categories_response.json()
                    # Combine expense categories
                    expense_categories = categories_data.get('expense_categories', [])
                    income_categories = categories_data.get('income_categories', [])
                    all_categories = expense_categories + income_categories
                    
                    category = st.selectbox("Category (Optional)", [""] + all_categories)
                else:
                    category = st.text_input("Category (Optional)")
            except:
                category = st.text_input("Category (Optional)")
        
        with col2:
            period = st.selectbox(
                "Budget Period *",
                ["monthly", "weekly", "quarterly", "yearly"],
                format_func=lambda x: x.title()
            )
            
            start_date = st.date_input("Start Date *", value=date.today())
            
            # Calculate end date based on period
            if period == "weekly":
                end_date = start_date + timedelta(days=6)
            elif period == "monthly":
                # Last day of month
                last_day = calendar.monthrange(start_date.year, start_date.month)[1]
                end_date = date(start_date.year, start_date.month, last_day)
            elif period == "quarterly":
                # End of quarter
                quarter_month = ((start_date.month - 1) // 3 + 1) * 3
                last_day = calendar.monthrange(start_date.year, quarter_month)[1]
                end_date = date(start_date.year, quarter_month, last_day)
            else:  # yearly
                end_date = date(start_date.year, 12, 31)
            
            st.info(f"End Date: {end_date.strftime('%Y-%m-%d')}")
            end_date_input = st.date_input("Or Custom End Date", value=end_date)
        
        description = st.text_area("Description", placeholder="What is this budget for?")
        
        submitted = st.form_submit_button("Create Budget", type="primary", use_container_width=True)
        
        if submitted:
            if not name or amount <= 0:
                st.error("Please fill in all required fields (*)")
            else:
                budget_data = {
                    "name": name,
                    "amount": float(amount),
                    "period": period,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date_input.isoformat(),
                    "category": category if category else None
                }
                
                try:
                    response = requests.post(f"{api_url}/api/budgets", json=budget_data)
                    
                    if response.status_code == 200:
                        st.success("✅ Budget created successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Failed to create budget: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")

def show_budget_analysis(api_url):
    """Advanced budget analysis with charts"""
    st.subheader("Budget Analysis")
    
    try:
        response = requests.get(f"{api_url}/api/budgets/analysis")
        
        if response.status_code == 200:
            analysis_data = response.json()
            
            if analysis_data:
                df = pd.DataFrame(analysis_data)
                
                # Utilization chart
                col1, col2 = st.columns(2)
                
                with col1:
                    # Donut chart of budget status
                    if 'status' in df.columns:
                        status_counts = df['status'].value_counts()
                        fig1 = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            title='Budget Status Distribution',
                            hole=0.4,
                            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFD166']
                        )
                        fig1.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        st.info("No status data available")
                
                with col2:
                    # Utilization by budget
                    if 'percentage_used' in df.columns:
                        fig2 = px.bar(
                            df,
                            x='budget_name',
                            y='percentage_used',
                            title='Utilization by Budget (%)',
                            color='percentage_used',
                            color_continuous_scale='RdYlGn_r',
                            labels={'percentage_used': 'Utilization %', 'budget_name': 'Budget'}
                        )
                        fig2.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="100% Limit")
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("No utilization data available")
                
                # Monthly budget tracking
                st.subheader("Monthly Budget Tracking")
                
                # Get transactions for trend analysis
                try:
                    transactions_response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
                    if transactions_response.status_code == 200:
                        transactions = transactions_response.json()
                        
                        if transactions:
                            transactions_df = pd.DataFrame(transactions)
                            
                            # Handle date field
                            if 'transaction_date' in transactions_df.columns:
                                transactions_df['date'] = pd.to_datetime(transactions_df['transaction_date'])
                            elif 'date' in transactions_df.columns:
                                transactions_df['date'] = pd.to_datetime(transactions_df['date'])
                            
                            if 'date' in transactions_df.columns:
                                transactions_df['month'] = transactions_df['date'].dt.to_period('M')
                                
                                # Group by month and type
                                monthly_expenses = transactions_df[
                                    transactions_df['type'] == 'expense'
                                ].groupby('month')['amount'].sum().reset_index()
                                
                                if not monthly_expenses.empty:
                                    monthly_expenses['month'] = monthly_expenses['month'].astype(str)
                                    
                                    # Get budgets for comparison
                                    budgets_df = pd.DataFrame(analysis_data)
                                    total_monthly_budget = budgets_df[
                                        budgets_df['period'] == 'monthly'
                                    ]['budget_amount'].sum()
                                    
                                    # Create comparison chart
                                    fig3 = go.Figure()
                                    
                                    fig3.add_trace(go.Scatter(
                                        x=monthly_expenses['month'],
                                        y=monthly_expenses['amount'],
                                        mode='lines+markers',
                                        name='Actual Expenses',
                                        line=dict(color='red', width=3)
                                    ))
                                    
                                    fig3.add_trace(go.Scatter(
                                        x=monthly_expenses['month'],
                                        y=[total_monthly_budget] * len(monthly_expenses),
                                        mode='lines',
                                        name='Budget Limit',
                                        line=dict(color='green', dash='dash', width=2)
                                    ))
                                    
                                    fig3.update_layout(
                                        title='Monthly Expenses vs Budget',
                                        xaxis_title='Month',
                                        yaxis_title='Amount (€)',
                                        height=400
                                    )
                                    
                                    st.plotly_chart(fig3, use_container_width=True)
                except Exception as e:
                    st.info(f"Could not load transaction data for trend analysis: {str(e)}")
                
                # Budget variance table
                if 'budget_amount' in df.columns and 'actual_spent' in df.columns:
                    st.subheader("Budget Variance Analysis")
                    
                    df['variance'] = df['budget_amount'] - df['actual_spent']
                    df['variance_percentage'] = (df['variance'] / df['budget_amount'] * 100)
                    
                    display_df = df[[
                        'budget_name', 'budget_amount', 'actual_spent', 
                        'variance', 'variance_percentage', 'status'
                    ]].copy()
                    
                    display_df['budget_amount'] = display_df['budget_amount'].apply(lambda x: f"€{x:,.2f}")
                    display_df['actual_spent'] = display_df['actual_spent'].apply(lambda x: f"€{x:,.2f}")
                    display_df['variance'] = display_df['variance'].apply(lambda x: f"€{x:,.2f}")
                    display_df['variance_percentage'] = display_df['variance_percentage'].apply(lambda x: f"{x:.1f}%")
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "budget_name": "Budget",
                            "budget_amount": "Budget Amount",
                            "actual_spent": "Actual Spent",
                            "variance": "Variance",
                            "variance_percentage": "Variance %",
                            "status": "Status"
                        }
                    )
                    
                    # Export button
                    if st.button("📥 Export Budget Report", use_container_width=True):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV Report",
                            data=csv,
                            file_name="budget_analysis_report.csv",
                            mime="text/csv"
                        )
            
            else:
                st.info("No budget data available for analysis")
        
        else:
            st.error("Could not load budget analysis data")
    
    except Exception as e:
        st.error(f"Error loading analysis: {str(e)}")

def show_budget_alerts(api_url):
    """Display budget alerts and notifications"""
    st.subheader("Budget Alerts & Notifications")
    
    try:
        response = requests.get(f"{api_url}/api/budgets/analysis")
        
        if response.status_code == 200:
            analysis_data = response.json()
            
            if analysis_data:
                df = pd.DataFrame(analysis_data)
                
                # Over budget alerts
                over_budget = df[df['status'] == 'over']
                if not over_budget.empty:
                    st.error("🚨 OVER BUDGET ALERTS")
                    for _, row in over_budget.iterrows():
                        with st.container():
                            st.markdown(f"**{row['budget_name']}**")
                            st.markdown(f"Budget: €{row['budget_amount']:,.2f} | Spent: €{row['actual_spent']:,.2f}")
                            st.markdown(f"Overspent by: €{row['actual_spent'] - row['budget_amount']:,.2f}")
                            st.markdown("---")
                
                # Approaching limit alerts
                if 'percentage_used' in df.columns:
                    approaching = df[(df['percentage_used'] >= 80) & (df['percentage_used'] < 100) & (df['status'] != 'over')]
                    if not approaching.empty:
                        st.warning("⚠️ APPROACHING BUDGET LIMIT")
                        for _, row in approaching.iterrows():
                            with st.container():
                                st.markdown(f"**{row['budget_name']}**")
                                st.markdown(f"Utilization: {row['percentage_used']:.1f}%")
                                remaining = row['budget_amount'] - row['actual_spent']
                                st.markdown(f"Remaining: €{remaining:,.2f}")
                                st.markdown("---")
                
                # On track budgets
                on_track = df[df['status'] == 'on_track']
                if not on_track.empty:
                    st.success("✅ ON TRACK BUDGETS")
                    for _, row in on_track.iterrows():
                        with st.container():
                            st.markdown(f"**{row['budget_name']}**")
                            if 'percentage_used' in row:
                                st.markdown(f"Utilization: {row['percentage_used']:.1f}%")
                            st.markdown("---")
                
                # Budget recommendations
                st.subheader("💡 Budget Recommendations")
                
                # Find highest spending categories
                try:
                    transactions_response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
                    if transactions_response.status_code == 200:
                        transactions = transactions_response.json()
                        
                        if transactions:
                            transactions_df = pd.DataFrame(transactions)
                            expenses_df = transactions_df[transactions_df['type'] == 'expense']
                            
                            if not expenses_df.empty:
                                category_spending = expenses_df.groupby('category')['amount'].sum().reset_index()
                                top_categories = category_spending.nlargest(3, 'amount')
                                
                                for _, row in top_categories.iterrows():
                                    st.info(f"**{row['category']}**: €{row['amount']:,.2f} - Consider setting a specific budget for this category")
                except Exception as e:
                    st.info(f"Could not generate recommendations: {str(e)}")
                
                # Summary statistics
                st.subheader("📊 Alert Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Over Budget", len(over_budget))
                with col2:
                    st.metric("Approaching Limit", len(approaching) if 'approaching' in locals() else 0)
                with col3:
                    st.metric("On Track", len(on_track))
            
            else:
                st.info("No budgets created yet. No alerts to display.")
        
        else:
            st.error("Could not load budget data for alerts")
    
    except Exception as e:
        st.error(f"Error loading alerts: {str(e)}")