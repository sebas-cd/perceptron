import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página de Streamlit
st.set_page_config(page_title="Simulador de Perceptrón", layout="wide")

st.title("Perceptrón")
st.write(
    "Ajusta los pesos y el bias manualmente para intentar separar los puntos "
    "según las etiquetas que definas en el menú lateral."
)

# -------------------------------------------------------------------------
# 1. ENTRADAS: Configuración de la Tabla de Verdad en la barra lateral
# -------------------------------------------------------------------------
st.sidebar.header("⚙️ Configuración del Problema")
st.sidebar.write("Define la clase objetivo para cada combinación de entrada:")

puntos = [(0, 0), (0, 1), (1, 0), (1, 1)]
etiquetas_deseadas = {}

for x1, x2 in puntos:
    # Por defecto configuramos una compuerta AND ((1,1) es 1, el resto es -1)
    defecto_index = 1 if (x1 == 1 and x2 == 1) else 0
    
    etiquetas_deseadas[(x1, x2)] = st.sidebar.selectbox(
        f"Etiqueta para ({x1}, {x2})",
        options=[-1, 1],
        index=defecto_index,
        key=f"target_{x1}_{x2}"
    )

# -------------------------------------------------------------------------
# 2. ENTRADAS: Controles (Sliders) para los Pesos y el Bias
# -------------------------------------------------------------------------
st.subheader("🎛️ Perillas de Ajuste (Pesos y Bias)")
col_w1, col_w2, col_bias = st.columns(3)

with col_w1:
    w1 = st.slider("Peso w₁", min_value=-2.0, max_value=2.0, value=0.5, step=0.1)
with col_w2:
    w2 = st.slider("Peso w₂", min_value=-2.0, max_value=2.0, value=0.5, step=0.1)
with col_bias:
    bias = st.slider("Bias (b)", min_value=-2.0, max_value=2.0, value=-0.7, step=0.1)

# -------------------------------------------------------------------------
# 3. LÓGICA: Evaluación del Perceptrón y cálculo de métricas
# -------------------------------------------------------------------------
aciertos = 0
filas_tabla = []

for (x1, x2), y_deseada in etiquetas_deseadas.items():
    # Cálculo de la suma ponderada (z)
    suma_ponderada = (x1 * w1) + (x2 * w2) + bias
    
    # Función de activación de escalón (-1 o 1)
    y_predicha = 1 if suma_ponderada >= 0 else -1
    
    # Verificar si la clasificación es correcta
    es_correcto = (y_predicha == y_deseada)
    if es_correcto:
        aciertos += 1
        
    filas_tabla.append({
        "Entrada X₁": x1,
        "Entrada X₂": x2,
        "Clase Deseada (y)": y_deseada,
        "Suma Ponderada (z)": round(suma_ponderada, 2),
        "Salida Perceptrón (ŷ)": y_predicha,
        "Estado": "✅ Correcto" if es_correcto else "❌ Incorrecto"
    })

# -------------------------------------------------------------------------
# 4. VISUALIZACIÓN: Renderizado de Resultados y Gráfica
# -------------------------------------------------------------------------
col_grafica, col_tabla = st.columns([3, 2])

with col_tabla:
    st.subheader("📊 Resultados de Clasificación")
    st.metric(label="Patrones Clasificados Correctamente", value=f"{aciertos} / 4")
    st.table(filas_tabla)

with col_grafica:
    st.subheader("📐 Frontera de Decisión en 2D")
    
    # Crear la figura de Matplotlib
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Graficar los puntos del dataset
    for (x1, x2), y_deseada in etiquetas_deseadas.items():
        color = "#FF7F0E" if y_deseada == 1 else "#1F77B4"
        marcador = "o" if y_deseada == 1 else "s"
        ax.scatter(x1, x2, color=color, s=200, marker=marcador, edgecolor='black', zorder=5, 
                   label=f"Clase {y_deseada}" if f"Clase {y_deseada}" not in ax.get_legend_handles_labels()[1] else "")
    
    # ---- LÓGICA CRÍTICA: Graficar la frontera de decisión (w1*x1 + w2*x2 + b = 0) ----
    x1_valores = np.linspace(-0.5, 1.5, 100)
    
    if w2 != 0:
        # Caso estándar: se puede despejar x2 en función de x1
        # x2 = (-w1*x1 - b) / w2
        x2_valores = (-w1 * x1_valores - bias) / w2
        ax.plot(x1_valores, x2_valores, color="red", linestyle="--", linewidth=2, label="Frontera de decisión")
    else:
        # Caso especial: w2 es CERO. La línea es completamente vertical
        if w1 != 0:
            # Despejando: x1 = -b / w1
            x1_vertical = -bias / w1
            ax.axvline(x=x1_vertical, color="red", linestyle="--", linewidth=2, label="Frontera de decisión")
        else:
            # Si tanto w1 como w2 son cero, no hay línea (plano indeterminado)
            st.warning("⚠️ Los pesos w₁ y w₂ son cero. El perceptrón no puede definir una línea.")

    # Colorear las regiones de decisión de fondo (Opcional, mejora visual)
    # Crea una rejilla en el plano para pintar dónde predice +1 (rojo claro) y -1 (azul claro)
    xx, yy = np.meshgrid(np.linspace(-0.5, 1.5, 200), np.linspace(-0.5, 1.5, 200))
    Z = (xx * w1) + (yy * w2) + bias
    Z_activado = np.where(Z >= 0, 1, -1)
    ax.contourf(xx, yy, Z_activado, levels=[-2, 0, 2], colors=['#1F77B4', '#FF7F0E'], alpha=0.15, zorder=1)

    # Configuración de límites y estilo del plano cartesiano
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel("Entrada X₁", fontsize=12)
    ax.set_ylabel("Entrada X₂", fontsize=12)
    ax.axhline(0, color='gray', linewidth=0.8, linestyle=":")
    ax.axvline(0, color='gray', linewidth=0.8, linestyle=":")
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.legend(loc="upper left")
    
    # Renderizar la gráfica en Streamlit
    st.pyplot(fig)
