-- PostgreSQL Data Models for Delivery Analysis

-- Orders Table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date TIMESTAMP,
    delivery_address TEXT,
    order_value DECIMAL(10,2),
    status VARCHAR(50)
);

-- Deliveries Table
CREATE TABLE deliveries (
    delivery_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    rider_id INT,
    hub_id INT,
    pickup_time TIMESTAMP,
    delivery_time TIMESTAMP,
    sla_deadline TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    status VARCHAR(50)
);

-- Hubs Table
CREATE TABLE hubs (
    hub_id SERIAL PRIMARY KEY,
    hub_name VARCHAR(100),
    location VARCHAR(100)
);

-- Riders Table
CREATE TABLE riders (
    rider_id SERIAL PRIMARY KEY,
    rider_name VARCHAR(100),
    hub_id INT REFERENCES hubs(hub_id)
);

-- Performance Metrics Table
CREATE TABLE performance_metrics (
    metric_id SERIAL PRIMARY KEY,
    date DATE,
    hub_id INT REFERENCES hubs(hub_id),
    rider_id INT REFERENCES riders(rider_id),
    on_time_delivery_rate DECIMAL(5,2),
    hub_efficiency DECIMAL(5,2),
    turnaround_time INTERVAL,
    sla_breaches INT
);
