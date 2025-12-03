from libcorehey.core import get_quick_replies_ultra_simple, get_typification_ultra_simple
import json


def console_interface():
    """Interfaz simple para probar los endpoints de HeyBanco."""
    while True:
        print("\n=== LIBCOREHEY - HEYBANCO API CLIENT ===")
        print("1. Quick Replies")
        print("2. Tipificaciones")
        print("3. Salir")
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                org = input("Organización: ").strip()
                group = input("Grupo: ").strip()
                
                if not org or not group:
                    print("❌ Organización y grupo son requeridos")
                    continue
                    
                print("🔄 Consultando Quick Replies...")
                result = get_quick_replies_ultra_simple(org, group)
                print_result(result)
                    
            elif choice == "2":
                org = input("Organización: ").strip()
                group = input("Grupo: ").strip()
                
                if not org or not group:
                    print("❌ Organización y grupo son requeridos")
                    continue
                    
                print("🔄 Consultando Tipificaciones...")
                result = get_typification_ultra_simple(org, group)
                print_result(result)
                    
            elif choice == "3":
                print("¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida. Seleccione 1, 2 o 3.")
                
        except Exception as e:
            print(f"❌ Error: {e}")


def print_result(result):
    """Muestra el resultado de la consulta."""
    if result:
        try:
            parsed = json.loads(result)
            if "error" in parsed:
                print(f"❌ Error: {parsed['error']}")
            else:
                print("✅ Resultado:")
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"✅ Resultado: {result}")
    else:
        print("❌ Sin respuesta")


if __name__ == "__main__":
    console_interface()
