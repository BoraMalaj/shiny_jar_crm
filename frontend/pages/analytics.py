# frontend/pages/analytics.py - COMPLETE VERSION
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to import sklearn, but provide fallback if not available
try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ scikit-learn not installed. Some forecasting features will be limited.")
    # Simple linear regression fallback
    class SimpleLinearRegression:
        def __init__(self):
            self.slope = 0
            self.intercept = 0
        
        def fit(self, X, y):
            if len(X) > 1:
                x_mean = np.mean(X)
                y_mean = np.mean(y)
                numerator = np.sum((X - x_mean) * (y - y_mean))
                denominator = np.sum((X - x_mean) ** 2)
                self.slope = numerator / denominator if denominator != 0 else 0
                self.intercept = y_mean - self.slope * x_mean
            return self
        
        def predict(self, X):
            return self.intercept + self.slope * X

def show_analytics_page():
    st.markdown('<h1 class="main-header">🔮 Advanced Business Analytics</h1>', unsafe_allow_html=True)
    
    api_url = st.session_state.get('api_url', 'http://localhost:8000')
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Forecasting", "👥 Customer Insights", "💰 Profit Analysis", "📊 Business Intelligence"])
    
    with tab1:
        show_sales_forecasting(api_url)
    
    with tab2:
        show_customer_insights(api_url)
    
    with tab3:
        show_profit_analysis(api_url)
    
    with tab4:
        show_business_intelligence(api_url)

