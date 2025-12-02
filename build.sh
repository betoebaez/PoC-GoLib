#!/bin/bash

# Build script for LibCoreHey shared library
# Builds the Go shared library for different platforms

set -e

echo "🏗️  Building LibCoreHey shared library..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if lib.go exists
if [ ! -f "lib.go" ]; then
    echo "❌ Error: lib.go not found in current directory"
    exit 1
fi

# Create libcorehey directory if it doesn't exist
mkdir -p libcorehey

# Detect platform and build accordingly
OS="$(uname -s)"
case "${OS}" in
    Linux*)
        echo "🐧 Building for Linux..."
        go build -buildmode=c-shared -o libcorehey/libcorehey.so lib.go
        echo "✅ Built libcorehey.so"
        ;;
    Darwin*)
        echo "🍎 Building for macOS..."
        go build -buildmode=c-shared -o libcorehey/libcorehey.dylib lib.go
        
        # Sign the library for macOS
        echo "✍️  Signing library..."
        codesign -s - libcorehey/libcorehey.dylib 2>/dev/null || echo "⚠️  Warning: Could not sign library"
        
        echo "✅ Built libcorehey.dylib"
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo "🪟 Building for Windows..."
        go build -buildmode=c-shared -o libcorehey/libcorehey.dll lib.go
        echo "✅ Built libcorehey.dll"
        ;;
    *)
        echo "❌ Error: Unsupported operating system: ${OS}"
        exit 1
        ;;
esac

echo ""
echo "🎉 Build completed successfully!"
echo "📁 Library location: libcorehey/"
echo ""
echo "💡 Next steps:"
echo "   pip install -e ."
echo "   python -c \"import libcorehey; print('LibCoreHey installed successfully!')\""