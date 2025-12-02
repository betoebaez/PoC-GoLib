#!/usr/bin/env python3
"""
Ejemplo de uso ultra-simple de LibCoreHey en Azure

Este ejemplo muestra cómo usar LibCoreHey de la forma más simple posible
cuando la aplicación está corriendo en Azure con Managed Identity habilitado.
"""

import os
import libcorehey as LibCoreHey


def example_minimal_config():
    """
    Ejemplo con configuración mínima para apps corriendo en Azure.
    
    Prerequisitos:
    1. App corriendo en Azure con Managed Identity habilitado
    2. Variable de entorno AZURE_KEY_VAULT_URL configurada
    3. Secretos url-whatapp y token-whatapp en Key Vault
    """
    print("🚀 Ejemplo: Configuración Mínima (Azure)")
    print("=" * 45)
    
    # Opción 1: Ultra-simple - solo necesita los parámetros de negocio
    try:
        replies = LibCoreHey.get_quick_replies_simple("org123", "group456")
        print("✅ Quick Replies:", replies[:100] + "...")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_with_manual_vault_url():
    """
    Ejemplo especificando manualmente la URL del vault.
    """
    print("\n🔧 Ejemplo: Con URL de Vault Manual")
    print("=" * 45)
    
    try:
        vault_url = "https://my-vault.vault.azure.net"
        replies = LibCoreHey.get_quick_replies_simple(
            "org123", 
            "group456", 
            vault_url=vault_url
        )
        print("✅ Quick Replies:", replies[:100] + "...")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_full_control():
    """
    Ejemplo con control completo de la configuración.
    """
    print("\n⚙️  Ejemplo: Control Completo")
    print("=" * 45)
    
    try:
        # Crear configuración personalizada
        config = LibCoreHey.create_azure_config(
            vault_url="https://my-vault.vault.azure.net",
            client_id="optional-user-assigned-mi-client-id"
        )
        
        replies = LibCoreHey.get_quick_replies(config, "org123", "group456")
        print("✅ Quick Replies:", replies[:100] + "...")
    except Exception as e:
        print(f"❌ Error: {e}")


def check_environment():
    """
    Verificar configuración del ambiente.
    """
    print("\n🔍 Verificación de Ambiente")
    print("=" * 30)
    
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    client_id = os.getenv("AZURE_CLIENT_ID")
    
    print(f"AZURE_KEY_VAULT_URL: {'✅' if vault_url else '❌'} {vault_url or 'No configurado'}")
    print(f"AZURE_CLIENT_ID: {'✅' if client_id else '⚠️'} {client_id or 'No configurado (opcional)'}")
    
    if not vault_url:
        print("\n💡 Para configurar:")
        print("export AZURE_KEY_VAULT_URL='https://your-vault.vault.azure.net'")


if __name__ == "__main__":
    print("🔐 LibCoreHey - Azure Ultra-Simple Examples")
    print("=" * 50)
    
    check_environment()
    
    # Diferentes niveles de simplicidad
    example_minimal_config()
    example_with_manual_vault_url()
    example_full_control()
    
    print("\n📚 Resumen de opciones:")
    print("1. get_quick_replies_simple(org, group) - Ultra simple")
    print("2. get_quick_replies_simple(org, group, vault_url) - Con URL manual")
    print("3. get_quick_replies(config, org, group) - Control completo")