#!/usr/bin/env python3
"""
GWAS SNP Search Web Application Startup Script
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'selenium', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_chrome():
    """Check if Chrome browser is available"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✅ Chrome browser and ChromeDriver are working")
        return True
    except Exception as e:
        print("❌ Chrome browser or ChromeDriver not found")
        print(f"   Error: {e}")
        print("\n🔧 Please install Chrome browser and ChromeDriver:")
        print("   Windows: choco install chromedriver")
        print("   macOS: brew install chromedriver")
        print("   Linux: sudo apt-get install chromium-chromedriver")
        return False

def main():
    print("🚀 Starting GWAS SNP Search Web Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Chrome
    if not check_chrome():
        sys.exit(1)
    
    print("\n🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 