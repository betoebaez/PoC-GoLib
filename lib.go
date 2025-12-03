package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
	"unsafe"
)

// ============ FUNCIONES ESPECÍFICAS HEYBANCO ============

//export GetQuickReplies
func GetQuickReplies(vaultConfig *C.char, org *C.char, group *C.char) *C.char {
	goVaultConfig := C.GoString(vaultConfig)
	goOrg := C.GoString(org)
	goGroup := C.GoString(group)

	// Obtener baseURL y token desde Azure Key Vault
	baseURL, token, err := getSecretsFromVault(goVaultConfig)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to get secrets: %s"}`, err.Error()))
	}

	fullURL := fmt.Sprintf("%s/v2/quick_replies?org=%s&group=%s", baseURL, goOrg, goGroup)

	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	req, err := http.NewRequest("GET", fullURL, nil)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to create request: %s"}`, err.Error()))
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Request failed: %s"}`, err.Error()))
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to read response: %s"}`, err.Error()))
	}

	return C.CString(string(body))
}

//export GetTypification
func GetTypification(vaultConfig *C.char, org *C.char, group *C.char) *C.char {
	goVaultConfig := C.GoString(vaultConfig)
	goOrg := C.GoString(org)
	goGroup := C.GoString(group)

	// Obtener baseURL y token desde Azure Key Vault
	baseURL, token, err := getSecretsFromVault(goVaultConfig)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to get secrets: %s"}`, err.Error()))
	}

	fullURL := fmt.Sprintf("%s/v2/typification?org=%s&group=%s", baseURL, goOrg, goGroup)

	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	req, err := http.NewRequest("GET", fullURL, nil)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to create request: %s"}`, err.Error()))
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Request failed: %s"}`, err.Error()))
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString(fmt.Sprintf(`{"error": "Failed to read response: %s"}`, err.Error()))
	}

	return C.CString(string(body))
}

// ============ AZURE KEY VAULT INTEGRATION ============

type VaultConfig struct {
	VaultURL string `json:"vault_url,omitempty"` // Opcional si está en variable de entorno
	ClientID string `json:"client_id,omitempty"` // Solo para User-Assigned MI
}

type AzureTokenResponse struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
}

type AzureSecretResponse struct {
	Value string `json:"value"`
}

func getSecretsFromVault(configJSON string) (string, string, error) {
	var config VaultConfig
	if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
		return "", "", fmt.Errorf("invalid vault config: %v", err)
	}

	// Usar solo Managed Identity API
	return getSecretsWithAPI(config)
}

func getAzureAccessToken(config VaultConfig) (string, error) {
	// Usar solo Managed Identity
	return getManagedIdentityToken(config.ClientID)
}

func getManagedIdentityToken(clientID string) (string, error) {
	// Azure Instance Metadata Service (IMDS) endpoint
	imdsURL := "http://169.254.169.254/metadata/identity/oauth2/token"

	// Construir URL con parámetros
	params := "api-version=2018-02-01&resource=https://vault.azure.net"
	if clientID != "" {
		params += "&client_id=" + clientID
	}

	tokenURL := fmt.Sprintf("%s?%s", imdsURL, params)

	req, err := http.NewRequest("GET", tokenURL, nil)
	if err != nil {
		return "", fmt.Errorf("failed to create IMDS request: %v", err)
	}

	// Header requerido por IMDS
	req.Header.Set("Metadata", "true")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to call IMDS: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("IMDS returned status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read IMDS response: %v", err)
	}

	var tokenResp AzureTokenResponse
	if err := json.Unmarshal(body, &tokenResp); err != nil {
		return "", fmt.Errorf("failed to parse IMDS response: %v", err)
	}

	return tokenResp.AccessToken, nil
}

func getSecretFromVault(vaultURL, secretName, accessToken string) (string, error) {
	secretURL := fmt.Sprintf("%s/secrets/%s?api-version=7.4", vaultURL, secretName)

	req, err := http.NewRequest("GET", secretURL, nil)
	if err != nil {
		return "", err
	}

	req.Header.Set("Authorization", "Bearer "+accessToken)

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var secretResp AzureSecretResponse
	if err := json.Unmarshal(body, &secretResp); err != nil {
		return "", fmt.Errorf("failed to parse secret response: %v", err)
	}

	return secretResp.Value, nil
}

func getEnvironmentVariable(name string) string {
	return os.Getenv(name)
}

func getSecretsWithAPI(config VaultConfig) (string, string, error) {
	// Determinar vault URL - puede venir de config o variable de entorno
	vaultURL := config.VaultURL
	if vaultURL == "" {
		// Intentar obtener desde variable de entorno si no se proporcionó
		vaultURL = getEnvironmentVariable("AZURE_KEY_VAULT_URL")
		if vaultURL == "" {
			// Usar vault por defecto si no se especifica ninguno
			vaultName := getEnvironmentVariable("AZURE_KEY_VAULT_NAME")
			if vaultName == "" {
				vaultName = "wasecrets" // Nombre por defecto corregido
			}
			vaultURL = fmt.Sprintf("https://%s.vault.azure.net", vaultName)
		}
	}

	// Obtener token de acceso para Azure Key Vault
	accessToken, err := getAzureAccessToken(config)
	if err != nil {
		return "", "", fmt.Errorf("failed to get access token: %v", err)
	}

	// Obtener baseURL desde Key Vault con nombre fijo
	baseURL, err := getSecretFromVault(vaultURL, "url-whatapp", accessToken)
	if err != nil {
		return "", "", fmt.Errorf("failed to get url-whatapp secret: %v", err)
	}

	// Obtener token desde Key Vault con nombre fijo
	token, err := getSecretFromVault(vaultURL, "token-whatapp", accessToken)
	if err != nil {
		return "", "", fmt.Errorf("failed to get token-whatapp secret: %v", err)
	}

	return baseURL, token, nil
}

// ============ MANEJO DE MEMORIA ============

//export FreeCString
func FreeCString(p *C.char) {
	C.free(unsafe.Pointer(p))
}

// Un paquete -buildmode=c-shared debe compilarse como 'package main' y tener main vacío.
func main() {}
