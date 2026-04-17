import pandas as pd
import schedule
import time
import os
from datetime import datetime

# PASO 1: Crear un archivo CSV sucio de ejemplo (solo para probar)
def crear_datos_sucios():
    """Genera un archivo CSV con datos problemáticos"""
    datos = {
        'fecha': ['2026-04-15', '15/04/2026', '2026-04-15', '', '2026-04-14'],
        'producto': ['Laptop', 'laptop', 'Mouse', 'TECLADO', 'Mouse'],
        'precio': ['$1200', '1250', '35.5', '45', '35.50'],
        'cantidad': [2, 3, 'cinco', 1, '3'],
        'cliente': ['Ana', 'Ana', 'Luis', '', None]
    }
    df = pd.DataFrame(datos)
    df.to_csv('ventas_sucias.csv', index=False)
    print("Archivo 'ventas_sucias.csv' creado con datos sucios")

# Ejecutar para crear el archivo de prueba
crear_datos_sucios()

# ==================
# PASO 2: Función para limpiar los datos
def limpiar_datos(archivo_entrada='ventas_sucias.csv', archivo_salida=f'ventas_limpias_{datetime.now().strftime("%Y-%m-%d")}.csv'):
    """
    Limpia el CSV de ventas y guarda una versión limpia
    """
    print(f"\nIniciando limpieza de {archivo_entrada}...")
    
    # Leer el archivo
    df = pd.read_csv(archivo_entrada)
    print(f"Filas originales: {len(df)}")
    
    # 1. Limpiar columna 'fecha' - convertir a formato estándar
    def limpiar_fecha(fecha_str):
        if pd.isna(fecha_str) or fecha_str == '':
            return None
        try:
            return pd.to_datetime(fecha_str).strftime('%Y-%m-%d')
        except:
            return None
    
    df['fecha'] = df['fecha'].apply(limpiar_fecha)
    
    # 2. Limpiar columna 'precio' - quitar $ y convertir a número
    df['precio'] = df['precio'].astype(str).str.replace('$', '').str.strip()
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    # 3. Limpiar columna 'cantidad' - convertir texto a número
    def convertir_cantidad(val):
        if pd.isna(val):
            return 0
        if isinstance(val, (int, float)):
            return int(val) if val == int(val) else 0
        if val == 'cinco':
            return 5
        try:
            return int(float(val))
        except:
            return 0
    
    df['cantidad'] = df['cantidad'].apply(convertir_cantidad)
    
    # 4. Limpiar columna 'producto' - estandarizar mayúsculas
    df['producto'] = df['producto'].astype(str).str.upper().str.strip()
    df['producto'] = df['producto'].replace(['NAN', 'None', ''], None)
    
    # 5. Limpiar columna 'cliente' - valores nulos a 'DESCONOCIDO'
    df['cliente'] = df['cliente'].fillna('DESCONOCIDO')
    df['cliente'] = df['cliente'].replace(['', 'None'], 'DESCONOCIDO')
    
    # 6. Eliminar filas donde fecha es None (datos inservibles)
    df = df.dropna(subset=['fecha'])
    
    # 7. Eliminar duplicados
    df = df.drop_duplicates()
    
    # 8. Calcular total por fila
    df['total'] = df['precio'] * df['cantidad']
    
    print(f"Filas después de limpieza: {len(df)}")
    print(f"Total de ventas: ${df['total'].sum():.2f}")
    
    # Guardar archivo limpio
    df.to_csv(archivo_salida, index=False)
    print(f"Archivo limpio guardado: {archivo_salida}")
    
    return df

# Probar la función
limpiar_datos()

# =============================
# PASO 2: Programar la limpieza automática cada día a las 9:00 AM 
def trabajo_programado():
    """
    Función que se ejecutará automáticamente cada día
    """
    print("\n" + "="*50)
    print(f"EJECUCIÓN PROGRAMADA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Verificar si existe archivo sucio
    if os.path.exists('ventas_sucias.csv'):
        limpiar_datos()
        print("📊 Resumen de ventas limpias:")
        df = pd.read_csv('ventas_limpias.csv')
        print(f"   - Total de transacciones: {len(df)}")
        print(f"   - Ingreso total: ${df['total'].sum():.2f}")
        print(f"   - Producto más vendido: {df['producto'].mode()[0] if not df['producto'].mode().empty else 'N/A'}")
    else:
        print("⚠️ No se encontró archivo 'ventas_sucias.csv' para limpiar")
    
    print("="*50 + "\n")

# Programar la tarea
schedule.every().day.at("09:00").do(trabajo_programado)

# También probamos cada 30 segundos para verlo funcionar (opcional)
# schedule.every(30).seconds.do(trabajo_programado)

print("SISTEMA DE AUTOMATIZACIÓN INICIADO")
print("Tarea programada: Limpieza diaria a las 9:00 AM")
print("Presiona Ctrl+C para detener\n")

# Mantener el programa corriendo
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSistema detenido por el usuario")
    
# ============================= 
# Escriba un log de cada ejecución en un archivo limpieza_log.txt
with open("limpieza_log.txt", "a") as f:
    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ejecución de limpieza automática\n")
    