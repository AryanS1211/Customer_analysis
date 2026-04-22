#!/usr/bin/env python3


import subprocess
import sys
import os

def install_dependencies():
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    return True

def run_analysis():
    print("Running delivery analysis...")
    try:
        subprocess.check_call([sys.executable, "delivery_analysis.py"])
        print("Analysis completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Analysis failed: {e}")
        return False
    return True

def main():
    print("Delivery Analysis Project")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found. Please run from the project root directory.")
        sys.exit(1)
    
    if not os.path.exists("delivery_analysis.py"):
        print("Error: delivery_analysis.py not found.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run analysis
    if not run_analysis():
        sys.exit(1)
    
    print("\nProject execution completed!")
    print("Check the generated files:")
    print("- delivery_analysis_report.png (visualizations)")
    print("- Console output for performance metrics")

if __name__ == "__main__":
    main()
