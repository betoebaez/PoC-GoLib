import ctypes
import os
from ctypes import c_int, c_char_p, POINTER, byref

os.environ['DYLD_LIBRARY_PATH'] = '.'

lib = ctypes.CDLL("./libmylib.so")

# int Add(int a, int b);
lib.Add.argtypes = [c_int, c_int]
lib.Add.restype = c_int

# int Multiply(int a, int b);
lib.Multiply.argtypes = [c_int, c_int]
lib.Multiply.restype = c_int

# int Fibonacci(int n);
lib.Fibonacci.argtypes = [c_int]
lib.Fibonacci.restype = c_int

# int IsPrime(int n);
lib.IsPrime.argtypes = [c_int]
lib.IsPrime.restype = c_int

# char* GetQuickReplies(char* token, char* org, char* group);
lib.GetQuickReplies.argtypes = [c_char_p, c_char_p, c_char_p]
lib.GetQuickReplies.restype = c_char_p

# char* GetTypification(char* token, char* org, char* group);
lib.GetTypification.argtypes = [c_char_p, c_char_p, c_char_p]
lib.GetTypification.restype = c_char_p

# void FreeCString(char* p);
lib.FreeCString.argtypes = [c_char_p]
lib.FreeCString.restype = None


def add_numbers(a: int, b: int) -> int:
    """Suma dos números y regresa el resultado."""
    result = lib.Add(a, b)
    return int(result)


def multiply_numbers(a: int, b: int) -> int:
    """Multiplica dos números y regresa el resultado."""
    result = lib.Multiply(a, b)
    return int(result)


def get_fibonacci(n: int) -> int:
    """Calcula el n-ésimo número de Fibonacci."""
    result = lib.Fibonacci(n)
    return int(result)


def is_prime(n: int) -> bool:
    """Verifica si un número es primo."""
    result = lib.IsPrime(n)
    return result != 0


def get_quick_replies(token: str, org: str, group: str) -> str:
    """Obtiene quick replies de HeyBanco para una organización y grupo específicos."""
    token_bytes = token.encode('utf-8')
    org_bytes = org.encode('utf-8')
    group_bytes = group.encode('utf-8')
    
    result_ptr = lib.GetQuickReplies(token_bytes, org_bytes, group_bytes)
    if result_ptr:
        try:
            # Convertir el puntero a string sin liberar (Go maneja su memoria)
            result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
            return result
        except:
            return ""
    return ""


def get_typification(token: str, org: str, group: str) -> str:
    """Obtiene tipificaciones de HeyBanco para una organización y grupo específicos."""
    token_bytes = token.encode('utf-8')
    org_bytes = org.encode('utf-8')
    group_bytes = group.encode('utf-8')
    
    result_ptr = lib.GetTypification(token_bytes, org_bytes, group_bytes)
    if result_ptr:
        try:
            # Convertir el puntero a string sin liberar (Go maneja su memoria)
            result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
            return result
        except:
            return ""
    return ""


