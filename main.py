import streamlit as st
from backend.cubits import CircuitParams, QubitParams, _CIRCUIT_INSTANCE, _ANGLE_INSTANCE

def set_pages_st():
    st.title("Исследование поведения кубитов в переменном магнитном поле")

    main_page       = st.Page("frontend/main_page.py",    title="Главная страница")
    bloch_sphere    = st.Page("frontend/bloch_sphere.py", title="Сфера Блоха")
    stats           = st.Page("frontend/stats.py",        title="Распределение вероятностей")
    theory          = st.Page("frontend/theory.py",       title="Теория")
    circuit_scheme  = st.Page("frontend/scheme.py",       title="Схема")

    pg = st.navigation([main_page, bloch_sphere, stats, theory, circuit_scheme])
    return pg

def main():
    n = st.sidebar.slider("Количество кубитов", 2, 8, 2, 1)

    if _ANGLE_INSTANCE not in st.session_state or len(st.session_state[_ANGLE_INSTANCE]) != n:
        st.session_state[_ANGLE_INSTANCE] = [QubitParams() for _ in range(n)]

    qubit_number = st.sidebar.slider("Номер кубита кубитов", 1, n, 1, 1)
    angle = QubitParams()
    st.session_state[_ANGLE_INSTANCE][qubit_number-1].theta = st.sidebar.slider("θ (rx)", 0.0, 6.28318, st.session_state[_ANGLE_INSTANCE][qubit_number-1].theta, 0.01, key=f"theta_{qubit_number-1}")
    st.session_state[_ANGLE_INSTANCE][qubit_number-1].phi = st.sidebar.slider("φ (rz)", 0.0, 6.28318, st.session_state[_ANGLE_INSTANCE][qubit_number-1].phi, 0.01, key=f"phi_{qubit_number-1}")
    circuit = CircuitParams(n, st.session_state[_ANGLE_INSTANCE])
    st.session_state[_CIRCUIT_INSTANCE] = circuit

    pg = set_pages_st()
    pg.run()

if __name__ == "__main__":
    main()