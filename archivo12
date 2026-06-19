import streamlit as st
import numpy as np
import pandas as pd

from scipy.optimize import milp
from scipy.optimize import LinearConstraint
from scipy.optimize import Bounds

st.set_page_config(
    page_title="Optimizador MILP",
    layout="wide"
)

st.title("Optimizador de Programación Lineal / MILP")

st.markdown("""
Defina:

- Función objetivo
- Restricciones
- Límites de variables
- Variables enteras o continuas
""")

# -------------------------
# CONFIGURACIÓN
# -------------------------

n_vars = st.number_input(
    "Cantidad de variables",
    min_value=1,
    max_value=20,
    value=4
)

tipo_objetivo = st.radio(
    "Objetivo",
    ["Maximizar", "Minimizar"]
)

st.subheader("Coeficientes de la función objetivo")

c = []

cols = st.columns(min(n_vars, 4))

for i in range(n_vars):
    with cols[i % len(cols)]:
        coef = st.number_input(
            f"x{i+1}",
            value=1.0,
            key=f"obj_{i}"
        )
        c.append(coef)

# -------------------------
# VARIABLES
# -------------------------

st.subheader("Variables")

lb = []
ub = []
integrality = []

for i in range(n_vars):

    c1, c2, c3 = st.columns(3)

    with c1:
        lower = st.number_input(
            f"LB x{i+1}",
            value=0.0,
            key=f"lb_{i}"
        )

    with c2:
        upper = st.number_input(
            f"UB x{i+1}",
            value=10.0,
            key=f"ub_{i}"
        )

    with c3:
        entero = st.checkbox(
            f"Entera x{i+1}",
            key=f"int_{i}"
        )

    lb.append(lower)
    ub.append(upper)

    integrality.append(1 if entero else 0)

# -------------------------
# RESTRICCIONES
# -------------------------

st.subheader("Restricciones")

n_rest = st.number_input(
    "Cantidad de restricciones",
    min_value=1,
    max_value=50,
    value=2
)

A = []
bl = []
bu = []

for r in range(n_rest):

    st.markdown(f"### Restricción {r+1}")

    fila = []

    cols = st.columns(min(n_vars, 4))

    for j in range(n_vars):

        with cols[j % len(cols)]:
            aij = st.number_input(
                f"a({r+1},{j+1})",
                value=0.0,
                key=f"a_{r}_{j}"
            )

        fila.append(aij)

    c1, c2 = st.columns(2)

    with c1:
        lower = st.number_input(
            f"Límite inferior R{r+1}",
            value=-1e20,
            key=f"bl_{r}"
        )

    with c2:
        upper = st.number_input(
            f"Límite superior R{r+1}",
            value=10.0,
            key=f"bu_{r}"
        )

    A.append(fila)
    bl.append(lower)
    bu.append(upper)

# -------------------------
# RESOLVER
# -------------------------

if st.button("Resolver"):

    try:

        c_np = np.array(c)

        if tipo_objetivo == "Maximizar":
            c_np = -c_np

        constraints = LinearConstraint(
            np.array(A),
            np.array(bl),
            np.array(bu)
        )

        bounds = Bounds(lb, ub)

        resultado = milp(
            c=c_np,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality
        )

        if resultado.success:

            st.success("Solución encontrada")

            valor_obj = resultado.fun

            if tipo_objetivo == "Maximizar":
                valor_obj = -valor_obj

            st.metric(
                "Valor óptimo",
                round(valor_obj, 6)
            )

            sol = pd.DataFrame({
                "Variable": [f"x{i+1}" for i in range(n_vars)],
                "Valor": resultado.x
            })

            st.dataframe(sol, use_container_width=True)

        else:

            st.error(resultado.message)

    except Exception as e:
        st.exception(e)
