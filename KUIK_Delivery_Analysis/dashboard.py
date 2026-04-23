import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REQUIRED_FILES = [
    DATA_DIR / "orders.csv",
    DATA_DIR / "deliveries.csv",
    DATA_DIR / "hubs.csv",
    DATA_DIR / "riders.csv",
]

# Set page configuration
st.set_page_config(
    page_title="Delivery Analysis Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        missing_files = [path.name for path in REQUIRED_FILES if not path.exists()]
        if missing_files:
            from delivery_analysis import create_sample_data
            create_sample_data()

        orders = pd.read_csv(DATA_DIR / 'orders.csv')
        deliveries = pd.read_csv(DATA_DIR / 'deliveries.csv')
        hubs = pd.read_csv(DATA_DIR / 'hubs.csv')
        riders = pd.read_csv(DATA_DIR / 'riders.csv')
        
        # Convert datetime columns
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        deliveries['pickup_time'] = pd.to_datetime(deliveries['pickup_time'])
        deliveries['sla_deadline'] = pd.to_datetime(deliveries['sla_deadline'])
        deliveries['actual_delivery_time'] = pd.to_datetime(deliveries['actual_delivery_time'])
        
        # Add SLA breach analysis
        deliveries['is_breach'] = deliveries['actual_delivery_time'] > deliveries['sla_deadline']
        deliveries['delay_minutes'] = (deliveries['actual_delivery_time'] - deliveries['sla_deadline']).dt.total_seconds() / 60
        
        return orders, deliveries, hubs, riders
    except FileNotFoundError as e:
        st.error(f"Data files could not be created or loaded. Error: {e}")
        return None, None, None, None

def create_metric_card(title, value, format_type="number"):
    if format_type == "percentage":
        display_value = f"{value:.1f}%"
    elif format_type == "currency":
        display_value = f"${value:,.0f}"
    elif format_type == "time":
        display_value = f"{value:.1f} min"
    else:
        display_value = f"{value:,.0f}"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{display_value}</div>
        <div class="metric-label">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def normalize_date_range(date_selection):
    if isinstance(date_selection, tuple):
        if len(date_selection) == 0:
            return None, None
        if len(date_selection) == 1:
            return date_selection[0], date_selection[0]
        return date_selection[0], date_selection[1]
    return date_selection, date_selection

def create_empty_figure(title):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        height=400,
        annotations=[
            dict(
                text="No data available for the selected filters",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font={"size": 16},
            )
        ],
    )
    return fig

