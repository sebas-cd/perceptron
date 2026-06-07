import streamlit as st

st.set_page_config(page_title="Clasificador de Imágenes Manual", layout="wide")

st.title("Máquina de Puntuación de Imágenes Binarias (Matriz 3x3)")
st.write(
    "Ajusta manualmente los pesos de la rejilla para entrenar a tu máquina. "
    "El objetivo es maximizar el puntaje de las letras 'T' y penalizar las figuras incorrectas."
)

# -------------------------------------------------------------------------
# 1. IMÁGENES BINARIAS (3 Tipo T y 3 que NO son T)
# -------------------------------------------------------------------------
imagenes = {
    # --- 3 Imágenes Tipo T ---
    "Letra T Estándar (Tipo T)": [1, 1, 1, 
                                  0, 1, 0, 
                                  0, 1, 0],
    
    "Letra T Ancha / Techo Largo (Tipo T)": [1, 1, 1, 
                                             1, 1, 1, 
                                             0, 1, 0],
                                             
    "Letra T Corta (Tipo T)": [1, 1, 1, 
                               0, 1, 0, 
                               0, 0, 0],
                               
    # --- 3 Imágenes que NO son T ---
    "Cruz / Signo Más (No es T)": [0, 1, 0, 
                                   1, 1, 1, 
                                   0, 1, 0],
                                   
    "Línea Horizontal (No es T)": [1, 1, 1, 
                                   0, 0, 0, 
                                   0, 0, 0],
                                  
    "Cuadrado Hueco (No es T)": [1, 1, 1, 
                                 1, 0, 1, 
                                 1, 1, 1]
}

# -------------------------------------------------------------------------
# 2. SISTEMA DE PESOS AJUSTABLES (Preconfigurado con la matriz de la guía)
# -------------------------------------------------------------------------
st.header("Configuración de las Perillas (Pesos por Píxel)")
st.write("Cada celda representa el impacto que tendrá ese píxel si se encuentra activo (1).")

# Matriz sugerida en la guía para inicializar
pesos_iniciales = [
    2.0,  2.0,  2.0,
   -1.0,  3.0, -1.0,
   -1.0,  3.0, -1.0
]

pesos = [0.0] * 9
columnas_ui = [st.columns(3), st.columns(3), st.columns(3)]

idx = 0
for f in range(3):
    for c in range(3):
        with columnas_ui[f][c]:
            pesos[idx] = st.slider(
                f"Celda [{f+1},{c+1}]", 
                min_value=-5.0, 
                max_value=5.0, 
                value=pesos_iniciales[idx], 
                step=0.5,
                key=f"w_{idx}"
            )
        idx += 1

# Umbral ajustable para decidir si el puntaje califica como una T
st.markdown("---")
threshold = st.slider("Umbral de Aceptación (Threshold)", min_value=-5.0, max_value=15.0, value=5.0, step=0.5)

# -------------------------------------------------------------------------
# 3. CÁLCULO DE PUNTAJE TOTAL Y VISUALIZACIÓN DINÁMICA
# -------------------------------------------------------------------------
st.markdown("---")
st.header("Evaluación de la Imagen Seleccionada")

col_izq, col_der = st.columns([2, 3])

with col_izq:
    opcion = st.selectbox("Selecciona una imagen del banco de datos:", list(imagenes.keys()))
    img_seleccionada = imagenes[opcion]
    
    st.write("**Visualización de la Matriz de Pútbol (3x3):**")
    
    # --- SOLUCIÓN VISUAL: Renderizar la matriz como un mapa de calor/píxeles ---
    import matplotlib.pyplot as plt
    
    # Convertimos la lista de 9 elementos de nuevo a una matriz de 3x3
    matriz_3x3 = [
        img_seleccionada[0:3],
        img_seleccionada[3:6],
        img_seleccionada[6:9]
    ]
    
    fig, ax = plt.subplots(figsize=(3, 3))
    # cmap="binary" pinta el 1 como negro y el 0 como blanco
    ax.imshow(matriz_3x3, cmap="binary", vmin=0, vmax=1)
    
    # Dibujar líneas de rejilla internas para separar los píxeles
    ax.set_xticks([0.5, 1.5], minor=True)
    ax.set_yticks([0.5, 1.5], minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=1.5)
    
    # Quitar los ejes numéricos para que parezca una pantalla limpia
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Forzar que los bordes del gráfico se vean limpios
    for spine in ax.spines.values():
        spine.set_edgecolor('gray')
        spine.set_linewidth(1.5)
        
    st.pyplot(fig)

with col_der:
    st.write("**Desglose Matemática Interna:**")
    
    # Operación matemática pura: y = Σ(wᵢxᵢ)
    puntaje_total = 0.0
    operaciones_texto = []
    
    for i in range(9):
        pixel = img_seleccionada[i]
        peso = pesos[i]
        producto = pixel * peso
        puntaje_total += producto
        if pixel == 1:
            operaciones_texto.append(f"Píxel {i+1} encendido (1) × Peso ({peso}) = {producto}")
            
    # Mostrar el paso a paso matemático al usuario
    for operacion in operaciones_texto:
        st.caption(operacion)
        
    st.markdown(f"### **Puntaje Total Calculado ($y$):** `{round(puntaje_total, 2)}`")
    
    # Clasificación basada en el Umbral
    if puntaje_total >= threshold:
        st.success(f"**Resultado:** CLASIFICADO COMO LETRA T (Puntaje ≥ {threshold})")
    else:
        st.error(f"**Resultado:** RECHAZADO (Puntaje < {threshold})")

# -------------------------------------------------------------------------
# 4. TABLA GLOBAL DE RENDIMIENTO
# -------------------------------------------------------------------------
st.markdown("---")
st.header("Cuadro de Rendimiento General")

tabla_resumen = []
for nombre, img in imagenes.items():
    score = sum(img[i] * pesos[i] for i in range(9))
    es_t_segun_modelo = score >= threshold
    es_t_real = "Tipo T" in nombre
    
    # Evaluar si la predicción manual coincide con la etiqueta real
    evaluacion = "Correcto" if es_t_segun_modelo == es_t_real else "Error de Clasificación"
    
    tabla_resumen.append({
        "Estructura de Imagen": nombre,
        "Puntaje Total ($y$)": round(score, 2),
        "Predicción": "Es una T" if es_t_segun_modelo else "No es una T",
        "Diagnóstico": evaluacion
    })

st.table(tabla_resumen)
