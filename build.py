import os
import platform
import subprocess

def build():
    operative_system = platform.system()

    if operative_system == "Windows":
        command = [
            "pyinstaller",
            "--onefile",
            "--name", "corregIR_win",
            "--distpath", "dist_windows",
            "--workpath", "build_windows",
            "--hidden-import", "PIL._tkinter_finder",
            "main.py"
        ]
    elif operative_system == "Linux":
        command = [         
            "pyinstaller",
            "--onefile",
            "--name", "corregIR_linux",
            "--distpath", "dist_linux",
            "--workpath", "build_linux",
            "--hidden-import", "PIL._tkinter_finder",
            "main.py"
        ]

    else:
        print("Sistema operativo no encontrado: ", opearative_system)
        return

    print("Ejecutando:", "".join(command))

    subprocess.run(command)

if __name__ == "__main__":
    build()





