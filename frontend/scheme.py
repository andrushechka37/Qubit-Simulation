import streamlit as st
import matplotlib.pyplot as plt
from typing import cast
from matplotlib.figure import Figure

from backend.cubits import get_circuit

qc = get_circuit()
fig = cast(Figure, qc.draw(output="mpl", initial_state=True, fold=60, scale=0.8))
st.pyplot(fig, use_container_width=True)
plt.close(fig)