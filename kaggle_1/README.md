# Titanic survival analysis

Análisis exploratorio de los datos del *Titanic* para identificar patrones de supervivencia.

## 📊 Dataset:
- **Fuente:** Kaggle - Titanic: Machine Learning from Disaster
- **Registros:** 891 pasajeros
- **Variables:** 12 columnas

## 🛠️ Tecnologías:
- Python (Pandas, NumPy)
- Visualización: Matplotlib, Seaborn

## 🔍 Proceso:
1. **Limpieza:** Imputación de nulos (mediana en Age, moda en Embarked), creación de `has_cabin`
2. **EDA:** 4 gráficos clave + matriz de correlación
3. **KPIs:** Tasas de supervivencia por sexo, clase y global

## 📈 Resultados clave:
| Métrica | Valor |
|---------|-------|
| Tasa global | 38.38% |
| Mujeres | 74.20% |
| Hombres | 18.89% |
| Primera clase | 62.96% |
| Tercera clase | 24.24% |
| Mujeres 1ra clase | ~97% |

## 💡 Conclusiones:
- El **sexo** y la **clase** son los factores más determinantes
- Perfil de mayor riesgo: **hombres de tercera clase**
- Perfil de menor riesgo: **mujeres de primera clase**

## 📁 Archivos:
- `titanic.ipynb` - Notebook completo

## 👤 Autor
[Raúl Tovar] – [GitHub]([https://github.com/tu-usuario](https://github.com/RulTovar/analisis_datos))

---
