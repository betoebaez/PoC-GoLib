#!/bin/bash

# Distribution build script for LibCoreHey
# Builds the package ready for PyPI upload

set -e

echo "📦 Building LibCoreHey distribution package..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Clean previous builds
echo "🧹 Cleaning previous build artifacts..."
rm -rf build/ dist/ *.egg-info/

# Build the Go library first
echo "🏗️  Building Go shared library..."
./build.sh

# Install build dependencies
echo "📋 Installing build dependencies..."
pip install --upgrade build twine

# Build source and wheel distributions
echo "🛠️  Building Python package..."
python -m build

echo "✅ Build completed!"
echo ""
echo "📁 Distribution files created:"
ls -la dist/

echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Test the built package:"
echo "   pip install dist/LibCoreHey-1.0.0-py3-none-any.whl"
echo ""
echo "2. Upload to TestPyPI (optional):"
echo "   twine upload --repository testpypi dist/*"
echo ""
echo "3. Upload to PyPI:"
echo "   twine upload dist/*"
echo ""
echo "💡 Make sure you have PyPI credentials configured before uploading!"