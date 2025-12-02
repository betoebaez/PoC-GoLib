#!/bin/bash

# Script para compilar binarios para todas las plataformas
# Usa este script cuando tengas acceso a cada plataforma

echo "🏗️  Compilando LibCoreHey para todas las plataformas..."

# Crear directorio si no existe
mkdir -p libcorehey

# macOS (ya tienes este)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Compilando para macOS..."
    go build -buildmode=c-shared -o libcorehey/libcorehey.dylib lib.go
    codesign -s - libcorehey/libcorehey.dylib 2>/dev/null || echo "⚠️  Firma opcional"
    echo "✅ macOS: libcorehey.dylib"
fi

echo ""
echo "📝 Para completar la compilación multiplataforma:"
echo ""
echo "🐧 En una máquina Linux:"
echo "   go build -buildmode=c-shared -o libcorehey/libcorehey.so lib.go"
echo ""
echo "🪟 En una máquina Windows:"
echo "   go build -buildmode=c-shared -o libcorehey/libcorehey.dll lib.go"
echo ""
echo "💡 Alternativas:"
echo "   • Usar GitHub Actions (ya configurado)"
echo "   • Usar Docker para Linux"
echo "   • Pedir a colaboradores con otras plataformas"
echo ""
echo "🎯 Una vez que tengas todos los binarios:"
echo "   git add libcorehey/*.{dylib,so,dll}"
echo "   git commit -m 'Add pre-built binaries for all platforms'"
echo "   git push"