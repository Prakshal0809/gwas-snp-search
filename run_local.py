#!/usr/bin/env python3
"""
Local development script for GWAS SNP Search
This script runs the Flask app locally without webdriver-manager
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("Starting GWAS SNP Search locally...")
    print("Make sure you have Chrome and ChromeDriver installed locally")
    print("Access the app at: http://localhost:5000")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000) 