from __future__ import annotations

import streamlit as st
from dataclasses import dataclass
from typing import Literal, Optional, cast

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerSimulator


@dataclass
class QubitParams:
    theta: float = 0.0
    phi: float = 0.0


GateName = Literal["x", "h", "z", "cx", "cz", "ccx"]


@dataclass(frozen=True)
class GateOp:
    name: GateName
    q0: int
    q1: Optional[int] = None
    q2: Optional[int] = None


class CircuitParams:
    def __init__(
        self,
        n_qubits: int,
        qubit_angles: list[QubitParams],
        ops: Optional[list[GateOp]] = None,
    ):
        self.n_qubits: int = n_qubits
        self.qubit_angles: list[QubitParams] = qubit_angles
        self.ops: list[GateOp] = ops or []

        self.circuit = QuantumCircuit(self.n_qubits)

        for i, a in enumerate(self.qubit_angles):
            if i >= self.n_qubits:
                break
            self.circuit.rx(float(a.theta), i)
            self.circuit.rz(float(a.phi), i)

        for op in self.ops:
            self._apply_op(op)

    def _valid_q(self, q: Optional[int]) -> bool:
        return q is not None and 0 <= q < self.n_qubits

    def _apply_op(self, op: GateOp) -> None:
        if not self._valid_q(op.q0):
            return

        if op.name == "x":
            self.circuit.x(op.q0)
            return
        if op.name == "h":
            self.circuit.h(op.q0)
            return
        if op.name == "z":
            self.circuit.z(op.q0)
            return

        if op.name in ("cx", "cz"):
            if not self._valid_q(op.q1):
                return
            if op.q0 == op.q1:
                return
            if op.name == "cx":
                self.circuit.cx(op.q0, cast(int, op.q1))
            else:
                self.circuit.cz(op.q0, cast(int, op.q1))
            return

        if op.name == "ccx":
            if not self._valid_q(op.q1) or not self._valid_q(op.q2):
                return
            q1 = cast(int, op.q1)
            q2 = cast(int, op.q2)
            if len({op.q0, q1, q2}) != 3:
                return
            self.circuit.ccx(op.q0, q1, q2)
            return

    def get_cur_circuit(self) -> QuantumCircuit:
        return self.circuit

    def draw_bloch_sphere(self) -> None:
        sv = Statevector.from_instruction(self.circuit)
        fig = cast(Figure, plot_bloch_multivector(sv))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_scheme(self) -> None:
        fig = cast(
            Figure,
            self.circuit.draw(output="mpl", initial_state=True, fold=60, scale=0.8),
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_stats(self) -> None:
        qc = self.circuit.copy()
        qc.measure_all()
        sim = AerSimulator()
        result = sim.run(qc).result()
        counts = result.get_counts()
        fig = cast(Figure, plot_histogram(counts))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
