#aa
import tkinter as tk
from tkinter import ttk

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.geometry("800x600")

# Crear un Canvas
canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, bg="lightgray")
canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# Agregar un scrollbar vertical
scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

# Configurar el scrollbar para interactuar con el Canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Crear un Frame dentro del Canvas
scroll_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

# Añadir contenido al Frame
for i in range(20):
    tk.Label(scroll_frame, text=f"Label {i}").grid(row=i, column=0, sticky="w")

# Configurar la barra de desplazamiento horizontal
canvas.grid_rowconfigure(0, weight=1)
canvas.grid_columnconfigure(0, weight=1)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind("<Configure>", on_frame_configure)
canvas.bind("<MouseWheel>", on_mousewheel)

# Configurar la barra de desplazamiento horizontal
scrollbar.config(command=canvas.yview)

root.mainloop()
