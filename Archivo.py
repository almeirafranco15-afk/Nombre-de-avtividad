import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.set_page_config(page_title="Optimizador de Potencia", layout="wide")

st.title("📊 Optimización de Potencia en Redes de Telecomunicaciones")
st.markdown("""
Esta aplicación permite resolver el modelo de optimización lineal detallado en la **Guía Técnica de Telecomunicaciones**.
El objetivo es minimizar el consumo energético ($Z = P_1 + P_2 + P_3 + P_4$) bajo restricciones de calidad y hardware.
""")

# --- Sidebar para ajustes ---
st.sidebar.header("Parámetros del Sistema")
st.sidebar.markdown("Ajusta los valores para ver cómo cambia la optimización:")

# Inputs para las restricciones
c1 = st.sidebar.slider("Coeficiente Propagación P1", 1, 20, 12)
c2 = st.sidebar.slider("Coeficiente Propagación P2", 1, 20, 15)
c3 = st.sidebar.slider("Coeficiente Propagación P3", 1, 20, 8)
c4 = st.sidebar.slider("Coeficiente Propagación P4", 1, 20, 20)

threshold = st.sidebar.number_input("Umbral de Calidad (QoS)", min_value=100, max_value=500, value=200)
max_power = st.sidebar.number_input("Límite de Interferencia", min_value=10, max_value=50, value=25)
hw_limit = st.sidebar.number_input("Límite Térmico (Hardware)", min_value=1, max_value=20, value=10)

# --- Lógica de Resolución ---
# Función objetivo (minimizar consumo)
c = [1, 1, 1, 1]

# Matriz de restricciones
A = [
    [c1, c2, c3, c4], # Cobertura
    [1, 1, 1, 1]      # Interferencia
]

# Límites
bl = [threshold, -np.inf]
bu = [np.inf, max_power]

constraints = LinearConstraint(A, bl, bu)
bounds = Bounds([0]*4, [hw_limit]*4)

# Resolver
res = milp(c=c, constraints=constraints, bounds=bounds)

# --- Visualización ---
st.subheader("Resultados de la Optimización")

if res.success:
    col1, col2 = st.columns(2)
    with col1:
        st.success("¡Optimización Exitosa!")
        st.metric("Consumo Energético Total (Z)", f"{res.fun:.2f} Watts")
    with col2:
        st.write("Distribución de Potencia Óptima:")
        st.bar_chart(res.x)
    
    st.write("Valores de las variables (P1, P2, P3, P4):")
    st.write(res.x)
else:
    st.error("No se encontró una solución factible con estos parámetros. Intente ajustar el umbral o los límites.")

st.markdown("---")
st.subheader("📖 Notas del Modelo")
st.info("""
- **Cobertura:** $c_1P_1 + c_2P_2 + c_3P_3 + c_4P_4 \ge$ **Umbral**
- **Interferencia:** $\sum P_i \le$ **Límite de Interferencia**
- **Hardware:** $P_i \le$ **Límite Térmico**
""")
