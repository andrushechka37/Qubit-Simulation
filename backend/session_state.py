import streamlit as st
from backend.cubits import CircuitParams, QubitParams, GateOp
from backend.dynamics import DynamicQubit, DynamicParams
from typing import cast

_CIRCUIT_INSTANCE = "circuit"
_ANGLE_INSTANCE = "angle"
_DYNAMIC_INSTANCE = "dynamic_qubit_instance"
_OPS_INSTANCE = "ops"


class SessionState:  # stores in session state of streamlit angles, gates, etc.
    def __init__(self, n: int):
        # angles
        if (_ANGLE_INSTANCE not in st.session_state) or (
            len(st.session_state[_ANGLE_INSTANCE]) != n
        ):
            st.session_state[_ANGLE_INSTANCE] = [QubitParams() for _ in range(n)]

            st.session_state[_OPS_INSTANCE] = []

        # ops
        if _OPS_INSTANCE not in st.session_state:
            st.session_state[_OPS_INSTANCE] = []

        self.angles: list[QubitParams] = st.session_state[_ANGLE_INSTANCE]
        self.ops: list[GateOp] = st.session_state[_OPS_INSTANCE]

    def get_qubit_object_by_number(self, number: int) -> QubitParams:
        return self.angles[number]


def get_circuit_instance() -> CircuitParams:
    if _CIRCUIT_INSTANCE not in st.session_state:
        st.session_state[_CIRCUIT_INSTANCE] = CircuitParams(1, [QubitParams()], [])
    return cast(CircuitParams, st.session_state[_CIRCUIT_INSTANCE])


def update_circuit_instance(instance: CircuitParams) -> None:
    st.session_state[_CIRCUIT_INSTANCE] = instance


# --- ops helpers ---
def clear_ops() -> None:
    st.session_state[_OPS_INSTANCE] = []


def pop_last_op() -> None:
    ops = st.session_state.get(_OPS_INSTANCE, [])
    if ops:
        ops.pop()
        st.session_state[_OPS_INSTANCE] = ops


def get_dynamic_qubit() -> DynamicQubit:
    if _DYNAMIC_INSTANCE not in st.session_state:
        st.session_state[_DYNAMIC_INSTANCE] = DynamicQubit(DynamicParams())
    return cast(DynamicQubit, st.session_state[_DYNAMIC_INSTANCE])


def update_dynamic_qubit_instance(p: DynamicParams) -> None:
    dq = get_dynamic_qubit()
    dq.set_params(p)
