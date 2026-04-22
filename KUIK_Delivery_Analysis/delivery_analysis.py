import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def create_sample_data():
    np.random.seed(42)
    
    # Generate sample orders (50K+ records)
    n_orders = 50000
    orders = pd.DataFrame({
        'order_id': range(1, n_orders + 1),
        'customer_id': np.random.randint(1, 10000, n_orders),
        'order_date': pd.date_range('2025-11-01', '2025-12-31', periods=n_orders),
        'order_value': np.random.uniform(10, 200, n_orders),
        'status': np.random.choice(['delivered', 'pending', 'cancelled'], n_orders, p=[0.92, 0.05, 0.03])
    })
    
    # Generate hubs data with display names
    hubs = pd.DataFrame({
        'hub_id': range(1, 21),  # 20 hubs
        'hub_name': [f'Hub_{i}' for i in range(1, 21)],
        'location': ['Downtown', 'Downtown', 'Suburb_South', 'Suburb_North', 'City_Center',
                    'Downtown', 'Suburb_South', 'Suburb_East', 'Downtown', 'Suburb_North',
                    'City_Center', 'Suburb_North', 'Suburb_South', 'Suburb_South', 'Suburb_West',
                    'City_Center', 'City_Center', 'Downtown', 'City_Center', 'Suburb_North'],
    })
    
    # Add display names
    hubs['display_name'] = hubs.apply(
        lambda row: f"{row['location'].replace('_', ' ')} - {row['hub_name']}", 
        axis=1
    )
    
    # Generate riders data
    riders = []
    for hub_id in hubs['hub_id']:
        n_riders_per_hub = np.random.randint(5, 15)  # 5-15 riders per hub
        for i in range(n_riders_per_hub):
            riders.append({
                'rider_id': len(riders) + 1,
                'rider_name': f'Rider_{len(riders) + 1}',
                'hub_id': hub_id
            })
    riders = pd.DataFrame(riders)
    
    # Generate sample deliveries for delivered orders
    delivered_orders = orders[orders['status'] == 'delivered']
    pickup_times = delivered_orders['order_date'] + pd.to_timedelta(np.random.uniform(0, 2, len(delivered_orders)), unit='h')
    
    deliveries = pd.DataFrame({
        'delivery_id': range(1, len(delivered_orders) + 1),
        'order_id': delivered_orders['order_id'].values,
        'rider_id': np.random.choice(riders['rider_id'], len(delivered_orders)),
        'hub_id': np.random.choice(hubs['hub_id'], len(delivered_orders)),
        'pickup_time': pickup_times,
    })
    
    # Add delivery times with realistic breaches based on hour and day
    deliveries['sla_deadline'] = deliveries['pickup_time'] + pd.to_timedelta(np.random.uniform(1, 4, len(delivered_orders)), unit='h')
    
    # Create varying breach rates by day and hour
    hour = deliveries['pickup_time'].dt.hour
    day_of_week = deliveries['pickup_time'].dt.dayofweek  # 0=Monday, 6=Sunday
    
    # Higher breach rate during peak hours (9-11, 14-17) and weekdays
    peak_hour_factor = np.where((hour >= 9) & (hour <= 11), 2.0, 1.0)
    peak_hour_factor = np.where((hour >= 14) & (hour <= 17), 1.8, peak_hour_factor)
    weekend_factor = np.where(day_of_week >= 5, 0.4, 1.0)  # Much lower breach on weekends
    
    # Create realistic breach probability (20-50% depending on time)
    breach_probability = np.minimum(0.3 * peak_hour_factor * weekend_factor, 0.6)
    
    # Create delays: some negative (early), some positive (late)
    is_breach = np.random.random(len(deliveries)) < breach_probability
    
    delays = np.where(
        is_breach,
        np.random.exponential(2.0, len(deliveries)),  # Significant delay if breached (0-8 hours)
        -np.random.exponential(0.3, len(deliveries))  # Arrive early if on-time (-0.5 to 0 hours)
    )
    
    deliveries['actual_delivery_time'] = deliveries['sla_deadline'] + pd.to_timedelta(delays, unit='h')
    deliveries['status'] = 'completed'
    
    # Save data to CSV files
    DATA_DIR.mkdir(exist_ok=True)

    orders_path = DATA_DIR / "orders.csv"
    deliveries_path = DATA_DIR / "deliveries.csv"
    hubs_path = DATA_DIR / "hubs.csv"
    riders_path = DATA_DIR / "riders.csv"

    orders.to_csv(orders_path, index=False)
    deliveries.to_csv(deliveries_path, index=False)
    hubs.to_csv(hubs_path, index=False)
    riders.to_csv(riders_path, index=False)

    print(f"Saved {len(orders)} orders to {orders_path}")
    print(f"Saved {len(deliveries)} deliveries to {deliveries_path}")
    print(f"Saved {len(hubs)} hubs to {hubs_path}")
    print(f"Saved {len(riders)} riders to {riders_path}")
    
    return orders, deliveries

if __name__ == "__main__":
    print("Delivery Analysis - Python Implementation")
    print("=" * 50)
    
    # Create sample data and save to CSV
    orders, deliveries = create_sample_data()
    
    print(f"\nAnalysis complete! CSV files saved to {DATA_DIR}.")
