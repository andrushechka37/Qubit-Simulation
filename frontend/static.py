import streamlit as st
from backend.session_state import (
    get_circuit_instance,
    SessionState,
    update_circuit_instance,
    clear_ops,
    pop_last_op,
)
from backend.cubits import CircuitParams, GateOp

st.title("Статическая модель")

# sliders
n = st.sidebar.slider("Количество кубитов", 2, 8, 2, 1, key="n_qubits")
session = SessionState(n)

qubit_number = st.sidebar.slider(
    "Номер кубита для настройки", 1, n, 1, 1, key="qubit_number"
)
cur_qubit = session.get_qubit_object_by_number(qubit_number - 1)

cur_qubit.theta = st.sidebar.slider(
    "θ (rx)", 0.0, 6.28318, float(cur_qubit.theta), 0.01, key=f"theta_{qubit_number-1}"
)
cur_qubit.phi = st.sidebar.slider(
    "φ (rz)", 0.0, 6.28318, float(cur_qubit.phi), 0.01, key=f"phi_{qubit_number-1}"
)

# -----------------------------
# Gate pool UI
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Логические гейты")

with st.sidebar.expander("Добавить гейт", expanded=True):
    gate = st.selectbox("Гейт", ["x", "h", "z", "cx", "cz", "ccx"], key="gate_type")

    q0 = st.number_input("q0", 1, n, 1, 1, key="gate_q0")
    q1 = None
    q2 = None

    if gate in ("cx", "cz", "ccx"):
        q1 = st.number_input("q1", 1, n, min(2, n), 1, key="gate_q1")
    if gate == "ccx":
        q2 = st.number_input("q2", 1, n, min(3, n), 1, key="gate_q2")

    col1, col2, col3 = st.columns(3)
    add = col1.button("Добавить", key="add_gate_btn")
    undo = col2.button("Удалить последний", key="undo_gate_btn")
    wipe = col3.button("Очистить", key="clear_gate_btn")

    if undo:
        pop_last_op()
    if wipe:
        clear_ops()

    if add:
        q0_i = int(q0) - 1
        q1_i = None if q1 is None else int(q1) - 1
        q2_i = None if q2 is None else int(q2) - 1

        if gate in ("cx", "cz") and (q1_i is None or q0_i == q1_i):
            st.error("Для CX/CZ нужно выбрать разные q0 и q1.")
        elif gate == "ccx" and (
            q1_i is None or q2_i is None or len({q0_i, q1_i, q2_i}) != 3
        ):
            st.error("Для CCX нужно выбрать три разных кубита: q0, q1, q2.")
        else:
            session.ops.append(GateOp(name=gate, q0=q0_i, q1=q1_i, q2=q2_i))

if session.ops:
    st.sidebar.markdown("#### Очередь операций")
    for i, op in enumerate(session.ops, start=1):
        if op.name in ("x", "h", "z"):
            st.sidebar.write(f"{i}. {op.name.upper()} q{op.q0 + 1}")
        elif op.name in ("cx", "cz"):
            st.sidebar.write(
                f"{i}. {op.name.upper()} q{op.q0 + 1} → q{(op.q1 or 0) + 1}"
            )
        else:
            st.sidebar.write(
                f"{i}. CCX q{op.q0 + 1}, q{(op.q1 or 0) + 1} → q{(op.q2 or 0) + 1}"
            )
else:
    st.sidebar.caption("Операций пока нет.")

# build circuit (angles + ops)
circuit = CircuitParams(n, session.angles, ops=session.ops)
update_circuit_instance(circuit)

# visuals
qc = get_circuit_instance()
st.info("Настройки состояний и гейтов расположены слева")

st.markdown("## Сфера Блоха:")
qc.draw_bloch_sphere()

st.markdown("## Распределение вероятностей:")
qc.draw_stats()

st.markdown("## Логическая схема:")
qc.draw_scheme()

st.markdown(
    "[Реализация статической модели](https://github.com/andrushechka37/Qubit-Simulation/blob/main/backend/cubits.py)"
)
