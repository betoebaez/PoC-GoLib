import libcorehey as LibCoreHey


def console_interface():
    """Interfaz de consola para interactuar con los métodos de la librería."""
    while True:
        print("\n=== LIBCOREHEY - HEYBANCO API CLIENT ===")
        print("🏦 HEYBANCO APIs:")
        print("1. Obtener Quick Replies (get_quick_replies)")
        print("2. Obtener Tipificaciones (get_typification)")
        print("")
        print("3. Salir")
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                # get_quick_replies
                token = input("Ingrese el token de autorización: ").strip()
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not token or not org or not group:
                    print("❌ Todos los campos son requeridos")
                    continue
                    
                print("🔄 Consultando Quick Replies...")
                result = LibCoreHey.get_quick_replies(token, org, group)
                if result:
                    print(f"✅ Quick Replies obtenidos:\n{result}")
                else:
                    print("❌ No se pudieron obtener los Quick Replies")
                    
            elif choice == "2":
                # get_typification
                token = input("Ingrese el token de autorización: ").strip()
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not token or not org or not group:
                    print("❌ Todos los campos son requeridos")
                    continue
                    
                print("🔄 Consultando Tipificaciones...")
                result = LibCoreHey.get_typification(token, org, group)
                if result:
                    print(f"✅ Tipificaciones obtenidas:\n{result}")
                else:
                    print("❌ No se pudieron obtener las Tipificaciones")
                    
            elif choice == "3":
                print("¡Hasta luego!")
                exit()
                
            else:
                print("❌ Opción no válida. Por favor seleccione 1, 2 o 3.")
                
        except ValueError:
            print("❌ Error: Por favor ingrese valores válidos")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    console_interface()
