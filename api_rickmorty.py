import requests
import pandas as pd
from datetime import datetime

# 1. Conectar a la API (sin registro, gratis)
url = "https://rickandmortyapi.com/api/character"
response = requests.get(url)

print(f"Código de respuesta: {response.status_code}")  # 200 = éxito

# 2. Ver los datos (primeros 5 personajes)
data = response.json()
print(f"\nTotal de personajes: {data['info']['count']}")
print(f"Primer personaje: {data['results'][0]['name']} - {data['results'][0]['species']}")

# 3. Convertir resultados a DataFrame
df_raw = pd.DataFrame(data['results'])

print(f"\nColumnas disponibles: {df_raw.columns.tolist()}")
print(f"Forma del DataFrame: {df_raw.shape}")

# 4. Seleccionar columnas relevantes (las que importan para análisis)
columnas_interes = ['id', 'name', 'status', 'species', 'type', 'gender', 'origin', 'location', 'episode']
df_clean = df_raw[columnas_interes].copy()

# 5. Limpiar columnas anidadas (origin y location son diccionarios)
df_clean['origin_name'] = df_clean['origin'].apply(lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown')
df_clean['location_name'] = df_clean['location'].apply(lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown')

# 6. Contar cuántos episodios tiene cada personaje
df_clean['episode_count'] = df_clean['episode'].apply(len)

# 7. Eliminar columnas originales anidadas
df_clean = df_clean.drop(['origin', 'location', 'episode'], axis=1)

print(f"\nDataFrame limpio - Primeros 5 personajes:")
print(df_clean.head())

# 8. Función completa para descargar y limpiar datos
def descargar_personajes_rickmorty():
    """
    Descarga personajes de Rick & Morty API, limpia y guarda CSV con fecha
    """
    try:
        print(f"\nDescargando datos de API...")
        response = requests.get("https://rickandmortyapi.com/api/character")
        response.raise_for_status()  # Lanza error si hay problema
        
        data = response.json()
        df_raw = pd.DataFrame(data['results'])
        
        # Limpiar
        df_clean = df_raw[['id', 'name', 'status', 'species', 'gender']].copy()
        df_clean['origin'] = df_raw['origin'].apply(lambda x: x.get('name', 'Unknown'))
        df_clean['location'] = df_raw['location'].apply(lambda x: x.get('name', 'Unknown'))
        df_clean['episode_count'] = df_raw['episode'].apply(len)
        
        # Guardar con fecha
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo = f'rickmorty_personajes_{fecha}.csv'
        df_clean.to_csv(archivo, index=False)
        
        print(f"Datos guardados: {archivo}")
        print(f"Total personajes: {len(df_clean)}")
        print(f"   - Vivos: {df_clean[df_clean['status']=='Alive'].shape[0]}")
        print(f"   - Muertos: {df_clean[df_clean['status']=='Dead'].shape[0]}")
        
        return df_clean
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# 9. Ejecutar la función
df_resultado = descargar_personajes_rickmorty()