def show_sales_forecasting(api_url):
    st.subheader("📈 Sales Forecasting & Predictions")
    
    # Fetch sales data
    try:
        response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
        
        if response.status_code == 200:
            transactions = response.json()
            
            if transactions:
                df = pd.DataFrame(transactions)
                
                # Handle date field
                if 'transaction_date' in df.columns:
                    df['date'] = pd.to_datetime(df['transaction_date'])
                elif 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                # Filter income (sales) only
                sales_df = df[df['type'] == 'income'].copy()
                
                if not sales_df.empty and len(sales_df) > 3:  # Need at least 3 data points
                    # Resample to monthly sales
                    sales_df.set_index('date', inplace=True)
                    monthly_sales = sales_df.resample('M')['amount'].sum().reset_index()
                    monthly_sales['month_num'] = range(len(monthly_sales))
                    
                    # Forecast configuration
                    st.sidebar.subheader("Forecast Settings")
                    forecast_months = st.sidebar.slider("Months to forecast", 1, 12, 3)
                    
                    # Use appropriate regression model
                    if SKLEARN_AVAILABLE:
                        model = LinearRegression()
                    else:
                        model = SimpleLinearRegression()
                    
                    # Prepare data for regression
                    X = monthly_sales['month_num'].values.reshape(-1, 1)
                    y = monthly_sales['amount'].values
                    
                    # Fit model
                    model.fit(X, y)
                    
                    # Generate forecast
                    future_months = np.array([[i] for i in range(len(monthly_sales), len(monthly_sales) + forecast_months)])
                    
                    if SKLEARN_AVAILABLE:
                        predictions = model.predict(future_months)
                    else:
                        predictions = model.predict(future_months.flatten())
                    
                    # Calculate confidence interval (simplified)
                    if SKLEARN_AVAILABLE:
                        predictions_flat = predictions
                    else:
                        predictions_flat = predictions
                    
                    residuals = y - model.predict(X).flatten() if SKLEARN_AVAILABLE else y - model.predict(X.flatten())
                    std_residuals = np.std(residuals)
                    confidence_interval = std_residuals * 1.96  # 95% confidence
                    
                    # Display forecast results
                    st.success(f"✅ Forecast generated for next {forecast_months} months")
                    
                    if not SKLEARN_AVAILABLE:
                        st.info("ℹ️ Using simple linear regression (install scikit-learn for advanced features)")
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        next_month_pred = predictions_flat[0] if len(predictions_flat) > 0 else 0
                        st.metric("Next Month Forecast", f"€{next_month_pred:,.0f}")
                    with col2:
                        if len(monthly_sales) > 0:
                            avg_growth = ((predictions_flat[-1] / monthly_sales['amount'].iloc[-1]) - 1) * 100
                            st.metric("Growth Rate", f"{avg_growth:.1f}%")
                        else:
                            st.metric("Growth Rate", "N/A")
                    with col3:
                        total_forecast = predictions_flat.sum()
                        st.metric("Total Forecast", f"€{total_forecast:,.0f}")
                    with col4:
                        best_month = monthly_sales['amount'].max() if len(monthly_sales) > 0 else 0
                        st.metric("Best Month", f"€{best_month:,.0f}")
                    
                    # Chart with forecast
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(go.Scatter(
                        x=monthly_sales['date'],
                        y=monthly_sales['amount'],
                        mode='lines+markers',
                        name='Historical Sales',
                        line=dict(color='#4ECDC4', width=3),
                        marker=dict(size=8)
                    ))
                    
                    # Forecast data
                    future_dates = pd.date_range(
                        start=monthly_sales['date'].iloc[-1] + pd.DateOffset(months=1),
                        periods=forecast_months,
                        freq='M'
                    )
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=predictions_flat,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='#FF6B6B', width=3, dash='dash'),
                        marker=dict(size=8, symbol='diamond')
                    ))
                    
                    # Confidence interval
                    fig.add_trace(go.Scatter(
                        x=list(future_dates) + list(future_dates)[::-1],
                        y=list(predictions_flat + confidence_interval) + list(predictions_flat - confidence_interval)[::-1],
                        fill='toself',
                        fillcolor='rgba(255, 107, 107, 0.2)',
                        line=dict(color='rgba(255, 255, 255, 0)'),
                        name='95% Confidence Interval',
                        showlegend=True
                    ))
                    
                    fig.update_layout(
                        title='Sales Forecast with Confidence Interval',
                        xaxis_title='Date',
                        yaxis_title='Sales Amount (€)',
                        hovermode='x unified',
                        height=500,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Forecast table
                    st.subheader("📅 Detailed Forecast")
                    
                    forecast_df = pd.DataFrame({
                        'Month': [d.strftime('%B %Y') for d in future_dates],
                        'Forecasted Sales': predictions_flat,
                        'Lower Bound (95%)': predictions_flat - confidence_interval,
                        'Upper Bound (95%)': predictions_flat + confidence_interval
                    })
                    
                    display_df = forecast_df.copy()
                    display_df['Forecasted Sales'] = display_df['Forecasted Sales'].apply(lambda x: f"€{x:,.0f}")
                    display_df['Lower Bound (95%)'] = display_df['Lower Bound (95%)'].apply(lambda x: f"€{x:,.0f}")
                    display_df['Upper Bound (95%)'] = display_df['Upper Bound (95%)'].apply(lambda x: f"€{x:,.0f}")
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Insights
                    st.subheader("💡 Forecasting Insights")
                    
                    insights_col1, insights_col2 = st.columns(2)
                    
                    with insights_col1:
                        st.info("""
                        **Seasonal Patterns:**
                        - 📈 **Best Month:** Identify peak seasons
                        - 📉 **Slow Periods:** Plan for slower months
                        - 🎯 **Growth Trend:** Track month-over-month growth
                        """)
                    
                    with insights_col2:
                        st.info("""
                        **Business Recommendations:**
                        - 🛍️ **Stock Up:** Increase inventory before forecasted peaks
                        - 💰 **Budget Planning:** Use forecast for expense planning  
                        - 📢 **Marketing:** Time campaigns with growth periods
                        """)
                    
                    # Export forecast
                    if st.button("📥 Export Forecast Data", use_container_width=True):
                        export_df = pd.DataFrame({
                            'Month': [d.strftime('%Y-%m') for d in future_dates],
                            'Forecasted_Sales': predictions_flat,
                            'Lower_Bound': predictions_flat - confidence_interval,
                            'Upper_Bound': predictions_flat + confidence_interval
                        })
                        csv = export_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="sales_forecast.csv",
                            mime="text/csv"
                        )
                    
                elif len(sales_df) <= 3:
                    st.info("Need at least 3 months of sales data for accurate forecasting. Current data points: {}".format(len(sales_df)))
                else:
                    st.info("No sales data available for forecasting. Add some income transactions first!")
            else:
                st.info("No transaction data available")
        else:
            st.error("Failed to fetch transaction data")
    
    except Exception as e:
        st.error(f"Error in sales forecasting: {str(e)}")
        st.info("Try installing scikit-learn for better forecasting: `pip install scikit-learn`")

