#!/bin/bash

# Vigyoti Voice Demo Generator - Setup Script
# This script sets up the environment for generating AI receptionist demos

set -e  # Exit on error

echo "========================================="
echo "Vigyoti Voice Demo Generator - Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment already exists"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip in virtual environment
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "Setting up environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ElevenLabs API key"
    echo ""
    echo "To get your API key:"
    echo "1. Visit: https://elevenlabs.io/app/settings/api-keys"
    echo "2. Copy your API key"
    echo "3. Edit .env and replace 'your_api_key_here' with your actual key"
    echo ""
    
    # Try to open .env in default editor
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        read -p "Would you like to open .env now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open -e .env
        fi
    fi
else
    echo "✅ .env file already exists"
fi
echo ""

# Create output directory
echo "Creating output directory..."
mkdir -p output
echo "✅ Output directory created"
echo ""

# Test API connection (if API key is set)
if grep -q "your_api_key_here" .env 2>/dev/null; then
    echo "⚠️  API key not configured yet"
    echo ""
    echo "Next steps:"
    echo "1. Add your ElevenLabs API key to .env"
    echo "2. Run: python3 generate_conversations.py --test-mode"
else
    echo "✅ API key appears to be configured"
    echo ""
    echo "Setup complete! 🎉"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Test with: python3 generate_conversations.py --test-mode"
    echo "3. Generate all: python3 generate_conversations.py --all"
fi

echo ""
echo "========================================="
echo "💡 Remember to activate the virtual environment"
echo "   Run: source venv/bin/activate"
echo ""
echo "For help, see README.md"
echo "========================================="
