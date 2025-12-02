# Distribución Multiplataforma con GitHub Actions

LibCoreHey ahora incluye **GitHub Actions** para compilar automáticamente en todas las plataformas.

## 🚀 Cómo funciona:

### Al subir a GitHub:
1. **GitHub Actions se ejecuta automáticamente**
2. **Compila en 3 plataformas simultáneamente:**
   - 🍎 macOS → `libcorehey.dylib`
   - 🐧 Linux → `libcorehey.so`  
   - 🪟 Windows → `libcorehey.dll`
3. **Crea un paquete con todos los binarios**
4. **Sube automáticamente a PyPI (opcional)**

### Para los usuarios finales:
```bash
pip install LibCoreHey  # ✅ Funciona en Mac, Linux, Windows
```

## 📋 Configuración incluida:

- ✅ **`.github/workflows/build.yml`** - Workflow de GitHub Actions
- ✅ **`setup.py` actualizado** - Soporta binarios precompilados
- ✅ **Detección inteligente** - Build automático vs binarios precompilados

## 🎯 Resultado:

**¡SÍ! Al subir a GitHub será AUTOMÁTICAMENTE multiplataforma** 🌍

Los usuarios podrán hacer `pip install LibCoreHey` desde cualquier plataforma y funcionará perfectamente.

## 📝 Próximos pasos:

1. **Subir a GitHub**
2. **GitHub Actions compilará automáticamente**
3. **¡Listo! Multiplataforma completa**

**Tu librería será verdaderamente multiplataforma desde el primer push a GitHub.** 🚀