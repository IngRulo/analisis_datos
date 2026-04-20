import requests
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constantes
API_URL = "http://universities.hipolabs.com/search"
COUNTRY = "mexico"

# === Normaliza los nombres de las columnas ===
def limpiar_columnas(df):
    df.columns = (df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False).str.replace('.', '', regex=False))
    return df

# === Obtenemos datos de la API y devolvemos ===
def descargar_datos_universidades(pais):
    params = {"country": pais}
    try:
        # Solicitamos datos a la API
        logging.info(f"Solicitando datos para: {pais}...")
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        # Convertimos la respuesta JSON a DataFrame
        data = response.json()
        # Verificamos que la API devolvió datos
        if not data:
            logging.warning("La API no devolvió resultados.")
            return None
        # Creamos DataFrame y limpiamos columnas
        df = pd.DataFrame(data)
        df = limpiar_columnas(df)
        
        # Usamos 'subset' solo si las columnas existen para evitar errores
        columnas_criticas = [col for col in ['name', 'domains'] if col in df.columns]
        df = df.dropna(subset=columnas_criticas)
        
        # Si 'domains' es una lista, la convertimos a string para mejor legibilidad
        if 'domains' in df.columns:
            df['domains'] = df['domains'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # Devolvemos el DataFrame limpio
        return df
    # Manejamos errores de conexión y otros errores inesperados
    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión: {e}")
    # Capturamos cualquier otro error inesperado para evitar que el programa se caiga
    except Exception as e:
        logging.error(f"Error inesperado al procesar datos: {e}")
    return None

# === Guarda el DataFrame en un archivo CSV ===
def guardar_csv(df, prefijo="universidades"):
    # Verificamos que el DataFrame no esté vacío antes de intentar guardar
    if df is None or df.empty:
        logging.error("No hay datos para guardar.")
        return
    # Generamos el nombre del archivo con la fecha actual
    fecha = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"{prefijo}_{fecha}.csv"
    # Aseguramos que el directorio de salida exista
    try:
        # Usamos utf-8-sig para que Excel reconozca tildes y Ñs automáticamente
        df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
        logging.info(f"Archivo guardado exitosamente: {nombre_archivo}")
        logging.info(f"Total de registros procesados: {len(df)}")
    except Exception as e:
        logging.error(f"Error al guardar el archivo: {e}")

# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    df_universidades = descargar_datos_universidades(COUNTRY)
    guardar_csv(df_universidades)