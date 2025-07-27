#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# For Render, we'll use a different approach
# Chrome will be available in the runtime environment
echo "Build completed successfully!"
echo "Chrome and ChromeDriver will be available in the runtime environment." 