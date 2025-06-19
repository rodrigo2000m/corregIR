import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from corregIR.controllers.events import open_file, graph_IR, correct_signal, save_file
from corregIR.utils.files import  save_IR_adjusted
from corregIR.utils.helpers import contact
import mplcursors

class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("corregIR")
        self.geometry("400x200")
 

        # main menu
        self.frame_menu = ttk.Frame(self)
        self.frame_menu.grid(row=0, column=0, sticky="ew")  # Expandirse horizontalmente

        self.botton_files = ttk.Button(self.frame_menu, text="Archivo", command=self.show_menu)
        self.botton_files.grid(row=0, column=0) 

        self.botton_manipulation = ttk.Button(self.frame_menu, text="Manipulación", command=self.show_manipulation_options)
        self.botton_manipulation.grid(row=0, column=1)
  
        self.botton_support = ttk.Button(self.frame_menu, text="Soporte", command=self.support_label)
        self.botton_support.grid(row=0, column=2)

        # Click "Archivos"
        self.show_menu = tk.Menu(self, tearoff=0)
        self.show_menu.add_command(label="Abrir", command=self.accion_abrir)
        #self.show_menu.add_command(label="Cerrar", command=self.cerrar)
        self.show_menu.add_separator()
        self.show_menu.add_command(label="Salir", command=self.quit)

        # Click "Manipulación"
        self.show_manipulation_options = tk.Menu(self, tearoff=0)
        self.show_manipulation_options.add_command(label="Linea de base asls", command=self.baseline)
        #self.show_manipulation_options.add_command(label="Suavizado", command=self.smooth)


        # Click soporte

        
   
    def show_menu(self):
        # Mostrar menú en posición del botón
        x = self.botton_files.winfo_rootx()
        y = self.botton_files.winfo_rooty() + self.botton_files.winfo_height()
        self.show_menu.tk_popup(x, y)

    def show_manipulation_options(self):
        x = self.botton_manipulation.winfo_rootx()
        y = self.botton_manipulation.winfo_rooty() + self.botton_manipulation.winfo_height()
        self.show_manipulation_options.tk_popup(x, y)


    # funciones cuando click
    def cerrar(self):
        print("Nuevo archivo")

    def abrir(self):
        print("Abrir archivo")


    def baseline(self):

        #contenido = open_file()
        self.abrir_ventana_valores()

        print("baseline")

#        if contenido is not None:
 #           df_corregido = correct_signal(contenido, lam, p)

  #          graph_IR(contenido)

    def smooth(self):
        print("smooth")
    
    def support_label(self):
        contact(self)
    def accion_abrir(self):
        contenido = open_file()
        if contenido is not None:
            # Mostrar el contenido en un widget, o lo que quieras hacer con él
            print("Contenido del archivo:\n", contenido)
            graph_IR(contenido, "%T")
            plt.tight_layout()
            plt.show(block=False)    

    def abrir_ventana_valores(self):
        contenido = open_file()
        ventana = tk.Toplevel(self)
        ventana.title("Ingresar valores A y B")

        tk.Label(ventana, text="lam:").grid(row=0, column=0, padx=10, pady=5)
        entry_a = tk.Entry(ventana)
        entry_a.grid(row=0, column=1, padx=10, pady=5)
        entry_a.insert(0, "1e9")

        tk.Label(ventana, text="p:").grid(row=1, column=0, padx=10, pady=5)
        entry_b = tk.Entry(ventana)
        entry_b.grid(row=1, column=1, padx=10, pady=5)
        entry_b.insert(0, "0.01")

        def calcular():
            lam = float(entry_a.get())
            p = float(entry_b.get())
            if contenido is not None:
                df = correct_signal(contenido, lam, p)
                lineplot = graph_IR(contenido, "%T_corrected")  
                cursor = mplcursors.cursor(lineplot, multiple=True)
                @cursor.connect("add")
                def on_add(sel):
                    idx = int(sel.index)
                    sel.annotation.set(text=f'{round(df.iloc[idx]["Wavenumeber_cm-1"])} '+"$cm^{-1}$")
                    sel.annotation.get_bbox_patch().set(fc="white", ec="white", lw=1.5, alpha=0)
                    sel.annotation.draggable(True)
                    print(idx)

                plt.tight_layout()
                plt.show(block=False)
        def guardar():
            nombre_archivo = entry_name.get()
            save_file(contenido)
            ventana.destroy()
            plt.close()
 
        boton_calcular = tk.Button(ventana, text="Calcular", command= calcular)
        boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Label(ventana, text="Nombre del archivo:").grid(row=3, column=0, padx=10, pady=5)
        entry_name = tk.Entry(ventana)
        entry_name.grid(row=3, column=1, padx=10, pady=5)
        entry_name.insert(0, "archivo")

        boton_guardar = tk.Button(ventana, text="Guardar espectro ajustado", command=guardar)
        boton_guardar.grid(row=4, column=0, columnspan=2, pady=10)


