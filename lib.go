package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"io"
	"net/http"
	"time"
	"unsafe"
)

// ============ FUNCIONES ESPECÍFICAS HEYBANCO ============

//export GetQuickReplies
func GetQuickReplies(token *C.char, org *C.char, group *C.char) *C.char {
	goToken := C.GoString(token)
	goOrg := C.GoString(org)
	goGroup := C.GoString(group)

	// URL base fija de HeyBanco
	baseURL := "https://whatsapp-cloud-api-bpue47stva-uc.a.run.app"
	fullURL := fmt.Sprintf("%s/v2/quick_replies?org=%s&group=%s", baseURL, goOrg, goGroup)

	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	req, err := http.NewRequest("GET", fullURL, nil)
	if err != nil {
		return C.CString("")
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+goToken)

	resp, err := client.Do(req)
	if err != nil {
		return C.CString("")
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString("")
	}

	return C.CString(string(body))
}

//export GetTypification
func GetTypification(token *C.char, org *C.char, group *C.char) *C.char {
	goToken := C.GoString(token)
	goOrg := C.GoString(org)
	goGroup := C.GoString(group)

	// URL base fija de HeyBanco
	baseURL := "https://whatsapp-cloud-api-bpue47stva-uc.a.run.app"
	fullURL := fmt.Sprintf("%s/v2/typification?org=%s&group=%s", baseURL, goOrg, goGroup)

	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	req, err := http.NewRequest("GET", fullURL, nil)
	if err != nil {
		return C.CString("")
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+goToken)

	resp, err := client.Do(req)
	if err != nil {
		return C.CString("")
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString("")
	}

	return C.CString(string(body))
}

// ============ MANEJO DE MEMORIA ============

//export FreeCString
func FreeCString(p *C.char) {
	C.free(unsafe.Pointer(p))
}

// Un paquete -buildmode=c-shared debe compilarse como 'package main' y tener main vacío.
func main() {}
