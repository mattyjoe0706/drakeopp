#!/bin/bash
# Install and run Drake vs The Opps game

echo "🎮 Drake vs The Opps - Setup Script"
echo "=================================="

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 found"

# Try to install pygame
echo "📦 Installing pygame..."

# Try different installation methods
if python3 -m pip install pygame==2.5.2 --user 2>/dev/null; then
    echo "✓ Pygame installed successfully with pip --user"
elif python3 -m pip install pygame --user 2>/dev/null; then
    echo "✓ Pygame installed successfully (latest version)"
elif sudo apt-get update && sudo apt-get install -y python3-pygame 2>/dev/null; then
    echo "✓ Pygame installed via apt"
else
    echo "⚠️  Could not install pygame automatically."
    echo "Please install pygame manually:"
    echo "  sudo apt install python3-pygame"
    echo "  OR"
    echo "  pip install pygame --user"
    echo ""
    echo "Then run: python3 main.py"
    exit 1
fi

echo ""
echo "🚀 Starting game..."
python3 main.py