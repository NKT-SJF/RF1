import tkinter as tk
from tkinter import scrolledtext, Scale
import subprocess
import os
import shutil

def ejF():
    name = entry_nombre.get()
    if not name:
        mostrar_resultado("Por favor ingrese un nombre.")
        return
    
    script_path = r'C:\Users\Streaming\Desktop\RF1-main\Reconocimiento Facial\code\Faces.py'
    try:
        result = subprocess.run(["python", script_path, name], capture_output=True, text=True)
        mostrar_resultado(result.stdout)
        entry_nombre.delete(0,tk.END)
    except Exception as e:
        mostrar_resultado(f"Error al ejecutar el código: {str(e)}")

def ejRF():
    script_path = r'C:\Users\Streaming\Desktop\RF1-main\Reconocimiento Facial\code\FacialRecognizer.py'
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        mostrar_resultado(result.stdout)
    except Exception as e:
        mostrar_resultado(f"Error al ejecutar el código: {str(e)}")

def ejMRF():
    script_path = r'C:\Users\Streaming\Desktop\RF1-main\Reconocimiento Facial\code\ModelsFaceRecognizer.py'
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

    carpeta_data = r'C:\Users\Streaming\Desktop\RF1-main\Reconocimiento Facial\Data'
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
ventana.geometry('1920x1040')

frame1 = tk.Frame(ventana, bg='lightblue',padx=10,pady=10)
frame1.place(relheight=1,relwidth=0.2,x=1280,y=0)

entry_nombre = tk.Entry(frame1, fg='gray')
entry_nombre.place(x=10,y=10,relwidth=0.8,height=40)

boton_ejF = tk.Button(frame1, text="Captura de cara", command=ejF, bg='lightgray')
boton_ejF.place(x=10,y=60,relwidth=0.8,height=40)

boton_ejRF = tk.Button(frame1, text="Reconocimiento Facial", command=ejRF, bg='lightgray')
boton_ejRF.place(x=10,y=110,relwidth=0.8,height=40)

boton_ejMRF = tk.Button(frame1, text="Entrenar modelo", command=ejMRF, bg='lightgray')
boton_ejMRF.place(x=10,y=160,relwidth=0.8,height=40)

boton_borrar = tk.Button(frame1, text="Borrar subcarpeta", command=DU, bg='lightgray')
boton_borrar.place(x=10,y=210,relwidth=0.8,height=40)

texto_resultado = scrolledtext.ScrolledText(ventana, width=120, height=20)
texto_resultado.place(x=5,y=10, relheight=0.98,relwidth=0.82)

ventana.mainloop()