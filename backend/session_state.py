import streamlit as st
from backend.cubits import CircuitParams, QubitParams
from typing import cast

_CIRCUIT_INSTANCE = "circuit"
_ANGLE_INSTANCE = "angle"


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
