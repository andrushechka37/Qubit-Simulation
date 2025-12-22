from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
from typing import cast
from matplotlib.figure import Figure
import streamlit as st
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

from backend.cubits import get_circuit
qc = get_circuit()


qc.measure_all()
sim = AerSimulator()
result = sim.run(qc).result()
counts = result.get_counts()
fig = cast(Figure, plot_histogram(counts))
st.pyplot(fig, use_container_width=True)
plt.close(fig)