def console_interface():
    """Interfaz de consola para interactuar con los métodos de la librería."""
    while True:
        print("\n=== BIBLIOTECA MULTIFUNCIONAL - MODO CONSOLA ===")
        print("📊 MATEMÁTICAS:")
        print("1. Sumar dos números (add_numbers)")
        print("2. Multiplicar dos números (multiply_numbers)")
        print("3. Calcular Fibonacci (get_fibonacci)")
        print("4. Verificar si es primo (is_prime)")
        print("")
        print("🏦 HEYBANCO APIs:")
        print("5. Obtener Quick Replies (get_quick_replies)")
        print("6. Obtener Tipificaciones (get_typification)")
        print("")
        print("7. Volver al menú principal")
        print("8. Salir")
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                # add_numbers
                a = int(input("Ingrese el primer número: "))
                b = int(input("Ingrese el segundo número: "))
                result = add_numbers(a, b)
                print(f"✅ Resultado de {a} + {b} = {result}")
                
            elif choice == "2":
                # multiply_numbers
                a = int(input("Ingrese el primer número: "))
                b = int(input("Ingrese el segundo número: "))
                result = multiply_numbers(a, b)
                print(f"✅ Resultado de {a} × {b} = {result}")
                    
            elif choice == "3":
                # get_fibonacci
                n = int(input("Ingrese el número para calcular Fibonacci: "))
                if n < 0:
                    print("❌ Por favor ingrese un número no negativo")
                    continue
                result = get_fibonacci(n)
                print(f"✅ Fibonacci({n}) = {result}")
                    
            elif choice == "4":
                # is_prime
                n = int(input("Ingrese el número para verificar si es primo: "))
                if n < 2:
                    print("❌ Por favor ingrese un número mayor o igual a 2")
                    continue
                result = is_prime(n)
                if result:
                    print(f"✅ {n} ES un número primo")
                else:
                    print(f"❌ {n} NO es un número primo")
                    
            elif choice == "5":
                # get_quick_replies
                token = input("Ingrese el token de autorización: ").strip()
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not token or not org or not group:
                    print("❌ Todos los campos son requeridos")
                    continue
                    
                print("🔄 Consultando Quick Replies...")
                result = get_quick_replies(token, org, group)
                if result:
                    print(f"✅ Quick Replies obtenidos:\n{result}")
                else:
                    print("❌ No se pudieron obtener los Quick Replies")
                    
            elif choice == "6":
                # get_typification
                token = input("Ingrese el token de autorización: ").strip()
                org = input("Ingrese la organización: ").strip()
                group = input("Ingrese el grupo: ").strip()
                
                if not token or not org or not group:
                    print("❌ Todos los campos son requeridos")
                    continue
                    
                print("🔄 Consultando Tipificaciones...")
                result = get_typification(token, org, group)
                if result:
                    print(f"✅ Tipificaciones obtenidas:\n{result}")
                else:
                    print("❌ No se pudieron obtener las Tipificaciones")
                    
            elif choice == "7":
                break
                
            elif choice == "8":
                print("¡Hasta luego!")
                exit()
                
            else:
                print("❌ Opción no válida")
                
        except ValueError:
            print("❌ Error: Ingrese un número válido")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


