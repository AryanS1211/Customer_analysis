#!/usr/bin/env python3
"""
Delivery Analysis Dashboard Launcher
Run this from the Customer_analysis directory
"""

import os
import sys
import subprocess

def main():
    print("🚚 Delivery Analysis Dashboard Launcher")
    print("=" * 40)
    
    # Change to the project directory
    project_dir = "KUIK_Delivery_Analysis"
    
    if not os.path.exists(project_dir):
        print(f"❌ Error: Project directory '{project_dir}' not found!")
        print("Please ensure you're running this from the Customer_analysis directory.")
        sys.exit(1)
    
    print(f"📁 Changing to project directory: {project_dir}")
    os.chdir(project_dir)
    
    # Check if dashboard files exist
    if not os.path.exists("run_dashboard.py"):
        print("❌ Error: run_dashboard.py not found in project directory!")
        sys.exit(1)
    
    if not os.path.exists("dashboard.py"):
        print("❌ Error: dashboard.py not found in project directory!")
        sys.exit(1)
    
    print("✅ Found dashboard files")
    print("🚀 Launching dashboard...")
    print("-" * 40)
    
    # Run the dashboard
    try:
        subprocess.run([sys.executable, "run_dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
