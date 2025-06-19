from tkinter import filedialog, messagebox
import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import mplcursors
from matplotlib.widgets import Slider
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import sparse
from scipy.sparse.linalg import spsolve
from matplotlib.widgets import Slider
from scipy.signal import savgol_filter
from pybaselines import Baseline, utils
from corregIR.utils.files import read_file, save_IR_adjusted


def open_file():
    path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if path:
        try:
            df = read_file(path)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
            return None

def save_file(df):
    filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar archivo como"
            )

    if filepath:
        save_IR_adjusted(df, filepath)
        print(f"Archivo guardado en: {filepath}")
    else:
        print("Archivo cancelado")


def graph_IR(df, y_label):
    fig, ax = plt.subplots(figsize=(10, 4))
    lineplot = sns.lineplot(df, x = "Wavenumeber_cm-1", y=y_label, ax=ax, color="red")

    plt.plot(df["Wavenumeber_cm-1"], df[y_label], color="red",  label="Línea ajustada")
    
    (lineplot,) = ax.plot(df["Wavenumeber_cm-1"], df[y_label], color="red", label="Línea ajustada")
    
    ax.set_xlabel('Wavenumber ($cm^{-1}$)')  
    ax.set_ylabel('%T') 

    ax.set_xlim(400, 4000)
    ax.invert_xaxis()
    
    return lineplot
    #cursor = mplcursors.cursor(lineplot, multiple=True)

    #@cursor.connect("add")

    #def on_add(sel):
        #idx = int(sel.index)
        #sel.annotation.set(text=f'{round(df.iloc[idx]["Wavenumeber_cm-1"])} '+"$cm^{-1}$")
        #sel.annotation.get_bbox_patch().set(fc="white", ec="white", lw=1.5, alpha=0)
        #sel.annotation.draggable(True)
        #print(idx)    
    #plt.tight_layout()
    #plt.show()


def correct_signal(df, lam, p):
    baseline_fitter = Baseline(x_data=df["Wavenumeber_cm-1"])
    bkg, params = baseline_fitter.asls(df["%T"], lam, p)
    #modpoly(df["%T"], poly_order=1)

    df["%T_baseline"] = df["%T"]-bkg
    nuevo_min, nuevo_max = 20, 100
    y_min = df["%T_baseline"].min()
    y_max = df["%T_baseline"].max()

    df["%T_corrected"] = (df["%T_baseline"] - y_min) / (y_max - y_min) * (nuevo_max - nuevo_min) + nuevo_min
    
    del df["%T_baseline"]
      
    return df
#def smooth_signal(df, window, pol):
 #   df["corrected_%T"] = savgol_filter(df["corrected_%T"], window, pol)
#    return df