def main():
    st.markdown('<h1 class="main-header">🚚 Delivery Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    orders, deliveries, hubs, riders = load_data()
    
    if orders is None:
        return
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [orders['order_date'].min().date(), orders['order_date'].max().date()],
        min_value=orders['order_date'].min().date(),
        max_value=orders['order_date'].max().date()
    )
    start_date, end_date = normalize_date_range(date_range)
    
    # Hub filter
    selected_hubs = st.sidebar.multiselect(
        "Select Hubs",
        options=hubs['display_name'].tolist(),
        default=[]
    )
    
    # Filter data based on selections
    date_filtered_orders = orders[
        (orders['order_date'].dt.date >= start_date) & 
        (orders['order_date'].dt.date <= end_date)
    ]
    
    hub_ids = hubs[hubs['display_name'].isin(selected_hubs)]['hub_id'].tolist()
    filtered_deliveries = deliveries[
        (deliveries['hub_id'].isin(hub_ids)) &
        (deliveries['pickup_time'].dt.date >= start_date) &
        (deliveries['pickup_time'].dt.date <= end_date)
    ]
    filtered_order_ids = filtered_deliveries['order_id'].unique()
    filtered_orders = date_filtered_orders[
        date_filtered_orders['order_id'].isin(filtered_order_ids)
    ]
    all_hubs_selected = len(selected_hubs) == len(hubs)
    kpi_orders = date_filtered_orders if all_hubs_selected else filtered_orders
    
    # Key Metrics Row
    st.header("📈 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_orders = len(kpi_orders)
        create_metric_card("Total Orders", total_orders)
    
    with col2:
        delivered_orders = len(kpi_orders[kpi_orders['status'] == 'delivered'])
        delivery_rate = (delivered_orders / total_orders) * 100 if total_orders > 0 else 0
        create_metric_card("Delivery Rate", delivery_rate, "percentage")
    
    with col3:
        total_deliveries = len(filtered_deliveries)
        breach_rate = (filtered_deliveries['is_breach'].sum() / total_deliveries) * 100 if total_deliveries > 0 else 0
        on_time_rate = 100 - breach_rate
        create_metric_card("On-Time Rate", on_time_rate, "percentage")
    
    with col4:
        breached_deliveries = filtered_deliveries[filtered_deliveries['is_breach']]
        avg_delay = breached_deliveries['delay_minutes'].mean() if len(breached_deliveries) > 0 else 0
        create_metric_card("Avg Delay", avg_delay, "time")
    
    with col5:
        total_revenue = kpi_orders['order_value'].sum()
        create_metric_card("Total Revenue", total_revenue, "currency")
    
    # Charts Section
    st.header("📊 Performance Analysis")
    
    # Row 1: SLA Breach Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("SLA Breach Rate Over Time")
        if filtered_deliveries.empty:
            fig = create_empty_figure("Daily SLA Breach Rate Trend")
        else:
            daily_breaches = filtered_deliveries.groupby(filtered_deliveries['pickup_time'].dt.date)['is_breach'].mean() * 100
            daily_breaches = daily_breaches.reset_index()
            daily_breaches.columns = ['Date', 'Breach Rate (%)']
            
            fig = px.line(daily_breaches, x='Date', y='Breach Rate (%)', 
                         title="Daily SLA Breach Rate Trend")
            fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Delay Distribution")
        breached_deliveries = filtered_deliveries[filtered_deliveries['is_breach']]

        if breached_deliveries.empty:
            fig = create_empty_figure("Delivery Delay Distribution")
        else:
            fig = px.histogram(breached_deliveries, x='delay_minutes', 
                              title="Delivery Delay Distribution",
                              labels={'delay_minutes': 'Delay (minutes)'},
                              nbins=30)
            fig.add_vline(x=0, line_dash="dash", line_color="red", 
                         annotation_text="SLA Deadline")
            fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: Hub and Rider Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hub Performance")
        if filtered_deliveries.empty:
            fig = create_empty_figure("SLA Breach Rate by Hub")
        else:
            hub_performance = filtered_deliveries.groupby('hub_id')['is_breach'].mean() * 100
            hub_performance = hub_performance.reset_index()
            hub_performance = hub_performance.merge(hubs[['hub_id', 'display_name']], on='hub_id')
            hub_performance.columns = ['hub_id', 'breach_rate', 'display_name']
            
            fig = px.bar(hub_performance, x='display_name', y='breach_rate',
                        title="SLA Breach Rate by Hub",
                        labels={'display_name': 'Hub', 'breach_rate': 'Breach Rate (%)'})
            fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("SLA Breach Rate by Hour of Day")
        if filtered_deliveries.empty:
            fig = create_empty_figure("Hourly SLA Breach Rate Heatmap (Day of Week vs Time)")
        else:
            heatmap_deliveries = filtered_deliveries.copy()
            heatmap_deliveries['hour'] = heatmap_deliveries['pickup_time'].dt.hour
            heatmap_deliveries['day_name'] = heatmap_deliveries['pickup_time'].dt.day_name()
            
            hourly_performance = heatmap_deliveries.groupby(['day_name', 'hour'])['is_breach'].mean() * 100
            hourly_performance = hourly_performance.reset_index()
            
            heatmap_data = hourly_performance.pivot(index='day_name', columns='hour', values='is_breach')
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])
            heatmap_data = heatmap_data.reindex(columns=range(24), fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=[f"{h:02d}:00" for h in heatmap_data.columns],
                y=heatmap_data.index,
                colorscale='RdYlGn_r',
                text=np.round(heatmap_data.values, 1),
                texttemplate='%{text:.1f}%',
                textfont={"size": 9},
                colorbar=dict(title="Breach Rate (%)")
            ))
            
            fig.update_layout(
                title="Hourly SLA Breach Rate Heatmap (Day of Week vs Time)",
                xaxis_title="Hour of Day",
                yaxis_title="Day of Week",
                height=400,
                xaxis={'side': 'bottom'}
            )
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Order Status and Revenue
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Status Distribution")
        if filtered_orders.empty:
            fig = create_empty_figure("Order Status Distribution")
        else:
            status_counts = filtered_orders['status'].value_counts()
            
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Order Status Distribution")
            fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Order Status")
        if filtered_orders.empty:
            fig = create_empty_figure("Revenue by Order Status")
        else:
            revenue_by_status = filtered_orders.groupby('status')['order_value'].sum()
            
            fig = px.bar(x=revenue_by_status.index, y=revenue_by_status.values,
                        title="Revenue by Order Status",
                        labels={'x': 'Status', 'y': 'Revenue ($)'})
            fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Tables Section
    st.header("📋 Detailed Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Orders", "Deliveries", "Hubs", "Riders"])
    
    with tab1:
        st.subheader("Orders Data")
        st.dataframe(filtered_orders.head(100), use_container_width=True)
        st.caption(f"Showing first 100 of {len(filtered_orders)} orders")
    
    with tab2:
        st.subheader("Deliveries Data")
        # Add breach status for better visibility
        display_deliveries = filtered_deliveries.copy()
        display_deliveries['SLA Status'] = display_deliveries['is_breach'].map({True: '❌ Breached', False: '✅ On Time'})
        st.dataframe(display_deliveries[['delivery_id', 'order_id', 'rider_id', 'hub_id', 'SLA Status', 'delay_minutes']].head(100), use_container_width=True)
        st.caption(f"Showing first 100 of {len(filtered_deliveries)} deliveries")
    
    with tab3:
        st.subheader("Hubs Data")
        st.dataframe(hubs, use_container_width=True)
    
    with tab4:
        st.subheader("Riders Data")
        st.dataframe(riders, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard generated from 50K+ delivery records • Data period: November-December 2025*")

if __name__ == "__main__":
    main()
