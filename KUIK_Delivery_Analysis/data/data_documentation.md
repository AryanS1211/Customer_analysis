# Data Documentation

## Data Sources
This project analyzes delivery data from operations, including:
- Order records (50K+ records)
- Delivery tracking data
- Hub and rider information
- Performance metrics

## Data Structure

### Orders Data
- order_id: Unique identifier for each order
- customer_id: Customer placing the order
- order_date: Timestamp when order was placed
- delivery_address: Delivery location
- order_value: Monetary value of the order
- status: Current order status

### Delivery Data
- delivery_id: Unique delivery identifier
- order_id: Reference to the order
- rider_id: Assigned delivery rider
- hub_id: Originating hub
- pickup_time: When rider picked up the order
- delivery_time: Scheduled delivery time
- sla_deadline: Service level agreement deadline
- actual_delivery_time: Actual delivery completion time
- status: Delivery status

### Hub and Rider Data
- Hub information: Location, capacity, operational hours
- Rider information: Performance history, assigned hub

## Data Quality Notes
- All timestamps are in UTC
- SLA deadlines are calculated based on order type and distance
- Missing actual_delivery_time indicates undelivered orders
- Data covers November-December 2025 period

## Data Loading Instructions
1. Ensure PostgreSQL database is set up
2. Run data_models.sql to create tables
3. Import CSV data files into respective tables
4. Run analysis_queries.sql for insights