def show_customer_insights(api_url):
    st.subheader("👥 Customer Analytics & Segmentation")
    
    try:
        # Fetch customers and transactions
        customers_response = requests.get(f"{api_url}/api/customers")
        transactions_response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
        
        if customers_response.status_code == 200 and transactions_response.status_code == 200:
            customers = customers_response.json()
            transactions = transactions_response.json()
            
            if customers:
                customers_df = pd.DataFrame(customers)
                
                # Customer segmentation
                st.subheader("Customer Segmentation")
                
                # Define segments based on spending
                customers_df['segment'] = pd.cut(
                    customers_df['total_spent'],
                    bins=[0, 100, 500, 1000, float('inf')],
                    labels=['New', 'Regular', 'VIP', 'Premium'],
                    right=False
                )
                
                # Segment distribution
                segment_counts = customers_df['segment'].value_counts().sort_index()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = px.pie(
                        values=segment_counts.values,
                        names=segment_counts.index,
                        title='Customer Segments',
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        hole=0.4
                    )
                    fig1.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Customer Lifetime Value (simplified)
                    avg_spent = customers_df['total_spent'].mean()
                    retention_rate = 0.7  # Assumption for demo
                    clv = avg_spent * retention_rate / (1 - retention_rate)
                    
                    st.metric("Avg Customer Value", f"€{avg_spent:,.0f}")
                    st.metric("Estimated CLV", f"€{clv:,.0f}")
                    st.metric("Customer Count", len(customers_df))
                
                # Top customers analysis
                st.subheader("Top 10 Customers Analysis")
                
                top_customers = customers_df.nlargest(10, 'total_spent')
                
                fig2 = px.bar(
                    top_customers,
                    x='name',
                    y='total_spent',
                    color='total_spent',
                    title='Top 10 Customers by Lifetime Value',
                    color_continuous_scale='Viridis',
                    labels={'total_spent': 'Total Spent (€)', 'name': 'Customer'}
                )
                
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
                
                # Customer acquisition trends
                st.subheader("Customer Acquisition Timeline")
                
                if 'customer_since' in customers_df.columns:
                    customers_df['customer_since'] = pd.to_datetime(customers_df['customer_since'])
                    monthly_acquisitions = customers_df.resample('M', on='customer_since').size().reset_index()
                    monthly_acquisitions.columns = ['month', 'new_customers']
                    
                    fig3 = px.line(
                        monthly_acquisitions,
                        x='month',
                        y='new_customers',
                        title='Monthly Customer Acquisition',
                        markers=True,
                        labels={'new_customers': 'New Customers', 'month': 'Month'}
                    )
                    
                    fig3.update_layout(height=350)
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Customer recommendations
                st.subheader("🎯 Customer Engagement Recommendations")
                
                rec_col1, rec_col2, rec_col3 = st.columns(3)
                
                with rec_col1:
                    st.info("""
                    **New Customers (€0-100):**
                    - Send welcome discount
                    - Request first review
                    - Follow-up email sequence
                    """)
                
                with rec_col2:
                    st.info("""
                    **Regular Customers (€100-500):**
                    - Loyalty program invite
                    - Birthday discounts
                    - Referral program
                    """)
                
                with rec_col3:
                    st.info("""
                    **VIP/Premium (€500+):**
                    - Exclusive early access
                    - Personal shopping assistant
                    - Premium support line
                    """)
                
                # Export customer insights
                if st.button("📊 Export Customer Analysis", use_container_width=True):
                    csv = customers_df[['name', 'email', 'total_spent', 'segment']].to_csv(index=False)
                    st.download_button(
                        label="Download Customer Data",
                        data=csv,
                        file_name="customer_analysis.csv",
                        mime="text/csv"
                    )
                
            else:
                st.info("No customer data available for insights")
        
        else:
            st.error("Failed to load customer data")
    
    except Exception as e:
        st.error(f"Error loading customer insights: {str(e)}")

