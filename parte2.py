import pandas as pd
import numpy as np
from scipy.stats import t

df = pd.read_csv("./velocidad_internet_ucu")

#PARTE 1: Filtracion de datos 
df_central = df[df["Edificio"] == "Central"]
df_semprun = df[df["Edificio"] == "Semprún"]

#PARTE 2
#Tamano muestral 
n1 = len(df_central)
n2 = len(df_semprun)

#Media
media1 = df_central["Velocidad Mb/s"].mean()
media2 = df_semprun["Velocidad Mb/s"].mean()

#Desviacion Estandar 
std1 = df_central["Velocidad Mb/s"].std(ddof=1)
std2 = df_semprun["Velocidad Mb/s"].std(ddof=1)

#PARTE 3: formula estadistico t
numerador = media1 - media2
denominador = np.sqrt(((std1**2)/n1) + ((std2**2)/n2))
t_stat = numerador / denominador

#Grados de libertad
s1_sq = std1**2
s2_sq = std2**2

df_num = ((s1_sq / n1) + (s2_sq / n2))**2
df_den = ((s1_sq / n1)**2) / (n1 - 1) + ((s2_sq / n2)**2) / (n2 - 1)
df = df_num / df_den

#PARTE 4: calculo de p-valor
p_value = t.cdf(t_stat, df=df)

print("Media Central:", round(media1, 2))
print("Media Semprún:", round(media2, 2))
print("t =", round(t_stat, 4))
print("Grados de libertad:", round(df, 2))
print("p-valor:", f"{p_value:.25f}")

#PARTE 5: Resultado del test de hipotesis
alpha = 0.05
if p_value < alpha:
    print("Se rechaza H0: la velocidad en Central es significativamente menor que en Semprún.")
else:
    print("No se rechaza H0: no hay evidencia suficiente de que la velocidad en Central sea menor.")