def gui_interface():
    """Interfaz gráfica para interactuar con los métodos de la librería."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext
        import json
    except ImportError:
        print("❌ Error: tkinter no está disponible. Usando modo consola.")
        console_interface()
        return
    
    def show_json_result(title, json_text):
        """Muestra el resultado JSON en una ventana formateada."""
        json_window = tk.Toplevel(root)
        json_window.title(title)
        json_window.geometry("700x500")
        # json_window.configure(bg="#000000")
        
        # Frame principal
        main_frame = tk.Frame(json_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text=title, font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Intentar formatear el JSON
        try:
            json_obj = json.loads(json_text)
            formatted_json = json.dumps(json_obj, indent=2, ensure_ascii=False, sort_keys=True)
        except json.JSONDecodeError:
            formatted_json = json_text  # Si no es JSON válido, mostrar tal como está
        
        # Cuadro de texto con scroll
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
        json_text_widget = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=25,
            font=("Consolas", 11),
            bg="#2d3748",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            selectbackground="#4a5568"
        )
        json_text_widget.pack(fill="both", expand=True)
        
        # Insertar el JSON formateado con colores
        json_text_widget.insert(tk.END, formatted_json)
        json_text_widget.config(state="disabled")  # Solo lectura
        
        # Configurar colores para JSON (syntax highlighting básico)
        json_text_widget.tag_configure("key", foreground="#63b3ed")
        json_text_widget.tag_configure("string", foreground="#68d391")
        json_text_widget.tag_configure("number", foreground="#fbb6ce")
        json_text_widget.tag_configure("boolean", foreground="#fbd38d")
        json_text_widget.tag_configure("null", foreground="#a0aec0")
        
        # Botones
        button_frame = tk.Frame(main_frame, bg="#000000")
        button_frame.pack(pady=(10, 0))
        
        tk.Button(button_frame, text="Copiar", command=lambda: copy_to_clipboard(formatted_json),
                  bg="#000000", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Cerrar", command=json_window.destroy,
                  bg="#000000", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        # Función para copiar al portapapeles
        def copy_to_clipboard(text):
            json_window.clipboard_clear()
            json_window.clipboard_append(text)
            messagebox.showinfo("Copiado", "JSON copiado al portapapeles")
        
        # Centrar la ventana
        json_window.transient(root)
        json_window.grab_set()
        
        # Enfocar la ventana
        json_window.focus_set()
    
    def execute_method():
        method = method_var.get()
        try:
            if method == "add_numbers":
                a = int(num1_entry.get())
                b = int(num2_entry.get())
                result = add_numbers(a, b)
                messagebox.showinfo("Resultado", f"{a} + {b} = {result}")
                
            elif method == "multiply_numbers":
                a = int(num1_entry.get())
                b = int(num2_entry.get())
                result = multiply_numbers(a, b)
                messagebox.showinfo("Resultado", f"{a} × {b} = {result}")
                    
            elif method == "get_fibonacci":
                n = int(num1_entry.get())
                if n < 0:
                    messagebox.showerror("Error", "Por favor ingrese un número no negativo")
                    return
                result = get_fibonacci(n)
                messagebox.showinfo("Resultado", f"Fibonacci({n}) = {result}")
                
            elif method == "is_prime":
                n = int(num1_entry.get())
                if n < 2:
                    messagebox.showerror("Error", "Por favor ingrese un número mayor or igual a 2")
                    return
                result = is_prime(n)
                if result:
                    messagebox.showinfo("Resultado", f"{n} ES un número primo")
                else:
                    messagebox.showinfo("Resultado", f"{n} NO es un número primo")
                    
            elif method == "get_quick_replies":
                token = token_entry.get().strip()
                org = org_entry.get().strip()
                group = group_entry.get().strip()
                
                if not token or not org or not group:
                    messagebox.showerror("Error", "Todos los campos son requeridos para Quick Replies")
                    return
                    
                result = get_quick_replies(token, org, group)
                if result:
                    show_json_result("🚀 Quick Replies - Respuesta API", result)
                else:
                    messagebox.showerror("Error", "No se pudieron obtener los Quick Replies")
                    
            elif method == "get_typification":
                token = token_entry.get().strip()
                org = org_entry.get().strip()
                group = group_entry.get().strip()
                
                if not token or not org or not group:
                    messagebox.showerror("Error", "Todos los campos son requeridos para Tipificaciones")
                    return
                    
                result = get_typification(token, org, group)
                if result:
                    show_json_result("🏦 Tipificaciones - Respuesta API", result)
                else:
                    messagebox.showerror("Error", "No se pudieron obtener las Tipificaciones")
                    
        except ValueError as e:
            messagebox.showerror("Error de entrada", "Por favor ingrese valores válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def update_fields(*args):
        # Limpiar campos
        for widget in [num1_entry, num2_entry, token_entry, org_entry, group_entry]:
            widget.delete(0, tk.END)
        
        method = method_var.get()
        if method == "add_numbers" or method == "multiply_numbers":
            # Mostrar campos numéricos, ocultar campos API
            num1_label.config(state="normal", text="Primer número:")
            num1_entry.config(state="normal")
            num2_label.config(state="normal", text="Segundo número:")
            num2_entry.config(state="normal")
            token_label.config(state="disabled", text="")
            token_entry.config(state="disabled")
            org_label.config(state="disabled", text="")
            org_entry.config(state="disabled")
            group_label.config(state="disabled", text="")
            group_entry.config(state="disabled")
            
        elif method == "get_fibonacci":
            num1_label.config(state="normal", text="Número n:")
            num1_entry.config(state="normal")
            num2_label.config(state="disabled", text="")
            num2_entry.config(state="disabled")
            token_label.config(state="disabled", text="")
            token_entry.config(state="disabled")
            org_label.config(state="disabled", text="")
            org_entry.config(state="disabled")
            group_label.config(state="disabled", text="")
            group_entry.config(state="disabled")
            
        elif method == "is_prime":
            num1_label.config(state="normal", text="Número a verificar:")
            num1_entry.config(state="normal")
            num2_label.config(state="disabled", text="")
            num2_entry.config(state="disabled")
            token_label.config(state="disabled", text="")
            token_entry.config(state="disabled")
            org_label.config(state="disabled", text="")
            org_entry.config(state="disabled")
            group_label.config(state="disabled", text="")
            group_entry.config(state="disabled")
            
        elif method == "get_quick_replies":
            # Ocultar campos numéricos, mostrar campos API
            num1_label.config(state="disabled", text="")
            num1_entry.config(state="disabled")
            num2_label.config(state="disabled", text="")
            num2_entry.config(state="disabled")
            token_label.config(state="normal", text="Token:")
            token_entry.config(state="normal")
            org_label.config(state="normal", text="Organización:")
            org_entry.config(state="normal")
            group_label.config(state="normal", text="Grupo:")
            group_entry.config(state="normal")
            
        elif method == "get_typification":
            num1_label.config(state="disabled", text="")
            num1_entry.config(state="disabled")
            num2_label.config(state="disabled", text="")
            num2_entry.config(state="disabled")
            token_label.config(state="normal", text="Token:")
            token_entry.config(state="normal")
            org_label.config(state="normal", text="Organización:")
            org_entry.config(state="normal")
            group_label.config(state="normal", text="Grupo:")
            group_entry.config(state="normal")
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("Biblioteca Multifuncional - Interfaz Gráfica")
    root.geometry("600x500")
    
    # Selector de método
    tk.Label(root, text="Seleccionar función:", font=("Arial", 12, "bold")).pack(pady=10)
    method_var = tk.StringVar(value="add_numbers")
    method_combo = ttk.Combobox(root, textvariable=method_var, 
                               values=["add_numbers", "multiply_numbers", "get_fibonacci", "is_prime", "get_quick_replies", "get_typification"],
                               state="readonly")
    method_combo.pack(pady=5)
    method_var.trace("w", update_fields)
    
    # Frame para los campos
    fields_frame = tk.Frame(root)
    fields_frame.pack(pady=20, padx=20, fill="x")
    
    # Campo número 1
    num1_label = tk.Label(fields_frame, text="Primer número:")
    num1_label.grid(row=0, column=0, sticky="w", pady=5)
    num1_entry = tk.Entry(fields_frame, width=30)
    num1_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
    
    # Campo número 2
    num2_label = tk.Label(fields_frame, text="Segundo número:")
    num2_label.grid(row=1, column=0, sticky="w", pady=5)
    num2_entry = tk.Entry(fields_frame, width=30)
    num2_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
    
    # Campo token
    token_label = tk.Label(fields_frame, text="Token:")
    token_label.grid(row=2, column=0, sticky="w", pady=5)
    token_entry = tk.Entry(fields_frame, width=30, show="*")
    token_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
    
    # Campo organización
    org_label = tk.Label(fields_frame, text="Organización:")
    org_label.grid(row=3, column=0, sticky="w", pady=5)
    org_entry = tk.Entry(fields_frame, width=30)
    org_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
    
    # Campo grupo
    group_label = tk.Label(fields_frame, text="Grupo:")
    group_label.grid(row=4, column=0, sticky="w", pady=5)
    group_entry = tk.Entry(fields_frame, width=30)
    group_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
    
    # Notas
    notes_frame = tk.Frame(root)
    notes_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(notes_frame, text="💡 Los campos se habilitan automáticamente según la función seleccionada",
             font=("Arial", 9), fg="gray").pack()
    tk.Label(notes_frame, text="🔒 El campo token se oculta por seguridad",
             font=("Arial", 8), fg="gray").pack()
    
    # Botones
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Ejecutar", command=execute_method, 
              bg="#000000", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="Volver al menú", command=root.destroy,
              bg="#000000", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    
    # Inicializar campos
    update_fields()
    
    root.mainloop()


def main_menu():
    """Menú principal para elegir entre consola o interfaz gráfica."""
    print("🚀 === BIBLIOTECA MULTIFUNCIONAL ===")
    print("¡Bienvenido! Esta aplicación incluye funciones matemáticas y APIs de HeyBanco.")
    print("Elija el modo de interacción:")
    
    while True:
        print("\n1. Modo Consola")
        print("2. Modo Interfaz Gráfica")
        print("3. Salir")
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                console_interface()
            elif choice == "2":
                gui_interface()
            elif choice == "3":
                print("¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida. Por favor seleccione 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main_menu()
