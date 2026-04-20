import pandas as pd

# Nombre archivo
nombre_archivo = 'universidades_2026-04-20.csv'
# Leemos archivo
univ_df = pd.read_csv(nombre_archivo)
# Mostramos cuandos datos son nulos
print(univ_df.isnull().sum())
# Cambiamos el valor nulo por "Desconocido"
univ_df['state-province'] = univ_df['state-province'].fillna('Desconocido')

# Mostramos los primeros 5 registros
print(univ_df.head())

# Guardamos el DataFrame limpio en un nuevo archivo CSV
univ_df.to_csv('universidades_limpias.csv', index=False, encoding='utf-8-sig')