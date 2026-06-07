import streamlit as st

st.set_page_config(page_title="Detector de T Manual", layout="wide")

st.title("👁️ Operación T: Clasificador de Imágenes Manual")
st.write(
    "Ajusta los 9 pesos de la matriz para lograr que las imágenes con forma de 'T' "
    "obtengan puntajes altos, y las formas incorrectas obtengan puntajes bajos."
)

# -------------------------------------------------------------------------
# 1. BASE DE DATOS DE IMÁGENES (Matrices de 3x3 representadas como listas de 9 elementos)
# -------------------------------------------------------------------------
patrones = {
    "Letra T Real (Perfecta)": [1, 1, 1, 
                                0, 1, 0, 
                                0, 1, 0],
    
    "Cruz / Signo Más (+)":    [0, 1, 0, 
                                1, 1, 1, 
                                0, 1, 0],
                                
    "Línea Horizontal Alta":   [1, 1, 1, 
                                0, 0, 0, 
                                0, 0, 0],
                                
    "Letra T Desplazada Izq.": [1, 1, 0, 
                                1, 0, 0, 
                                1, 0, 0],
                                
    "Bloque Sólido Completo":  [1, 1, 1, 
                                1, 1, 1, 
                                1, 1, 1]
}

# -------------------------------------------------------------------------
# 2. INTERFAZ: Configuración de los 9 Pesos (Matriz Interactiva)
# -------------------------------------------------------------------------
st.header("🎛️ Matriz de Pesos Neuronales ($w_i$)")
st.write("Modifica el peso de cada celda. Los píxeles activos (1) se multiplicarán por estos valores.")

# Creamos una cuadrícula visual de 3x3 sliders usando las columnas de Streamlit
pesos = [0.0] * 9
filas_ui = [st.columns(3), st.columns(3), st.columns(3)]

idx = 0
for f in range(3):
    for c in range(3):
        with filas_ui[f][c]:
            # Ponemos un valor inicial por defecto de 0.0 para que el alumno experimente
            pesos[idx] = st.slider(
                f"Peso Celda [{f+1},{c+1}]", 
                min_value=-5.0, 
                max_value=5.0, 
                value=0.0, 
                step=0.5,
                key=f"w_{idx}"
            )
        idx += 1

# Umbral de decisión (Threshold) para la clasificación final
st.markdown("---")
threshold = st.slider("🎯 Umbral de Clasificación (Threshold)", min_value=-10.0, max_value=10.0, value=2.0, step=0.5)

# -------------------------------------------------------------------------
# 3. INTERFAZ: Selección de Imagen de Prueba y Cálculo Matemático
# -------------------------------------------------------------------------
st.markdown("---")
st.header("🖼️ Banco de Pruebas Dinámico")

col_izq, col_der = st.columns([2, 3])

with col_izq:
    opcion = st.selectbox("Selecciona una imagen para evaluar:", list(patrones.keys()))
    imagen_actual = patrones[opcion]
    
    # Dibujar la imagen seleccionada de forma visual en la app
    st.write("**Píxeles de la imagen:**")
    render_tabla = ""
    for i in range(3):
        r1, r2, r3 = imagen_actual[i*3], imagen_actual[i*3+1], imagen_actual[i*3+2]
        # Cambiamos los 1 por cuadrados negros y los 0 por cuadrados blancos para simular una pantalla
        render_tabla += f"| {'⬛' if r1==1 else '⬜'} | {'⬛' if r2==1 else '⬜'} | {'⬛' if r3==1 else '⬜'} |\n"
    st.markdown(render_tabla)

with col_der:
    st.write("**Cálculo de la Máquina de Puntuación:**")
    
    # 🔁 OPERACIÓN MATEMÁTICA PURA (Sin librerías)
    suma_ponderada = 0.0
    detalles_operacion = []
    
    for i in range(9):
        pixel = imagen_actual[i]
        peso = pesos[i]
        producto = pixel * peso
        suma_ponderada += producto
        if pixel == 1:
            detalles_operacion.append(f"Píxel {i+1} activo (1) × Peso ({peso}) = {producto}")
            
    # Mostrar resultados numéricos
    st.write("🧮 Suma de píxeles activos:")
    for detalle in detalles_operacion:
        st.caption(detalle)
        
    st.markdown(f"### **Puntaje Total Obtenido ($y$):** `{round(suma_ponderada, 2)}`")
    
    # Decisión final basada en el Threshold
    if suma_ponderada >= threshold:
        st.success(f"🎉 **Resultado:** ¡CLASIFICADO COMO UNA LETRA T! (Puntaje ≥ {threshold})")
    else:
        st.error(f"❌ **Resultado:** RECHAZADO (Puntaje < {threshold})")

# -------------------------------------------------------------------------
# 4. TABLA GLOBAL DE PUNTUACIONES (Para el modo juego)
# -------------------------------------------------------------------------
st.markdown("---")
st.header("📊 Tabla de Clasificación Global")
st.write("Monitorea cómo reacciona tu configuración de pesos ante todos los patrones simultáneamente.")

tabla_global = []
for nombre, img in patrones.items():
    puntaje = sum(img[i] * pesos[i] for i in range(9))
    clasificacion = "✅ Es una T" if puntaje >= threshold else "❌ No es una T"
    
    # Saber si la máquina acertó según la lógica humana
    es_t_real = "Real" in nombre
    exito = "✨ Correcto" if (clasificacion == "✅ Es una T" and es_t_real) or (clasificacion == "❌ No es una T" and not es_t_real) else "🚨 Error"
    
    tabla_global.append({
        "Imagen": nombre,
        "Puntaje": round(puntaje, 2),
        "Predicción del Sistema": clasificacion,
        "Diagnóstico": exito
    })

st.table(tabla_global)
