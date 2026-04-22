#!/usr/bin/env python3


import subprocess
import sys
import os

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

def install_dependencies():
    try:
        import streamlit
        import plotly
        print("Dependencies already installed")
        return True
    except ImportError:
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            return False

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
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()
