# Power BI Dashboards Documentation

## Overview
This project includes Power BI dashboards designed to track key performance indicators (KPIs) for delivery operations.

## Dashboard Components

### 1. On-Time Delivery Rate Dashboard
- **Purpose:** Monitor the percentage of deliveries completed within SLA deadlines
- **Key Metrics:**
  - Overall on-time delivery rate
  - On-time rate by hub
  - On-time rate by rider
  - Trend over time
- **Visualizations:** Line charts, bar charts, KPI cards

### 2. Hub Efficiency Dashboard
- **Purpose:** Analyze operational efficiency at different hubs
- **Key Metrics:**
  - Average turnaround time per hub
  - Delivery volume per hub
  - Hub utilization rates
  - Cost per delivery
- **Visualizations:** Heat maps, scatter plots, gauge charts

### 3. Turnaround Time Dashboard
- **Purpose:** Track the time from order pickup to delivery completion
- **Key Metrics:**
  - Average turnaround time
  - Turnaround time distribution
  - Peak hour performance
  - Turnaround time by distance
- **Visualizations:** Histograms, time series charts

### 4. SLA Breach Reduction Dashboard
- **Purpose:** Monitor and analyze SLA breaches to identify improvement areas
- **Key Metrics:**
  - Number of SLA breaches
  - Breach rate by time of day
  - Breach rate by hub/rider
  - Root cause analysis
- **Visualizations:** Pie charts, trend lines, drill-down reports

## Data Sources
- PostgreSQL database with order and delivery data
- Real-time data refresh capabilities
- Historical data for trend analysis

## Usage Instructions
1. Open the .pbix files in Power BI Desktop
2. Connect to the PostgreSQL database
3. Refresh data sources
4. Publish to Power BI Service for sharing

## Key Insights
- Identified peak hours with highest breach rates
- Optimized hub assignments based on efficiency metrics
- Reduced operational costs through performance improvements
