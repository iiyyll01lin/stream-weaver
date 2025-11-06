#!/bin/bash
#
# Phase 1 Service Startup Script
# Quick Start Script for Phase 1
#

echo "=================================="
echo "Line Balance System Phase 1 Launcher"
echo "Line Balance System - Phase 1"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "❌ Python 3.10+ required, current version: $PYTHON_VERSION"
    echo "Please upgrade Python and try again"
    exit 1
fi

echo "✓ Python version: $PYTHON_VERSION"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."

if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠ Dependencies not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "✓ Dependencies ready"
echo ""

# Check data files
echo "Checking data files..."

if [ ! -f "data/test_tasks.csv" ]; then
    echo "❌ Cannot find data/test_tasks.csv"
    echo "Please ensure data files exist"
    exit 1
fi

echo "✓ Data files exist"
echo ""

# Create output directory
mkdir -p output

# Start service
echo "=================================="
echo "Starting API service..."
echo "=================================="
echo ""
echo "Service URL: http://localhost:8000"
echo "API Documentation: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop service"
echo ""

python3 src/api_server.py
