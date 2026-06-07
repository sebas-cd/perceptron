import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Clasificador Automático 3x3", layout="wide")

st.title("🎯 Clasificador Automático de Imágenes (Detector de Letras T)")
st.write(
    "¡Bienvenido a la fase de decisión! Ajusta los pesos y el umbral (*threshold*) "
    "para que la máquina clasifique automáticamente y de forma perfecta todas las imágenes."
)

# -------------------------------------------------------------------------
# 1. BASE DE DATOS DE EVALUACIÓN (Ejemplos Positivos y Negativos)
# -------------------------------------------------------------------------
# Estructuramos el banco con etiquetas reales para que el sistema calcule los errores
imagenes_banco = {
    # --- Ejemplos Positivos (Son una T) ---
    "Letra T Estándar": {"pixeles": [1, 1, 1, 0, 1, 0, 0, 1, 0], "es_t_real": True},
    "Letra T Techo Grueso": {"pixeles": [1, 1, 1, 1, 1, 1, 0, 1, 0], "es_t_real": True},
    "Letra T Corta": {"pixeles": [1, 1, 1, 0, 1, 0, 0, 0, 0], "es_t_real": True},
    
    # --- Ejemplos Negativos (NO son una T) ---
    "Signo Más / Cruz": {"pixeles": [0, 1, 0, 1, 1, 1, 0, 1, 0], "es_t_real": False},
    "Línea Horizontal Alta": {"pixeles": [1, 1, 1, 0, 0, 0, 0, 0, 0], "es_t_real": False},
    "Cuadrado Hueco": {"pixeles": [1, 1, 1, 1, 0, 1, 1, 1, 1], "es_t_real": False}
}

# -------------------------------------------------------------------------
# 2. INTERFAZ DE CONTROL: Ajuste de Parámetros Dinámicos
# -------------------------------------------------------------------------
st.header("🎛️ Panel de Control de Parámetros")
col_sliders, col_threshold = st.columns([2, 1])

with col_sliders:
    st.write("**Ajuste de Pesos ($w_i$) por Píxel:**")
    # Inicializamos con la matriz sugerida en la etapa anterior
    pesos_iniciales = [2.0, 2.0, 2.0, -1.0, 3.0, -1.0, -1.0, 3.0, -1.0]
    pesos = [0.0] * 9
    
    # Renderizado en rejilla 3x3 para que el usuario sepa qué pixel modifica
    columnas_ui = [st.columns(3), st.columns(3), st.columns(3)]
    idx = 0
    for f in range(3):
        for c in range(3):
            with columnas_ui[f][c]:
                pesos[idx] = st.slider(
                    f"Peso Píxel [{f+1},{c+1}]", 
                    min_value=-5.0, 
                    max_value=5.0, 
                    value=pesos_iniciales[idx], 
                    step=0.5,
                    key=f"w_{idx}"
                )
            idx += 1

with col_threshold:
    st.write("**Mecanismo de Decisión:**")
    # Control para modificar el límite divisorio de la máquina
    threshold = st.number_input(
        "🎯 Umbral de Clasificación (Threshold)", 
        min_value=-10.0, 
        max_value=20.0, 
        value=5.0, 
        step=0.5
    )
    st.caption(
        "Si el puntaje de la imagen supera este valor, la máquina dirá de forma "
        "autónoma 'Es una T'. De lo contrario, dirá 'No es una T'."
    )

# -------------------------------------------------------------------------
# 3. INTERFAZ DE PRUEBA: Evaluación de Ejemplo Individual
# -------------------------------------------------------------------------
st.markdown("---")
st.header("🖼️ Banco de Pruebas Individual")

col_img, col_calculo = st.columns([1, 2])

with col_img:
    opcion = st.selectbox("Selecciona una imagen para testear:", list(imagenes_banco.keys()))
    datos_img = imagenes_banco[opcion]
    pixeles_img = datos_img["pixeles"]
    
    # Dibujar la matriz en blanco y negro de 3x3 usando Matplotlib
    matriz_3x3 = [pixeles_img[0:3], pixeles_img[3:6], pixeles_img[6:9]]
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.imshow(matriz_3x3, cmap="binary", vmin=0, vmax=1)
    
    # Líneas divisorias de la cuadrícula
    ax.set_xticks([0.5, 1.5], minor=True)
    ax.set_yticks([0.5, 1.5], minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

with col_calculo:
    # Lógica del modelo: y = Σ(w_i * x_i)
    score = 0.0
    for i in range(9):
        score += pixeles_img[i] * pesos[i]
        
    st.markdown(f"### **Puntaje Calculado (Score):** `{round(score, 2)}`")
    st.markdown(f"### **Umbral Establecido (Threshold):** `{round(threshold, 2)}`")
    
    # ---- REGLA DE CLASIFICACIÓN MÍNIMA SOLICITADA ----
    if score >= threshold:
        decision = "Es una T"
        st.success(f"🤖 **Decisión de la máquina:** ¡{decision}!")
    else:
        decision = "No es una T"
        st.error(f"🤖 **Decisión de la máquina:** ¡{decision}!")
        
    # Validar si la máquina acertó con la realidad humana
    es_correcto = (decision == "Es una T" and datos_img["es_t_real"]) or (decision == "No es una T" and not datos_img["es_t_real"])
    if es_correcto:
        st.info("✨ **Diagnóstico:** Clasificación Correcta (El modelo coincide con la realidad).")
    else:
        st.warning("🚨 **Diagnóstico:** Error de Clasificación (Falso Positivo o Falso Negativo).")

# -------------------------------------------------------------------------
# 4. SISTEMA DE EVALUACIÓN COLECTIVA Y DETECCIÓN DE ERRORES
# -------------------------------------------------------------------------
st.markdown("---")
st.header("📊 Matriz de Evaluación Global y Detección de Errores")
st.write("Monitorea el comportamiento del clasificador simultáneamente ante todos los ejemplos:")

tabla_global = []
aciertos_totales = 0

for nombre, datos in imagenes_banco.items():
    # Cálculo automático
    puntaje_img = sum(datos["pixeles"][i] * pesos[i] for i in range(9))
    
    # Decisión automática
    prediccion = "Es una T" if puntaje_img >= threshold else "No es una T"
    realidad = "Es una T" if datos["es_t_real"] else "No es una T"
    
    # Diagnóstico del error
    if prediccion == realidad:
        diagnostico = "✅ Éxito"
        aciertos_totales += 1
    else:
        diagnostico = "❌ ERROR"
        
    tabla_global.append({
        "Estructura Visual": nombre,
        "Clase Real": realidad,
        "Puntaje Obtenido": round(puntaje_img, 2),
        "Decisión Automática": prediccion,
        "Estado del Clasificador": diagnostico
    })

# Métricas de rendimiento de la máquina
st.metric(label="Precisión General del Clasificador", value=f"{aciertos_totales} / {len(imagenes_banco)} Correctos")
st.table(tabla_global)
