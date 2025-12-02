#!/bin/bash

# LibCoreHey Easy Installer
# Installs the latest release of LibCoreHey from GitHub

echo "🚀 LibCoreHey - HeyBanco Python Library Installer"
echo "=================================================="

# Get latest release info
echo "🔍 Checking latest release..."
LATEST_RELEASE=$(curl -s https://api.github.com/repos/betoebaez/PoC-GoLib/releases/latest | grep "tag_name" | cut -d '"' -f 4)

if [ -z "$LATEST_RELEASE" ]; then
    echo "❌ Error: Could not fetch latest release information"
    exit 1
fi

echo "📦 Latest version: $LATEST_RELEASE"

# Install from GitHub release
echo "⬇️  Installing LibCoreHey..."
WHEEL_URL="https://github.com/betoebaez/PoC-GoLib/releases/download/$LATEST_RELEASE/libcorehey-${LATEST_RELEASE#v}-py3-none-any.whl"

pip install "$WHEEL_URL"

if [ $? -eq 0 ]; then
    echo "✅ LibCoreHey installed successfully!"
    echo ""
    echo "🎯 Quick test:"
    echo "python -c \"import libcorehey as LibCoreHey; print('✅ LibCoreHey ready!')\""
    echo ""
    echo "📚 Usage example:"
    echo "import libcorehey as LibCoreHey"
    echo "replies = LibCoreHey.get_quick_replies(token, org, group)"
else
    echo "❌ Installation failed"
    exit 1
fi