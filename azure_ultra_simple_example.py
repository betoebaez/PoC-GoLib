#!/usr/bin/env python3
"""
Ejemplo ULTRA-SIMPLE de LibCoreHey para servidores con az CLI

Este ejemplo es para servidores que ya pueden ejecutar:
az keyvault secret show --vault-name waSecrets --name url-whatapp

¡NO necesita configuración adicional!
"""

import libcorehey as LibCoreHey


def example_zero_config():
    """
    Ejemplo sin configuración alguna.
    
    Prerequisitos:
    - Servidor puede ejecutar: az keyvault secret show --vault-name waSecrets --name url-whatapp
    - Servidor puede ejecutar: az keyvault secret show --vault-name waSecrets --name token-whatapp
    
    ¡Eso es todo!
    """
    print("🎯 ULTRA-SIMPLE: Sin configuración")
    print("=" * 40)
    
    try:
        # ¡Una sola línea! La librería hace todo automáticamente
        replies = LibCoreHey.get_quick_replies_ultra_simple("org123", "group456")
        print("✅ Quick Replies obtenidos!")
        print(f"📄 Respuesta: {replies[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Verifica que puedas ejecutar:")
        print("az keyvault secret show --vault-name waSecrets --name url-whatapp")


def example_custom_vault_name():
    """
    Ejemplo si tu vault NO se llama 'waSecrets'.
    """
    print("\n🔧 Con nombre de vault personalizado")
    print("=" * 40)
    
    import os
    
    # Si tu vault se llama diferente, configura esta variable
    os.environ["AZURE_KEY_VAULT_NAME"] = "mi-vault-personalizado"
    
    try:
        replies = LibCoreHey.get_quick_replies_ultra_simple("org123", "group456")
        print("✅ Quick Replies obtenidos!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def test_az_cli_access():
    """
    Probar si el servidor tiene acceso a az CLI.
    """
    print("\n🧪 Prueba de acceso az CLI")
    print("=" * 30)
    
    import subprocess
    
    try:
        # Probar acceso a url-whatapp
        result = subprocess.run([
            "az", "keyvault", "secret", "show", 
            "--vault-name", "waSecrets", 
            "--name", "url-whatapp", 
            "--query", "value", 
            "-o", "tsv"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Acceso a url-whatapp: OK")
            print(f"🔗 URL: {result.stdout.strip()[:50]}...")
        else:
            print("❌ No se pudo acceder a url-whatapp")
            print(f"Error: {result.stderr}")
            
        # Probar acceso a token-whatapp
        result = subprocess.run([
            "az", "keyvault", "secret", "show", 
            "--vault-name", "waSecrets", 
            "--name", "token-whatapp", 
            "--query", "value", 
            "-o", "tsv"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Acceso a token-whatapp: OK")
            print(f"🔑 Token: {result.stdout.strip()[:20]}...")
        else:
            print("❌ No se pudo acceder a token-whatapp")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - az CLI muy lento")
    except FileNotFoundError:
        print("❌ az CLI no está instalado")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 LibCoreHey - ULTRA-SIMPLE Azure CLI Example")
    print("=" * 55)
    
    # Primero probar acceso
    test_az_cli_access()
    
    # Ejemplo principal
    example_zero_config()
    
    # Ejemplo con vault personalizado
    example_custom_vault_name()
    
    print("\n🎉 ¡Eso es todo!")
    print("Si funciona az CLI, la librería funciona automáticamente.")
    print("\n📚 Funciones disponibles:")
    print("• get_quick_replies_ultra_simple(org, group)")
    print("• get_typification_ultra_simple(org, group)")