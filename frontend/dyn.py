import numpy as np
import streamlit as st

from backend.dynamics import DynamicParams
from backend.session_state import get_dynamic_qubit, update_dynamic_qubit_instance

st.title("Динамическая модель")

nu_z = st.sidebar.slider("ν_z (частота кубита)", 0.1, 10.0, 5.0, 0.01)
nu_d = st.sidebar.slider("ν_d (частота драйва)", 0.1, 10.0, 5.0, 0.01)
nu_x = st.sidebar.slider("ν_x (амплитуда)", 0.0, 2.0, 0.10, 0.001)
phase = st.sidebar.slider("phase", 0.0, float(2 * np.pi), 0.0, 0.01)
duration = st.sidebar.slider("duration", 0.1, 50.0, 5.0, 0.1)
dt = st.sidebar.slider("dt", 0.001, 0.1, 0.01, 0.001)
shots = st.sidebar.slider("shots", 100, 10000, 2000, 100, key="dyn_shots")

with st.sidebar.expander("Шум", expanded=False):
    gamma1 = st.slider("Γ1 (T1)", 0.0, 5.0, 0.0, 0.01, key="dyn_gamma1")
    gammaphi = st.slider("Γφ (dephase)", 0.0, 5.0, 0.0, 0.01, key="dyn_gammaphi")

# ---- Пояснения текстом (markdown) ----
st.markdown("### Параметры динамической модели (что означает каждый)")

st.markdown(
    "**ν_z (частота кубита)** — собственная частота (расщепление уровней), постоянная часть гамильтониана вдоль Z."
)
st.latex(r"H_0=\frac{1}{2}(2\pi\nu_z)\,Z")

st.markdown("**ν_d (частота драйва)** — частота внешнего гармонического воздействия")
st.latex(r"\cos(2\pi\nu_d t+\varphi)")

st.markdown(
    "**ν_x (амплитуда)** — сила драйва; определяет скорость вращения вокруг оси X (частоту Раби)."
)
st.latex(r"H_{\text{drive}}(t)=(2\pi\nu_x)\cos(2\pi\nu_d t+\varphi)\,X")

st.markdown("**phase (фаза)** — начальная фаза в гармоническом сигнале.")

st.markdown(
    "**duration (длительность)** — время интегрирования (длина импульса/наблюдения)."
)

st.markdown("**dt** — шаг по времени (дискретизация); меньше → точнее, но медленнее.")

st.markdown(
    "**shots** — число «измерений» для гистограммы counts; на динамику не влияет, только на статистику."
)
st.latex(r"\text{counts} \sim \text{Multinomial}(\text{shots}, [P(0),P(1)])")

# ---- Шум (Линдблад) ----
st.markdown("### Шум (уравнение Линдблада)")


st.markdown("**Γ1 (T1)** — релаксация ")

st.markdown("**Γφ (dephase)** — чистая дефазировка (pure dephasing).")


p = DynamicParams(
    nu_z=float(nu_z),
    nu_d=float(nu_d),
    nu_x=float(nu_x),
    phase=float(phase),
    duration=float(duration),
    dt=float(dt),
    gamma1=float(gamma1),
    gammaphi=float(gammaphi),
)
update_dynamic_qubit_instance(p)

run = st.sidebar.button("Применить изменения")

dq = get_dynamic_qubit()
if run:
    dq.simulate(force=True)

if not dq.has_result():
    st.info("Нет примененных параметров")
    st.stop()

dq.draw_probs()
dq.draw_bloch()
dq.draw_counts(shots=shots)
dq.draw_bloch_components()


st.markdown(
    "[Реализация динамической модели](https://github.com/andrushechka37/Qubit-Simulation/blob/main/backend/cubits.py)"
)
