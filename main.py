from qiskit.circuit.quantumcircuit import S
import streamlit as st
from backend.cubits import CircuitParams
from backend.session_state import SessionState, update_circuit_instance


def set_pages_st():
    st.title("Симулятор для исследования поведения кубитов в переменном магнитном поле")

    main_page = st.Page("frontend/main_page.py", title="Главная страница")
    bloch_sphere = st.Page("frontend/bloch_sphere.py", title="Сфера Блоха")
    stats = st.Page("frontend/stats.py", title="Распределение вероятностей")
    theory = st.Page("frontend/theory.py", title="Теория")
    circuit_scheme = st.Page("frontend/scheme.py", title="Схема")

    pg = st.navigation([main_page, bloch_sphere, stats, theory, circuit_scheme])
    return pg


def main():
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

    pg = set_pages_st()
    pg.run()


if __name__ == "__main__":
    main()
