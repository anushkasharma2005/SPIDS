#!/bin/bash

echo "================================================="
echo "   Inflation Simulation - Installation Script"
echo "================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is not installed."
    echo "Please install Python3 and try again."
    exit 1
fi

echo "✅ Python3 found."

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Warning: pip3 not found. Trying 'python3 -m pip'..."
else
    echo "✅ pip3 found."
fi

# Create Virtual Environment
echo "-------------------------------------------------"
echo " Setting up virtual environment 'sim_env'..."
echo "-------------------------------------------------"

if [ ! -d "sim_env" ]; then
    python3 -m venv sim_env
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment."
        echo "Please ensure you have venv installed (e.g., sudo apt install python3-venv)"
        exit 1
    fi
    echo "✅ Virtual environment created."
else
    echo " Virtual environment 'sim_env' already exists."
fi

# Install dependencies in virtual environment
echo "-------------------------------------------------"
echo " Installing dependencies into 'sim_env'..."
echo "-------------------------------------------------"

# Activate and install
source sim_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================="
    echo "✅ Installation complete!"
    echo ""
    echo " To run the simulation:"
    echo "   1. Activate the environment:"
    echo "      source sim_env/bin/activate"
    echo ""
    echo "   2. Run the code:"
    echo "      python3 main.py"
    echo "================================================="
else
    echo ""
    echo "❌ Error: Failed to install dependencies."
    echo "Please check your internet connection or permissions."
fi
