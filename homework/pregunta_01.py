"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd 
import csv
import os
import glob

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    (['Unnamed: 0', 'sexo', 'tipo_de_emprendimiento', 'idea_negocio',
       'barrio', 'estrato', 'comuna_ciudadano', 'fecha_de_beneficio',
       'monto_del_credito', 'línea_credito'],
      dtype='object')
      (10920, 10)
      df[df.duplicated(
          subset=["client_id", "name"],
          keep="last",
      )]
    """
    df = pd.read_csv("./files/input/solicitudes_de_credito.csv",
                     sep=";", index_col=0)
    
    df = df.copy()
    #Limpieza de datos
    
    df["sexo"] = df["sexo"].str.lower()
    
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()
    
    fechas_formato_ano_primero = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    filas_con_error = fechas_formato_ano_primero.isna()
    fechas_formato_dia_primero = pd.to_datetime(df.loc[filas_con_error, "fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fechas_formato_ano_primero.loc[filas_con_error] = fechas_formato_dia_primero
    df["fecha_de_beneficio"] = fechas_formato_ano_primero
    
    
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(".00", "")
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(r"[,. $]", "", regex=True)
    
    
    columnas = ["idea_negocio", "barrio", "línea_credito"]
    for columna in columnas:
        if columna in df.columns:
            df[columna] = df[columna].str.lower().str.replace(r"[-_]", " ", regex=True)
    
    df = df.dropna()
    df = df.drop_duplicates()
    
    output_directory = "./files/output"
    
    if os.path.exists(output_directory):
        files = glob.glob(f"{output_directory}/*")
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)
        
    os.mkdir(output_directory)
    df.to_csv(os.path.join(output_directory, "solicitudes_de_credito.csv"), sep=";", index=False)
    
    
    
if __name__ == "__main__":
    pregunta_01()
