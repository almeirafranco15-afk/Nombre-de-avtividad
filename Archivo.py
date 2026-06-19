import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.title("Optimización de Potencia en una Red de Celdas Inalámbricas")

st.write("Resolver el problema de optimización lineal.")

if st.button("Optimizar"):

    # Función objetivo (negativa porque milp minimiza)
    c = [-25, -50]

    # Restricciones
    A = [
        [1, 1],
        [4, 6],
        [15, 40]
    ]

    bl = [-np.inf, 390, -np.inf]
    bu = [90, np.inf, 2000]

    constraints = LinearConstraint(A, bl, bu)

    bounds = Bounds(
        [0, 0],          # mínimos de x e y
        [np.inf, np.inf] # máximos
    )

    res = milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=[0, 0]
    )

    st.subheader("Resultados")

    st.write("Estado:", res.message)
    st.write("Valor óptimo F =", -res.fun)
    st.write("x =", res.x[0])
    st.write("y =", res.x[1])

    st.write("Vector solución:")
    st.write(res.x)
