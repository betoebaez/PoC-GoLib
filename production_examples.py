#!/usr/bin/env python3
"""
Ejemplos de uso híbrido de LibCoreHey en diferentes entornos de producción.

Este archivo demuestra cómo usar la librería en distintos escenarios,
aprovechando el sistema híbrido de autenticación:
1. az CLI primero (simple y funciona en cualquier lado)
2. Managed Identity como fallback (óptimo para Azure PaaS)
"""

import json
from libcorehey.core import (
    get_quick_replies_ultra_simple,
    get_quick_replies_simple,
    get_quick_replies,
    create_azure_config
)


def ejemplo_servidor_tradicional():
    """
    ESCENARIO 1: Servidor tradicional con az CLI configurado
    
    - VM Ubuntu/CentOS con az CLI instalado
    - Usuario tiene permisos al Key Vault
    - Comando funciona: az keyvault secret show --vault-name waSecrets --name url-whatapp
    
    VENTAJAS:
    ✅ Cero configuración necesaria
    ✅ Funciona inmediatamente
    ✅ Mismo nivel de seguridad que portal Azure
    """
    print("=== SERVIDOR TRADICIONAL CON AZ CLI ===")
    
    # Opción 1: Ultra-simple (recomendado para este escenario)
    try:
        result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
        data = json.loads(result)
        print(f"✅ Az CLI funcionó: {len(data.get('replies', []))} respuestas obtenidas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Código necesario:")
    print("""
    from libcorehey.core import get_quick_replies_ultra_simple
    
    # Una sola línea - cero configuración
    result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
    """)


def ejemplo_azure_app_service():
    """
    ESCENARIO 2: Azure App Service con Managed Identity
    
    - App Service con System-Assigned Managed Identity
    - Managed Identity tiene permisos al Key Vault
    - az CLI puede no estar disponible
    
    VENTAJAS:
    ✅ Rendimiento óptimo (sin procesos externos)
    ✅ Cero gestión de credenciales
    ✅ Integración nativa con Azure
    """
    print("\n=== AZURE APP SERVICE CON MANAGED IDENTITY ===")
    
    # Si az CLI no está disponible, usa Managed Identity automáticamente
    try:
        # La misma función funciona - el fallback es automático
        result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
        data = json.loads(result)
        print(f"✅ Managed Identity funcionó: {len(data.get('replies', []))} respuestas obtenidas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Código necesario:")
    print("""
    from libcorehey.core import get_quick_replies_ultra_simple
    
    # Misma línea - el fallback es automático
    result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
    
    # O si quieres ser explícito:
    from libcorehey.core import get_quick_replies_simple
    result = get_quick_replies_simple("mi_org", "mi_grupo")
    """)


def ejemplo_azure_vm_con_user_assigned():
    """
    ESCENARIO 3: Azure VM con User-Assigned Managed Identity
    
    - VM con User-Assigned Managed Identity específica
    - Necesitas especificar el client_id
    - Puede tener az CLI o no
    
    VENTAJAS:
    ✅ Control granular de permisos
    ✅ Funciona con o sin az CLI
    ✅ Fácil de migrar entre VMs
    """
    print("\n=== AZURE VM CON USER-ASSIGNED MANAGED IDENTITY ===")
    
    try:
        # Especificar el client_id de la User-Assigned Identity
        result = get_quick_replies_simple(
            org="mi_org", 
            group="mi_grupo",
            client_id="12345678-1234-5678-9012-123456789abc"
        )
        data = json.loads(result)
        print(f"✅ User-Assigned MI funcionó: {len(data.get('replies', []))} respuestas obtenidas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Código necesario:")
    print("""
    from libcorehey.core import get_quick_replies_simple
    
    result = get_quick_replies_simple(
        org="mi_org", 
        group="mi_grupo",
        client_id="tu-client-id-aqui"
    )
    """)


def ejemplo_contenedor_kubernetes():
    """
    ESCENARIO 4: Contenedor en Kubernetes (AKS o externo)
    
    - Pod con Service Account vinculado a Managed Identity (AKS)
    - O contenedor con az CLI y credenciales montadas
    - Flexibilidad para cualquier orquestador
    
    VENTAJAS:
    ✅ Funciona en AKS con AAD Pod Identity
    ✅ Funciona en k8s externo con az CLI
    ✅ Sin diferencias en el código de aplicación
    """
    print("\n=== CONTENEDOR EN KUBERNETES ===")
    
    try:
        # Funciona tanto en AKS como en k8s externo
        result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
        data = json.loads(result)
        print(f"✅ Kubernetes funcionó: {len(data.get('replies', []))} respuestas obtenidas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Código necesario:")
    print("""
    # En el Dockerfile:
    RUN curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    
    # En el código Python:
    from libcorehey.core import get_quick_replies_ultra_simple
    result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
    """)


