
from qiskit import QuantumCircuit
import streamlit as st
from frontend.shared import CircuitParams, set_params, get_params


st.title("Исследование поведения кубитов в переменном магнитном поле")



main_page = st.Page("frontend/main_page.py", title="Главная страница")
bloch_sphere = st.Page("frontend/bloch_sphere.py", title="Сфера Блоха")
stats = st.Page("frontend/stats.py", title="Распределение вероятностей")
theory = st.Page("frontend/theory.py", title="Теория")
circuit_scheme = st.Page("frontend/scheme.py", title="Схема")


p = get_params()
n = st.sidebar.slider("Количество кубитов", 1, 8, p.n_qubits, 1, key="n_qubits")
theta = st.sidebar.slider("θ (rx)", 0.0, 6.28318, float(p.theta), 0.01, key="theta")
phi = st.sidebar.slider("φ (rz)", 0.0, 6.28318, float(p.phi), 0.01, key="phi")

# 2) Записали параметры ДО pg.run()
set_params(CircuitParams(n_qubits=n, theta=theta, phi=phi, entangle=(n == 2)))


# Set up navigation
pg = st.navigation([main_page, bloch_sphere, stats, theory, circuit_scheme])

# Run the selected page
pg.run()