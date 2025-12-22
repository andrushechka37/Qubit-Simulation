from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
from typing import cast
from matplotlib.figure import Figure
import streamlit as st
import matplotlib.pyplot as plt

from backend.cubits import get_circuit
qc = get_circuit()
sv = Statevector.from_instruction(qc)
plot_bloch_multivector(sv)

fig = cast(Figure, plot_bloch_multivector(sv))
st.pyplot(fig, use_container_width=True)
plt.close(fig)