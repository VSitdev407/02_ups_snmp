#!/bin/bash

echo "=========================================="
echo "UPS SNMP Monitoring System Setup"
echo "=========================================="

# Check Python 3
echo "Checking Python 3..."
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found: $(python3 --version)"
else
    echo "✗ Python 3 not found. Please install Python 3.6 or higher."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Create logs directory
echo ""
echo "Creating logs directory..."
mkdir -p logs
echo "✓ Logs directory created"

# Test imports
echo ""
echo "Testing system components..."
python3 test_snmp.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Your UPS devices are configured:"
    echo "  • 10F UPS: 172.21.2.13"
    echo "  • 9F  UPS: 172.21.3.11"
    echo "  • 8F  UPS: 172.21.4.10"
    echo "  • 7F  UPS: 172.21.6.10"
    echo "  • 3F  UPS: 172.21.5.14"
    echo ""
    echo "To start monitoring, run:"
    echo "  python3 main.py"
    echo ""
    echo "To test connections first, run:"
    echo "  python3 main.py --test"
else
    echo ""
    echo "✗ Setup failed. Please check the errors above."
    exit 1
fi