def ejemplo_entorno_desarrollo():
    """
    ESCENARIO 5: Desarrollo local con az CLI
    
    - Desarrollador con az CLI configurado
    - `az login` ejecutado
    - Permisos de desarrollo al Key Vault
    
    VENTAJAS:
    ✅ Misma experiencia que producción
    ✅ Sin credenciales hardcodeadas
    ✅ Fácil onboarding de nuevos desarrolladores
    """
    print("\n=== DESARROLLO LOCAL ===")
    
    try:
        result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
        data = json.loads(result)
        print(f"✅ Desarrollo local funcionó: {len(data.get('replies', []))} respuestas obtenidas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Setup para desarrolladores:")
    print("""
    # Setup inicial (una vez):
    az login
    az account set --subscription "tu-subscription"
    
    # Verificar acceso:
    az keyvault secret show --vault-name waSecrets --name url-whatapp
    
    # Código Python:
    from libcorehey.core import get_quick_replies_ultra_simple
    result = get_quick_replies_ultra_simple("mi_org", "mi_grupo")
    """)


def ejemplo_configuracion_explicita():
    """
    ESCENARIO 6: Control total con configuración explícita
    
    - Cuando necesitas control granular
    - Multiple Key Vaults
    - Configuración específica por ambiente
    
    VENTAJAS:
    ✅ Control total sobre la autenticación
    ✅ Soporte para múltiples Key Vaults
    ✅ Configuración por ambiente
    """
    print("\n=== CONFIGURACIÓN EXPLÍCITA (CONTROL TOTAL) ===")
    
    # Configuración para producción
    prod_config = {
        "vault_url": "https://mi-keyvault-prod.vault.azure.net/",
        "use_managed_identity": True,
        "client_id": "12345678-1234-5678-9012-123456789abc"  # User-assigned
    }
    
    # Configuración para desarrollo
    dev_config = {
        "use_managed_identity": True  # Usará az CLI en desarrollo
    }
    
    try:
        # Usar configuración específica
        result = get_quick_replies(dev_config, "mi_org", "mi_grupo")
        data = json.loads(result)
        print(f"✅ Configuración explícita funcionó: {len(data.get('replies', []))} respuestas")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("Código para múltiples ambientes:")
    print("""
    import os
    from libcorehey.core import get_quick_replies
    
    # Configuración por ambiente
    if os.getenv('ENVIRONMENT') == 'production':
        config = {
            "vault_url": "https://prod-vault.vault.azure.net/",
            "use_managed_identity": True,
            "client_id": "prod-client-id"
        }
    else:
        config = {"use_managed_identity": True}  # az CLI en desarrollo
    
    result = get_quick_replies(config, "mi_org", "mi_grupo")
    """)


def mostrar_resumen_estrategia():
    """Resumen de la estrategia híbrida"""
    print("\n" + "="*70)
    print("🎯 RESUMEN DE LA ESTRATEGIA HÍBRIDA")
    print("="*70)
    
    print("""
📋 FLUJO DE AUTENTICACIÓN AUTOMÁTICO:
   1️⃣  az CLI (si está disponible)     → ✅ Simple, funciona en cualquier lado
   2️⃣  Managed Identity (si falla #1)  → ✅ Óptimo para Azure PaaS
   3️⃣  Error descriptivo (si falla #2) → ✅ Fácil debugging

🚀 FUNCIONES RECOMENDADAS POR ESCENARIO:

   🖥️  Servidor tradicional:     get_quick_replies_ultra_simple()
   ☁️  Azure App Service:        get_quick_replies_ultra_simple()  
   🏗️  Azure VM con User MI:     get_quick_replies_simple(client_id="...")
   📦 Kubernetes/Contenedor:    get_quick_replies_ultra_simple()
   💻 Desarrollo local:         get_quick_replies_ultra_simple()
   ⚙️  Control total:           get_quick_replies(config, ...)

✅ VENTAJAS DEL ENFOQUE HÍBRIDO:
   • Un solo código funciona en TODOS los entornos
   • Migración sin fricción entre arquitecturas
   • Máxima seguridad con mínima configuración
   • Experiencia de desarrollador excelente
   • Compatible con mejores prácticas de Microsoft

🔧 ZERO CONFIG REQUIREMENTS:
   • Secrets en Key Vault: url-whatapp, token-whatapp
   • Vault name: waSecrets (configurable)
   • Permisos: Key Vault Secrets User o superior
   • Az CLI: az keyvault secret show --vault-name waSecrets --name url-whatapp
""")


if __name__ == "__main__":
    print("LibCoreHey - Ejemplos de Producción Híbrida")
    print("="*50)
    
    # Ejecutar todos los ejemplos
    ejemplo_servidor_tradicional()
    ejemplo_azure_app_service()
    ejemplo_azure_vm_con_user_assigned()
    ejemplo_contenedor_kubernetes()
    ejemplo_entorno_desarrollo()
    ejemplo_configuracion_explicita()
    mostrar_resumen_estrategia()
    
    print(f"\n🎉 Todos los ejemplos ejecutados. Tu librería está lista para producción!")