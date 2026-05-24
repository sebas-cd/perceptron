import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🕹️ Desafío del Perceptrón Manual")

# 1. Configuración de la Tabla de Verdad (Entradas y Etiquetas)
st.sidebar.header("Configuración del Problema")
puntos = [(0,0), (0,1), (1,0), (1,1)]
etiquetas = {}

for x1, x2 in puntos:
    etiquetas[(x1, x2)] = st.sidebar.selectbox(
        f"Etiqueta para ({x1}, {x2})", 
        options=[-1, 1], 
        index=0 if (x1, x2) != (1,1) else 1 # Defecto: Compuerta AND
    )

# 2. Perillas de Control (Sliders)
st.header("Ajuste del Perceptrón")
w1 = st.slider("Peso w₁", -2.0, 2.0, 0.0, 0.1)
w2 = st.slider("Peso w₂", -2.0, 2.0, 0.0, 0.1)
bias = st.slider("Bias (Sesgo)", -2.0, 2.0, 0.0, 0.1)

# 3. Cálculos del Perceptrón
correctos = 0
tabla_datos = []

for (x1, x2), y_deseada in etiquetas.items():
    suma_ponderada = (x1 * w1) + (x2 * w2) + bias
    y_predicha = 1 if suma_ponderada >= 0 else -1
    es_correcto = (y_predicha == y_deseada)
    if es_correcto:
        correctos += 1
    
    tabla_datos.append([x1, x2, y_deseada, round(suma_ponderada, 2), y_predicha, "✅" if es_correcto else "❌"])

# 4. Renderizar Métricas y Tabla
st.metric(label="Patrones Clasificados Correctamente", value=f"{correctos} / 4")
st.table(tabla_datos) # Muestra las columnas correspondientes

# 5. Graficar Frontera de Decisión con Matplotlib
fig, ax = plt.subplots()
# (Aquí agregas la lógica para graficar los puntos y la recta z=0)
# Tip: Si w2 es diferente de 0, trazas una línea usando x2 = (-w1*x1 - bias) / w2