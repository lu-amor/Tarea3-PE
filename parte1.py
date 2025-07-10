from math import pow
import pandas as pd
import numpy as np
from scipy.stats import chi2

#Carga de datos
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
data = load_data('muestra_ech.csv')

# Parte 1: Ingreso per cápita
data['ingreso_per_capita'] = data['ingreso'] / data['personas_hogar']

# Parte 2: Clasificación de hogares por quintiles
percentiles = np.percentile(data['ingreso_per_capita'], [20, 40, 60, 80])
def clasificar_hogares(ingreso_per_capita):
    if ingreso_per_capita <= percentiles[0]:
        return 1
    elif ingreso_per_capita <= percentiles[1]:
        return 2
    elif ingreso_per_capita <= percentiles[2]:
        return 3
    elif ingreso_per_capita <= percentiles[3]:
        return 4
    else:
        return 5

data['quintil'] = data['ingreso_per_capita'].apply(clasificar_hogares)

# Parte 3: Hogares que pertenecen al quintil superior
hogares_quintil_superior = data[data["quintil"] == 5]

""" print("Hogares que pertenecen al quintil superior:")
print(hogares_quintil_superior) """
hogares_quintil_superior.to_csv("quintil_superior.csv", index=False) # Esto lo guarda en un archivo CSV

# Parte 4: Tabla de frecuencias observadas por departamento
frecuencias_observadas = hogares_quintil_superior['departamento'].value_counts().sort_index()

tabla_frecuencias = frecuencias_observadas.reset_index()
tabla_frecuencias.columns = ['Departamento', 'Frecuencia observada']

print("Frecuencias observadas por departamento (quintil superior):")
print(tabla_frecuencias.to_string(index=False))

# Parte 5: Tabla de frecuencias esperadas bajo hipótesis de distribución uniforme
total_hogares_q5 = len(hogares_quintil_superior)
frecuencia_esperada = total_hogares_q5 / hogares_quintil_superior['departamento'].nunique()
print(f"Frecuencia esperada: {frecuencia_esperada}")

# Parte 6: Cálculo de estadístico chi-cuadrado
chi_cuadrado = sum((observado - frecuencia_esperada) ** 2 / frecuencia_esperada for observado in frecuencias_observadas)
print(f"Estadístico chi-cuadrado: {chi_cuadrado}")

# Parte 7: Determinar si se rechaza la hipótesis nula
alfa = 0.05
grados_libertad = hogares_quintil_superior['departamento'].nunique() - 1
valor_critico = chi2.ppf(1 - alfa, grados_libertad)

print(f"Valor crítico para alfa={alfa} y {grados_libertad} grados de libertad: {valor_critico}")
if chi_cuadrado > valor_critico:
    print("Se rechaza H0.")
else:
    print("No se rechaza H0.")