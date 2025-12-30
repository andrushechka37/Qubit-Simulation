import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from typing import cast
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector
from matplotlib.figure import Figure
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator


class QubitParams:
    theta: float = 0.0
    phi: float = 0.0


class CircuitParams:
    def __init__(self, n_qubits, qubit_angles: list[QubitParams]):
        self.n_qubits: int = n_qubits
        self.qubit_angles: list[QubitParams] = qubit_angles
        self.circuit = QuantumCircuit(self.n_qubits)
        for i, a in enumerate(self.qubit_angles):
            self.circuit.rx(a.theta, i)
            self.circuit.rz(a.phi, i)

    def get_cur_circuit(self):
        return self.circuit

    def draw_bloch_sphere(self):
        sv = Statevector.from_instruction(self.circuit)
        plot_bloch_multivector(sv)

        fig = cast(Figure, plot_bloch_multivector(sv))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_scheme(self):
        fig = cast(
            Figure,
            self.circuit.draw(output="mpl", initial_state=True, fold=60, scale=0.8),
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_stats(self):
        qc = self.circuit.copy()
        qc.measure_all()
        sim = AerSimulator()
        result = sim.run(qc).result()
        counts = result.get_counts()
        fig = cast(Figure, plot_histogram(counts))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
