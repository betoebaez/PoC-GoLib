package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
	"unsafe"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	azsecrets "github.com/Azure/azure-sdk-for-go/sdk/keyvault/azsecrets"
)

// ============ FUNCIONES ESPECÍFICAS HEYBANCO ============

//export GetQuickReplies
func GetQuickReplies(vaultConfig *C.char, org *C.char, group *C.char) *C.char {
	goVaultConfig := C.GoString(vaultConfig)
	goOrg := C.GoString(org)
	goGroup := C.GoString(group)

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

// ============ AZURE KEY VAULT (WORKLOAD IDENTITY) ============

type VaultConfig struct {
	VaultURL string `json:"vault_url,omitempty"`
}

// getSecretsFromVault resuelve la URL del Key Vault y usa DefaultAzureCredential
// para leer los secretos url-whatapp y token-whatapp.
func getSecretsFromVault(configJSON string) (string, string, error) {
	var config VaultConfig
	if configJSON != "" {
		if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
			return "", "", fmt.Errorf("invalid vault config: %v", err)
		}
	}

	vaultURL := config.VaultURL
	if vaultURL == "" {
		vaultURL = os.Getenv("AZURE_KEY_VAULT_URL")
		if vaultURL == "" {
			vaultName := os.Getenv("AZURE_KEY_VAULT_NAME")
			if vaultName == "" {
				vaultName = "wasecrets"
			}
			vaultURL = fmt.Sprintf("https://%s.vault.azure.net", vaultName)
		}
	}

	cred, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		return "", "", fmt.Errorf("failed to create DefaultAzureCredential: %w", err)
	}

	client, err := azsecrets.NewClient(vaultURL, cred, nil)
	if err != nil {
		return "", "", fmt.Errorf("failed to create secrets client: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	baseURL, err := getSecretValue(ctx, client, "url-whatapp")
	if err != nil {
		return "", "", fmt.Errorf("failed to get url-whatapp secret: %w", err)
	}

	token, err := getSecretValue(ctx, client, "token-whatapp")
	if err != nil {
		return "", "", fmt.Errorf("failed to get token-whatapp secret: %w", err)
	}

	return baseURL, token, nil
}

func getSecretValue(ctx context.Context, client *azsecrets.Client, name string) (string, error) {
	// Versión vacía ("") => última versión del secreto
	resp, err := client.GetSecret(ctx, name, "", nil)
	if err != nil {
		return "", err
	}
	if resp.Value == nil {
		return "", fmt.Errorf("secret %s has nil value", name)
	}
	return *resp.Value, nil
}

// ============ MANEJO DE MEMORIA ============

//export FreeCString
func FreeCString(p *C.char) {
	C.free(unsafe.Pointer(p))
}

// Requerido para -buildmode=c-shared
func main() {}
