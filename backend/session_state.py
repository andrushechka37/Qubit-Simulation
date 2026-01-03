import streamlit as st
from backend.cubits import CircuitParams, QubitParams
from backend.dynamics import DynamicQubit, DynamicParams
from typing import cast

_CIRCUIT_INSTANCE = "circuit"
_ANGLE_INSTANCE = "angle"
_DYNAMIC_INSTANCE = "dynamic_qubit_instance"


class SessionState:  # stores in session state of steamlit angles and number of qubits
    def __init__(self, n):
        if (
            _ANGLE_INSTANCE not in st.session_state
            or len(st.session_state[_ANGLE_INSTANCE]) != n
        ):
            st.session_state[_ANGLE_INSTANCE] = [QubitParams() for _ in range(n)]
        self.angles = st.session_state[_ANGLE_INSTANCE]

    def get_qubit_object_by_number(self, number):
        return self.angles[number]


def get_circuit_instance():
    if _CIRCUIT_INSTANCE not in st.session_state:
        st.session_state[_CIRCUIT_INSTANCE] = CircuitParams(0, [])
    return cast(CircuitParams, st.session_state[_CIRCUIT_INSTANCE])


def update_circuit_instance(instance):
    st.session_state[_CIRCUIT_INSTANCE] = instance


def get_dynamic_qubit() -> DynamicQubit:
    if _DYNAMIC_INSTANCE not in st.session_state:
        st.session_state[_DYNAMIC_INSTANCE] = DynamicQubit(DynamicParams())
    return cast(DynamicQubit, st.session_state[_DYNAMIC_INSTANCE])


def update_dynamic_qubit_instance(p: DynamicParams) -> None:
    dq = get_dynamic_qubit()
    dq.set_params(p)
