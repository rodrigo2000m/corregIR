import pandas as pd

#def leer_archivo(ruta):
  #  with open(ruta, 'r', encoding='utf-8') as f:
   #     return f.read()

def read_file(file_path):
    with open(file_path, 'r') as f:
        for line_no, line in enumerate(f, start=1):
            if line.__contains__("##YUNITS=%T"):
                first_line = line_no + 1
            else:
                pass

    df = pd.read_csv(file_path,
                     sep = "\s+",
                     skiprows = first_line,
                     names=["Wavenumeber_cm-1", "%T"]
                     )
    return df



def save_IR_adjusted(df, path_name):
    df.to_csv(path_name, sep="\t", index=False)
