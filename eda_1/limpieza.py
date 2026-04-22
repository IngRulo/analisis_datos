# Librerias
import pandas as pd
import numpy as np
# Cargamos dataset
ventas_df = pd.read_csv('ventas_sucias.csv', sep=',', encoding='utf-8')
# Información general del dataset
print(ventas_df.info())
# Contamos filas y columnas
print("="*50)
print(f"El dataset tiene {ventas_df.shape[0]} filas y {ventas_df.shape[1]} columnas.")
# Verificamos valores nulos
print("="*50)
print(ventas_df.isnull().sum())
# Transformamos la columnas a su tipo de datos
ventas_df['fecha'] = pd.to_datetime(ventas_df['fecha'], format='%d/%m/%y', errors='coerce')
ventas_df['ventas'] = pd.to_numeric(ventas_df['ventas'], errors='coerce')
ventas_df['beneficio'] = pd.to_numeric(ventas_df['beneficio'], errors='coerce')
ventas_df['descuento'] = pd.to_numeric(ventas_df['descuento'], errors='coerce')
# Eliminamos la columna sin nombre

print("=== Valores negativos ===")
print(f"Ventas negativas: {len(ventas_df[ventas_df['ventas'] < 0])}")
print(f"Beneficio negativo: {len(ventas_df[ventas_df['beneficio'] < 0])}")
print(f"Descuento negativo: {len(ventas_df[ventas_df['descuento'] < 0])}")
print("\n=== Valores nulos ===")
print(ventas_df[['ventas', 'beneficio', 'descuento']].isnull().sum())

print("\n=== Filas con beneficio negativo ===")
print(ventas_df[ventas_df['beneficio'] < 0][['id_venta','descuento']])
