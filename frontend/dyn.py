import numpy as np
import streamlit as st

from backend.dynamics import DynamicParams
from backend.session_state import get_dynamic_qubit, update_dynamic_qubit_instance

st.title("Динамическая модель")

st.markdown(
    "Для изучения поведения кубита под воздействием ЭМ поля было выбрано использовать слудующую модель гамильтониана: "
)
st.latex(
    r"""
H = \frac{1}{2}\, 2\pi \nu_z\, Z \;+\; 2\pi \nu_x \cos\!\left(2\pi \nu_d t\right)\, X"""
)

st.latex(
    r"\{X, Y, Z\} \text{ --- матрицы Паули } \bigl(\sigma^a,\; a\in\{x,y,z\}\bigr)."
)

st.latex(
    r"""
X=\begin{pmatrix}0&1\\[2pt]1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\[2pt]i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\[2pt]0&-1\end{pmatrix}.

"""
)

st.markdown(
    "[Вывод данной модели](https://github.com/Qiskit/platypus/blob/main/notebooks/v2/quantum-hardware-pulses/transmon-physics.ipynb)"
)

nu_z = st.sidebar.slider("ν_z (частота кубита)", 0.1, 10.0, 5.0, 0.01)
nu_d = st.sidebar.slider("ν_d (частота вн. сигнала)", 0.1, 10.0, 5.0, 0.01)
nu_x = st.sidebar.slider("ν_x (амплитуда)", 0.0, 2.0, 0.10, 0.001)
phase = 0
duration = st.sidebar.slider("duration", 0.1, 50.0, 5.0, 0.1)
dt = st.sidebar.slider("dt", 0.001, 0.1, 0.01, 0.001)
shots = st.sidebar.slider("shots", 100, 10000, 2000, 100, key="dyn_shots")

gamma1 = 0
gammaphi = 0
st.markdown("### Параметры динамической модели")

st.latex(r"\nu_z \; \text{— собственная частота кубита.}")
st.latex(r"\nu_x \; \text{— амплитуда управляющего воздействия.}")
st.latex(r"\nu_d \; \text{— частота внешнего сигнала.}")


p = DynamicParams(
    nu_z=float(nu_z),
    nu_d=float(nu_d),
    nu_x=float(nu_x),
    phase=float(phase),
    duration=float(duration),
    dt=float(dt),
    gamma1=float(gamma1),
    gammaphi=float(gammaphi),
)
update_dynamic_qubit_instance(p)

run = st.sidebar.button("Применить изменения")

dq = get_dynamic_qubit()
if run:
    dq.simulate(force=True)

if not dq.has_result():
    st.info("Нет примененных параметров")
    st.stop()

dq.draw_probs()
dq.draw_bloch()
dq.draw_counts(shots=shots)
dq.draw_bloch_components()


st.markdown(
    "[Реализация динамической модели](https://github.com/andrushechka37/Qubit-Simulation/blob/main/backend/dynamics.py)"
)
