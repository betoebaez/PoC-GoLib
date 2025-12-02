#!/bin/bash

# Script para preparar librerías .so en macOS
# Uso: ./fix_library.sh [nombre_libreria.so]

LIBRARY=${1:-"libmylib.so"}

if [ ! -f "$LIBRARY" ]; then
    echo "❌ Error: No se encontró la librería '$LIBRARY'"
    echo "Uso: $0 [nombre_libreria.so]"
    exit 1
fi

echo "🔧 Preparando librería '$LIBRARY' para macOS..."

# 1. Remover atributos extendidos (cuarentena, etc.)
echo "📋 Removiendo atributos extendidos..."
xattr -c "$LIBRARY" 2>/dev/null || echo "   ℹ️  No hay atributos extendidos"

# 2. Remover firma existente
echo "🗑️  Removiendo firma existente..."
codesign --remove-signature "$LIBRARY" 2>/dev/null || echo "   ℹ️  No había firma previa"

# 3. Refirmar con firma local
echo "✍️  Aplicando nueva firma local..."
if codesign -s - "$LIBRARY"; then
    echo "✅ Librería '$LIBRARY' preparada exitosamente"
    
    # 4. Verificar que funciona
    echo "🧪 Verificando carga de librería..."
    if DYLD_LIBRARY_PATH=. python3 -c "import ctypes; ctypes.CDLL('./$LIBRARY')" 2>/dev/null; then
        echo "✅ ¡Librería lista para usar!"
        echo ""
        echo "💡 Para ejecutar tu aplicación:"
        echo "   DYLD_LIBRARY_PATH=. python3 main.py"
        echo "   o simplemente: ./run_native.sh"
    else
        echo "❌ Error al verificar la librería"
    fi
else
    echo "❌ Error al firmar la librería"
    exit 1
fi