from dataclasses import dataclass
import streamlit as st
from qiskit import QuantumCircuit

@dataclass(frozen=True)
class CircuitParams:
    n_qubits: int = 1
    theta: float = 1.5708
    phi: float = 0.7
    entangle: bool = False

def get_params() -> CircuitParams:
    return st.session_state.get("qc_params", CircuitParams())

def set_params(p: CircuitParams) -> None:
    st.session_state["qc_params"] = p

@st.cache_data(show_spinner=False)
def _build_circuit(p: CircuitParams) -> QuantumCircuit:
    qc = QuantumCircuit(p.n_qubits)
    qc.rx(p.theta, 0)
    qc.rz(p.phi, 0)
    if p.n_qubits == 2 and p.entangle:
        qc.h(0); qc.cx(0, 1)
    return qc

def get_circuit() -> QuantumCircuit:
    return _build_circuit(get_params()).copy()  # copy — чтобы страницы не портили общий