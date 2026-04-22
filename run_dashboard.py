#!/usr/bin/env python3
"""Streamlit Cloud entrypoint for the delivery dashboard."""

from pathlib import Path
import sys


PROJECT_DIR = Path(__file__).resolve().parent / "KUIK_Delivery_Analysis"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from dashboard import main


main()
