-- SQL Analysis Queries for Delivery Data

-- Identify SLA Breaches
SELECT 
    d.delivery_id,
    d.order_id,
    d.actual_delivery_time,
    d.sla_deadline,
    CASE WHEN d.actual_delivery_time > d.sla_deadline THEN 'Breach' ELSE 'On Time' END AS sla_status,
    EXTRACT(EPOCH FROM (d.actual_delivery_time - d.sla_deadline))/60 AS delay_minutes
FROM deliveries d
WHERE d.actual_delivery_time IS NOT NULL;

-- Delay Trends by Hour
SELECT 
    EXTRACT(HOUR FROM d.delivery_time) AS delivery_hour,
    COUNT(*) AS total_deliveries,
    AVG(EXTRACT(EPOCH FROM (d.actual_delivery_time - d.sla_deadline))/60) AS avg_delay_minutes,
    COUNT(CASE WHEN d.actual_delivery_time > d.sla_deadline THEN 1 END) AS breaches
FROM deliveries d
WHERE d.actual_delivery_time IS NOT NULL
GROUP BY delivery_hour
ORDER BY delivery_hour;

-- Hub-level Performance
SELECT 
    h.hub_name,
    COUNT(d.delivery_id) AS total_deliveries,
    COUNT(CASE WHEN d.actual_delivery_time <= d.sla_deadline THEN 1 END) * 100.0 / COUNT(d.delivery_id) AS on_time_rate,
    AVG(EXTRACT(EPOCH FROM (d.actual_delivery_time - d.pickup_time))/60) AS avg_turnaround_minutes
FROM deliveries d
JOIN hubs h ON d.hub_id = h.hub_id
WHERE d.actual_delivery_time IS NOT NULL
GROUP BY h.hub_id, h.hub_name;

-- Rider-level Performance
SELECT 
    r.rider_name,
    COUNT(d.delivery_id) AS total_deliveries,
    COUNT(CASE WHEN d.actual_delivery_time <= d.sla_deadline THEN 1 END) * 100.0 / COUNT(d.delivery_id) AS on_time_rate,
    AVG(EXTRACT(EPOCH FROM (d.actual_delivery_time - d.sla_deadline))/60) AS avg_delay_minutes
FROM deliveries d
JOIN riders r ON d.rider_id = r.rider_id
WHERE d.actual_delivery_time IS NOT NULL
GROUP BY r.rider_id, r.rider_name;