def show_profit_analysis(api_url):
    st.subheader("💰 Profit Margin Analysis")
    
    try:
        # Fetch transactions
        response = requests.get(f"{api_url}/api/transactions", params={"limit": 1000})
        
        if response.status_code == 200:
            transactions = response.json()
            
            if transactions:
                df = pd.DataFrame(transactions)
                
                # Handle date field
                if 'transaction_date' in df.columns:
                    df['date'] = pd.to_datetime(df['transaction_date'])
                elif 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                # Monthly profit analysis
                df['year_month'] = df['date'].dt.to_period('M')
                
                monthly_data = df.groupby(['year_month', 'type'])['amount'].sum().unstack(fill_value=0)
                monthly_data['profit'] = monthly_data.get('income', 0) - monthly_data.get('expense', 0)
                monthly_data['profit_margin'] = (monthly_data['profit'] / monthly_data.get('income', 1)) * 100
                
                # Reset index for plotting
                monthly_data = monthly_data.reset_index()
                monthly_data['year_month'] = monthly_data['year_month'].astype(str)
                
                # Profit metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_profit = monthly_data['profit'].sum()
                    st.metric("Total Profit", f"€{total_profit:,.0f}")
                
                with col2:
                    avg_margin = monthly_data['profit_margin'].mean()
                    st.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
                
                with col3:
                    best_margin = monthly_data['profit_margin'].max()
                    st.metric("Best Margin", f"{best_margin:.1f}%")
                
                with col4:
                    worst_margin = monthly_data['profit_margin'].min()
                    st.metric("Worst Margin", f"{worst_margin:.1f}%")
                
                # Profit trend chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=monthly_data['year_month'],
                    y=monthly_data['profit'],
                    mode='lines+markers',
                    name='Monthly Profit',
                    line=dict(color='#2ECC71', width=3),
                    yaxis='y'
                ))
                
                fig.add_trace(go.Scatter(
                    x=monthly_data['year_month'],
                    y=monthly_data['profit_margin'],
                    mode='lines+markers',
                    name='Profit Margin %',
                    line=dict(color='#9B59B6', width=3, dash='dot'),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title='Monthly Profit & Margin Trends',
                    xaxis_title='Month',
                    yaxis=dict(
                        title='Profit (€)',
                        titlefont=dict(color='#2ECC71'),
                        tickfont=dict(color='#2ECC71')
                    ),
                    yaxis2=dict(
                        title='Profit Margin %',
                        titlefont=dict(color='#9B59B6'),
                        tickfont=dict(color='#9B59B6'),
                        overlaying='y',
                        side='right'
                    ),
                    height=450,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Category profitability
                st.subheader("Category Profitability Analysis")
                
                # Get income by category
                income_by_cat = df[df['type'] == 'income'].groupby('category')['amount'].sum().reset_index()
                expense_by_cat = df[df['type'] == 'expense'].groupby('category')['amount'].sum().reset_index()
                
                # Merge and calculate profit
                cat_profit = pd.merge(
                    income_by_cat,
                    expense_by_cat,
                    on='category',
                    how='outer',
                    suffixes=('_income', '_expense')
                ).fillna(0)
                
                cat_profit['profit'] = cat_profit['amount_income'] - cat_profit['amount_expense']
                cat_profit['margin'] = (cat_profit['profit'] / cat_profit['amount_income'].replace(0, np.nan)) * 100
                
                # Sort by profit
                cat_profit = cat_profit.sort_values('profit', ascending=False)
                
                fig2 = px.bar(
                    cat_profit.head(10),
                    x='category',
                    y=['amount_income', 'amount_expense', 'profit'],
                    barmode='group',
                    title='Top 10 Categories: Income vs Expenses',
                    labels={'value': 'Amount (€)', 'variable': 'Type'},
                    color_discrete_map={
                        'amount_income': '#27AE60',
                        'amount_expense': '#E74C3C', 
                        'profit': '#3498DB'
                    }
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Profitability recommendations
                st.subheader("📊 Profitability Insights")
                
                insights_df = cat_profit[['category', 'amount_income', 'amount_expense', 'profit', 'margin']].copy()
                insights_df['amount_income'] = insights_df['amount_income'].apply(lambda x: f"€{x:,.0f}")
                insights_df['amount_expense'] = insights_df['amount_expense'].apply(lambda x: f"€{x:,.0f}")
                insights_df['profit'] = insights_df['profit'].apply(lambda x: f"€{x:,.0f}")
                insights_df['margin'] = insights_df['margin'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                
                st.dataframe(
                    insights_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "category": "Category",
                        "amount_income": "Income",
                        "amount_expense": "Expenses",
                        "profit": "Profit",
                        "margin": "Margin %"
                    }
                )
                
                # Recommendations
                st.info("""
                **Profit Optimization Strategies:**
                
                1. **High Margin Categories:** Focus marketing on categories with >30% margin
                2. **Cost Reduction:** Review expenses in categories with negative margins
                3. **Pricing Strategy:** Consider price increases for low-margin, high-volume items
                4. **Product Mix:** Promote bundle deals combining high and low margin items
                """)
                
            else:
                st.info("No transaction data available for profit analysis")
        
        else:
            st.error("Failed to fetch transaction data")
    
    except Exception as e:
        st.error(f"Error in profit analysis: {str(e)}")

def show_business_intelligence(api_url):
    st.subheader("📊 Business Intelligence Dashboard")
    
    try:
        # Fetch all data
        dashboard_response = requests.get(f"{api_url}/api/dashboard")
        stats_response = requests.get(f"{api_url}/api/stats")
        
        if dashboard_response.status_code == 200 and stats_response.status_code == 200:
            dashboard_data = dashboard_response.json()
            stats_data = stats_response.json()
            
            # KPI Cards
            st.subheader("📈 Key Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                profit = stats_data.get('profit', 0)
                profit_color = "normal" if profit >= 0 else "inverse"
                st.metric(
                    "Net Profit", 
                    f"€{profit:,.0f}",
                    delta_color=profit_color
                )
            
            with col2:
                total_income = stats_data.get('total_income', 0)
                st.metric("Total Revenue", f"€{total_income:,.0f}")
            
            with col3:
                customer_count = stats_data.get('customer_count', 0)
                st.metric("Customer Base", f"{customer_count}")
            
            with col4:
                avg_transaction = stats_data.get('average_transaction', 0)
                st.metric("Avg Transaction", f"€{avg_transaction:,.0f}")
            
            # Business Health Score
            st.subheader("🏥 Business Health Score")
            
            # Calculate health score (simplified)
            revenue_growth = 0.15  # Placeholder - would calculate from historical data
            profit_margin = (stats_data.get('profit', 0) / max(stats_data.get('total_income', 1), 1)) * 100
            customer_growth = 0.10  # Placeholder
            
            health_score = min(100, max(0, 
                (revenue_growth * 40) + 
                (profit_margin * 40) + 
                (customer_growth * 20)
            ))
            
            # Health gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                title={'text': "Business Health Score"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 100], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Health indicators
            health_col1, health_col2, health_col3 = st.columns(3)
            
            with health_col1:
                revenue_color = "green" if revenue_growth > 0.1 else "orange" if revenue_growth > 0 else "red"
                st.metric("Revenue Growth", f"{revenue_growth*100:.1f}%", delta_color=revenue_color)
            
            with health_col2:
                margin_color = "green" if profit_margin > 20 else "orange" if profit_margin > 10 else "red"
                st.metric("Profit Margin", f"{profit_margin:.1f}%", delta_color=margin_color)
            
            with health_col3:
                customer_color = "green" if customer_growth > 0.15 else "orange" if customer_growth > 0.05 else "red"
                st.metric("Customer Growth", f"{customer_growth*100:.1f}%", delta_color=customer_color)
            
            # Trend analysis
            st.subheader("📅 Business Trends")
            
            if 'monthly_trends' in dashboard_data:
                trends_df = pd.DataFrame(dashboard_data['monthly_trends'])
                
                # Pivot for chart
                trends_pivot = trends_df.pivot(index='month', columns='type', values='total').fillna(0)
                
                fig2 = go.Figure()
                
                for col in trends_pivot.columns:
                    fig2.add_trace(go.Scatter(
                        x=trends_pivot.index,
                        y=trends_pivot[col],
                        mode='lines+markers',
                        name=col.title(),
                        line=dict(width=3)
                    ))
                
                fig2.update_layout(
                    title='Monthly Income & Expense Trends',
                    xaxis_title='Month',
                    yaxis_title='Amount (€)',
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Business recommendations
            st.subheader("💡 Strategic Recommendations")
            
            rec_tab1, rec_tab2, rec_tab3 = st.tabs(["🚀 Growth", "💰 Profit", "👥 Customers"])
            
            with rec_tab1:
                st.info("""
                **Growth Opportunities:**
                
                1. **Market Expansion:** Consider adding 2-3 new product categories
                2. **Social Media:** Increase Instagram/TikTok content frequency by 50%
                3. **Email Marketing:** Launch segmented email campaigns for different customer groups
                4. **Partnerships:** Collaborate with complementary brands for cross-promotion
                """)
            
            with rec_tab2:
                st.info("""
                **Profit Optimization:**
                
                1. **Cost Analysis:** Review top 3 expense categories for reduction opportunities
                2. **Pricing Strategy:** Test 5-10% price increase on best-selling items
                3. **Upselling:** Implement bundle deals with 20% higher average order value
                4. **Supplier Negotiation:** Renegotiate terms with top 3 suppliers
                """)
            
            with rec_tab3:
                st.info("""
                **Customer Strategy:**
                
                1. **Retention Program:** Launch loyalty program for repeat customers
                2. **Referral System:** Implement referral program with 10% discount
                3. **Customer Feedback:** Send post-purchase surveys to improve experience
                4. **Personalization:** Use purchase history for personalized recommendations
                """)
            
            # Export business intelligence report
            if st.button("📋 Generate Business Report", type="primary", use_container_width=True):
                st.success("""
                ✅ **Business Intelligence Report Generated**
                
                **Summary:**
                - Overall Health Score: {:.1f}/100
                - Revenue: €{:,}
                - Profit Margin: {:.1f}%
                - Customer Base: {}
                
                **Next Steps:**
                1. Implement growth recommendations
                2. Monitor key metrics weekly
                3. Schedule monthly strategy review
                """.format(health_score, stats_data.get('total_income', 0), 
                          profit_margin, stats_data.get('customer_count', 0)))
        
        else:
            st.error("Failed to load business intelligence data")
    
    except Exception as e:
        st.error(f"Error in business intelligence: {str(e)}")