import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import shutil

def ejF():
    name = entry_nombre.get()
    if not name:
        mostrar_resultado("Por favor ingrese un nombre.")
        return
    
    script_path = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\code\Faces.py'
    try:
        result = subprocess.run(["python", script_path, name], capture_output=True, text=True)
        mostrar_resultado(result.stdout)
        entry_nombre.delete(0,tk.END)
    except Exception as e:
        mostrar_resultado(f"Error al ejecutar el código: {str(e)}")

def ejRF():
    script_path = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\code\FacialRecognizer.py'
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        mostrar_resultado(result.stdout)
    except Exception as e:
        mostrar_resultado(f"Error al ejecutar el código: {str(e)}")

def ejMRF():
    script_path = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\code\ModelsFaceRecognizer.py'
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        mostrar_resultado(result.stdout)
    except Exception as e:
        mostrar_resultado(f"Error al ejecutar el código: {str(e)}")

def DU():
    subcarpeta = entry_nombre.get()
    if not subcarpeta:
        mostrar_resultado("por favor ingresar el nombre de la carpeta a eliminar")
        return

    carpeta_data = r'C:\Users\garri\OneDrive\Escritorio\Reconocimiento Facial\Data'
    subcarpeta = os.path.join(carpeta_data,subcarpeta)
    if os.path.exists(subcarpeta) and os.path.isdir(subcarpeta):
        try:
            shutil.rmtree(subcarpeta)
            mostrar_resultado(f"Subcarpeta '{subcarpeta}' eliminada correctamente.")
            entry_nombre.delete(0, tk.END)
        except Exception as e:
            mostrar_resultado(f"Error al eliminar la subcarpeta: {str(e)}")
    else:
        mostrar_resultado(f"La subcarpeta '{subcarpeta}' no existe.")

def mostrar_resultado(resultado):
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, resultado)

ventana = tk.Tk()
ventana.title("Reconocimiento Facial")

label_nombre = tk.Label(ventana, text="Ingrese el nombre:")
label_nombre.pack(pady=5)

entry_nombre = tk.Entry(ventana, width=50)
entry_nombre.pack(pady=10)

boton_ejF = tk.Button(ventana, text="Captura de cara", command=ejF)
boton_ejF.pack(pady=10)

boton_ejRF = tk.Button(ventana, text="Reconocimiento Facial", command=ejRF)
boton_ejRF.pack(pady=10)

boton_ejMRF = tk.Button(ventana, text="Entrenar modelo", command=ejMRF)
boton_ejMRF.pack(pady=10)

boton_borrar = tk.Button(ventana, text="Borrar subcarpeta", command=DU)
boton_borrar.pack(pady=10)

texto_resultado = scrolledtext.ScrolledText(ventana, width=80, height=20)
texto_resultado.pack(padx=10, pady=10)

ventana.mainloop()