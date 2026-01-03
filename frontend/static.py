import streamlit as st
from backend.session_state import get_circuit_instance
from backend.session_state import SessionState, update_circuit_instance
from backend.cubits import CircuitParams

# sliders
n = st.sidebar.slider("Количество кубитов", 2, 8, 2, 1)
session = SessionState(n)

qubit_number = st.sidebar.slider("Номер кубита для настройки", 1, n, 1, 1)
cur_qubit = session.get_qubit_object_by_number(qubit_number - 1)
cur_qubit.theta = st.sidebar.slider(
    "θ (rx)", 0.0, 6.28318, cur_qubit.theta, 0.01, key=f"theta_{qubit_number-1}"
)
cur_qubit.phi = st.sidebar.slider(
    "φ (rz)", 0.0, 6.28318, cur_qubit.phi, 0.01, key=f"phi_{qubit_number-1}"
)

circuit = CircuitParams(n, session.angles)
update_circuit_instance(circuit)

# visuals

qc = get_circuit_instance()
st.info("Настройки состояний расположены слева")
st.markdown("## Сфера Блоха:")
qc.draw_bloch_sphere()
st.markdown("## Распределение вероятностей:")
qc.draw_stats()
st.markdown("## Логическая схема:")
qc.draw_scheme()

st.markdown(
    "[Реализация статической модели](https://github.com/andrushechka37/Qubit-Simulation/blob/main/backend/cubits.py)"
)
