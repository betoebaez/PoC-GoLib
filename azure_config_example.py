#!/usr/bin/env python3
"""
Ejemplo de configuración para Azure Key Vault con LibCoreHey

Este archivo muestra cómo configurar Azure Key Vault para usar con LibCoreHey.
"""

import os
import libcorehey as LibCoreHey


def example_usage():
    """Ejemplo de uso con Azure Key Vault y Managed Identity."""
    
    # Configuración de Azure Key Vault con Managed Identity
    vault_config = {
        # URL de tu Key Vault en Azure
        "vault_url": "https://your-keyvault.vault.azure.net",
        
        # Usar Managed Identity (recomendado en Azure)
        "use_managed_identity": True,
        
        # Opcional: Client ID para User-Assigned Managed Identity
        # Si no se especifica, usa System-Assigned Managed Identity
        "client_id": "87654321-4321-4321-4321-210987654321"
    }
    
    # Nota: Los secretos en Key Vault deben tener estos nombres exactos:
    # - url-whatapp: https://whatsapp-cloud-api-bpue47stva-uc.a.run.app
    # - token-whatapp: tu-token-de-api
    
    # Parámetros de la API
    org_id = "your-organization"
    group_id = "your-group"
    
    try:
        # Llamada usando Azure Key Vault
        quick_replies = LibCoreHey.get_quick_replies(vault_config, org_id, group_id)
        print("Quick Replies:", quick_replies)
        
        typifications = LibCoreHey.get_typification(vault_config, org_id, group_id)
        print("Typifications:", typifications)
        
    except Exception as e:
        print(f"Error: {e}")


def setup_environment_variables():
    """Configura las variables de entorno para Azure con Managed Identity."""
    
    # Variables mínimas requeridas para Managed Identity
    os.environ["AZURE_KEY_VAULT_URL"] = "https://your-keyvault.vault.azure.net"
    
    # Opcional: Para User-Assigned Managed Identity
    # Si no se especifica, usa System-Assigned Managed Identity
    os.environ["AZURE_CLIENT_ID"] = "87654321-4321-4321-4321-210987654321"
    
    # Los nombres de secretos están hardcodeados en la librería:
    # url-whatapp y token-whatapp


if __name__ == "__main__":
    print("🔐 Azure Key Vault Configuration Example")
    print("=" * 45)
    
    print("\n1. Setup Azure Key Vault:")
    print("   - Create a Key Vault in Azure Portal")
    print("   - Enable Managed Identity on your Azure service")
    print("   - Grant Key Vault access to Managed Identity")
    print("   - Add secrets with exact names:")
    print("     • url-whatapp: https://whatsapp-cloud-api-bpue47stva-uc.a.run.app")
    print("     • token-whatapp: your-whatsapp-api-token")
    
    print("\n2. Configure environment:")
    print("   - Set AZURE_KEY_VAULT_URL")
    print("   - Optional: Set AZURE_CLIENT_ID (for User-Assigned MI)")
    print("   - No secrets needed! (Managed Identity handles auth)")
    
    print("\n3. Use LibCoreHey with vault config:")
    print("   vault_config = {'vault_url': '...', 'use_managed_identity': True}")
    print("   LibCoreHey.get_quick_replies(vault_config, org, group)")
    
    print("\n📖 For detailed setup instructions, see:")
    print("https://docs.microsoft.com/en-us/azure/key-vault/general/overview")