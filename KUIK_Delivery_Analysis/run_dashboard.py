#!/usr/bin/env python3


import os
import subprocess
import sys

def check_csv_files():
    required_files = [
        'data/orders.csv',
        'data/deliveries.csv', 
        'data/hubs.csv',
        'data/riders.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing CSV data files. Please run analysis first:")
        print(" python delivery_analysis.py")
        print(f"Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def launch_dashboard():
    print("Launching Delivery Analysis Dashboard...")
    print("Dashboard will open in your default web browser")
    print("URL: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

def main():
    print("Delivery Analysis Dashboard")
    print("=" * 40)
    
    # Check if CSV files exist
    if not check_csv_files():
        sys.exit(1)
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()
