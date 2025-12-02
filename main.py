import libcorehey as LibCoreHey
from libcorehey.core import get_quick_replies_ultra_simple, get_typification_ultra_simple
import os
import json


def console_interface():
    """Interfaz de consola para interactuar con los métodos de la librería usando sistema híbrido."""
    while True:
        print("\n=== LIBCOREHEY - HEYBANCO API CLIENT (Sistema Híbrido) ===")
        print("🏦 HEYBANCO APIs:")
        print("1. Obtener Quick Replies (Ultra Simple - Zero Config)")
        print("2. Obtener Tipificaciones (Ultra Simple - Zero Config)")
        print("3. Ver información del sistema híbrido")
        print("4. Salir")
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                # get_quick_replies ultra simple
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not org or not group:
                    print("❌ Organización y grupo son requeridos")
                    continue
                    
                print("🔄 Consultando Quick Replies (sistema híbrido: az CLI → Managed Identity)...")
                result = get_quick_replies_ultra_simple(org, group)
                if result:
                    try:
                        parsed = json.loads(result)
                        if "error" in parsed:
                            print(f"❌ Error: {parsed['error']}")
                        else:
                            print("✅ Quick Replies obtenidos:")
                            print(json.dumps(parsed, indent=2, ensure_ascii=False))
                    except json.JSONDecodeError:
                        print(f"✅ Quick Replies obtenidos:\n{result}")
                else:
                    print("❌ No se pudieron obtener los Quick Replies")
                    
            elif choice == "2":
                # get_typification ultra simple
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not org or not group:
                    print("❌ Organización y grupo son requeridos")
                    continue
                    
                print("🔄 Consultando Tipificaciones (sistema híbrido: az CLI → Managed Identity)...")
                result = get_typification_ultra_simple(org, group)
                if result:
                    try:
                        parsed = json.loads(result)
                        if "error" in parsed:
                            print(f"❌ Error: {parsed['error']}")
                        else:
                            print("✅ Tipificaciones obtenidas:")
                            print(json.dumps(parsed, indent=2, ensure_ascii=False))
                    except json.JSONDecodeError:
                        print(f"✅ Tipificaciones obtenidas:\n{result}")
                else:
                    print("❌ No se pudieron obtener las Tipificaciones")
                    
            elif choice == "3":
                show_hybrid_system_info()
                    
            elif choice == "4":
                print("¡Hasta luego!")
                exit()
                
            else:
                print("❌ Opción no válida. Por favor seleccione 1, 2, 3 o 4.")
                
        except ValueError:
            print("❌ Error: Por favor ingrese valores válidos")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


def show_hybrid_system_info():
    """Muestra información sobre el sistema híbrido de autenticación."""
    print("\n🔄 SISTEMA HÍBRIDO DE AUTENTICACIÓN")
    print("=" * 60)
    print("🎯 ZERO CONFIG: No necesita variables de entorno!")
    print("")
    print("📋 FLUJO AUTOMÁTICO:")
    print("1️⃣  az CLI (si está disponible)     → ✅ Simple, funciona en cualquier lado")
    print("2️⃣  Managed Identity (si falla #1)  → ✅ Óptimo para Azure PaaS")
    print("3️⃣  Error descriptivo (si falla #2) → ✅ Fácil debugging")
    print("")
    print("🔧 REQUISITOS MÍNIMOS:")
    print("• Key Vault: waSecrets (por defecto)")
    print("• Secrets requeridos:")
    print("  - url-whatapp: https://whatsapp-cloud-api-bpue47stva-uc.a.run.app")
    print("  - token-whatapp: [your-whatsapp-api-token]")
    print("• Permisos: Key Vault Secrets User o superior")
    print("")
    print("🖥️  SERVIDOR TRADICIONAL:")
    print("   • az CLI instalado y configurado")
    print("   • az keyvault secret show --vault-name waSecrets --name url-whatapp")
    print("")
    print("☁️  AZURE PAAS (App Service, Functions):")
    print("   • Managed Identity habilitada")
    print("   • Permisos asignados al Key Vault")
    print("")
    print("💡 VENTAJAS:")
    print("   ✅ Un solo código funciona en TODOS los entornos")
    print("   ✅ Migración sin fricción entre arquitecturas")
    print("   ✅ Máxima seguridad con mínima configuración")
    print("   ✅ Sin credenciales hardcodeadas")
    print("")
    print("🧪 VERIFICAR ACCESO AZ CLI:")
    print("az keyvault secret show --vault-name waSecrets --name url-whatapp --query value -o tsv")
    print("")
    input("Presione Enter para continuar...")


if __name__ == "__main__":
    console_interface()
