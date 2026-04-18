import requests
import pandas as pd
import schedule
import time
import os
from datetime import datetime

# ========== PARTE 1: LIMPIEZA (de ayer) ==========
def limpiar_datos_ventas(archivo_entrada='ventas_sucias.csv'):
    """Limpia el CSV de ventas (tu script de ayer)"""
    try:
        df = pd.read_csv(archivo_entrada)
        # Limpieza rápida (versión simplificada para hoy)
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df['precio'] = df['precio'].astype(str).str.replace('$', '').astype(float)
        df = df.dropna(subset=['fecha'])
        fecha = datetime.now().strftime("%Y-%m-%d")
        df.to_csv(f'ventas_limpias_{fecha}.csv', index=False)
        print(f"Ventas limpias guardadas: ventas_limpias_{fecha}.csv")
        return df
    except Exception as e:
        print(f"Error limpiando ventas: {e}")
        return None

# ========== PARTE 2: API RICK & MORTY (nuevo) ==========
def descargar_api_rickmorty():
    """Descarga y limpia datos de la API"""
    try:
        print(f"\nDescargando API Rick & Morty...")
        response = requests.get("https://rickandmortyapi.com/api/character")
        response.raise_for_status()
        
        data = response.json()
        df_raw = pd.DataFrame(data['results'])
        
        df_clean = df_raw[['id', 'name', 'status', 'species', 'gender']].copy()
        df_clean['origin'] = df_raw['origin'].apply(lambda x: x.get('name', 'Unknown'))
        df_clean['episode_count'] = df_raw['episode'].apply(len)
        
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo = f'rickmorty_{fecha}.csv'
        df_clean.to_csv(archivo, index=False)
        
        print(f"API guardada: {archivo}")
        print(f"Total personajes: {len(df_clean)}")
        return df_clean
    except Exception as e:
        print(f"Error en API: {e}")
        return None

# ========== PARTE 3: TRABAJO PROGRAMADO ==========
def trabajo_automatico():
    """Ejecuta ambas tareas automáticamente"""
    print("\n" + "="*50)
    print(f"EJECUCIÓN AUTOMÁTICA - {datetime.now()}")
    print("="*50)
    
    # Tarea 1: Limpiar ventas si existe el archivo
    if os.path.exists('ventas_sucias.csv'):
        limpiar_datos_ventas()
    else:
        print("No hay archivo 'ventas_sucias.csv' para limpiar")
    
    # Tarea 2: Descargar API (siempre)
    descargar_api_rickmorty()
    
    print("="*50 + "\n")
    
    # Escribir log
    with open("pipeline_log.txt", "a") as log:
        log.write(f"{datetime.now()} - Pipeline ejecutado\n")

# ========== CONFIGURAR AUTOMATIZACIÓN ==========
# Programa cada día a las 9am
schedule.every().day.at("09:00").do(trabajo_automatico)

# También programa cada 2 minutos para probar AHORA (opcional)
schedule.every(2).minutes.do(trabajo_automatico)

print("PIPELINE AUTOMÁTICO INICIADO")
print("Tareas programadas:")
print("   - Limpieza de ventas (si existe archivo)")
print("   - Descarga de API Rick & Morty")
print("   - Cada 2 minutos (modo prueba)")
print("Presiona Ctrl+C para detener\n")

# Mantener corriendo
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nPipeline detenido")