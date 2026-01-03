from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, cast
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from qiskit.quantum_info import Operator, Statevector, DensityMatrix
from qiskit_dynamics import Solver, Signal
from qiskit.visualization import plot_bloch_multivector, plot_histogram


@dataclass(frozen=True)
class DynamicParams:
    nu_z: float = 5.0
    nu_d: float = 5.0
    nu_x: float = 0.10
    phase: float = 0.0
    duration: float = 5.0
    dt: float = 0.01
    gamma1: float = 0.0
    gammaphi: float = 0.0


@dataclass
class DynamicsResult:
    t: np.ndarray
    probs: np.ndarray  # (T,2)
    final_state: Any  # Statevector | DensityMatrix
    states: list[Any]  # состояния во времени (T штук)


class DynamicQubit:
    def __init__(self, p: DynamicParams) -> None:
        self.p = p
        self._last: Optional[DynamicsResult] = None
        self._last_key: Optional[tuple] = None

    def set_params(self, p: DynamicParams) -> None:
        self.p = p

    def _key(self) -> tuple:
        p = self.p
        return (p.nu_z, p.nu_d, p.nu_x, p.phase, p.duration, p.dt, p.gamma1, p.gammaphi)

    def has_result(self) -> bool:
        return self._last is not None

    def simulate(self, force: bool = False) -> DynamicsResult:
        key = self._key()
        if (not force) and self._last is not None and self._last_key == key:
            return self._last

        p = self.p

        X = Operator.from_label("X")
        Y = Operator.from_label("Y")
        Z = Operator.from_label("Z")

        static_h = 0.5 * (2 * np.pi * p.nu_z) * Z
        ham_ops = [(2 * np.pi * p.nu_x) * X]

        dissipators = []
        if p.gamma1 > 0.0:
            sigma_minus = 0.5 * (X - 1j * Y)  # T1: |1> -> |0>
            dissipators.append(np.sqrt(p.gamma1) * sigma_minus)
        if p.gammaphi > 0.0:
            dissipators.append(np.sqrt(p.gammaphi) * Z)

        solver = Solver(
            static_hamiltonian=static_h,
            hamiltonian_operators=ham_ops,
            static_dissipators=dissipators if dissipators else None,
            dt=float(p.dt),
        )

        sig = Signal(1.0, carrier_freq=float(p.nu_d), phase=float(p.phase))
        t = np.arange(0.0, float(p.duration) + 1e-12, float(p.dt))

        y0 = (
            DensityMatrix.from_label("0")
            if dissipators
            else Statevector.from_label("0")
        )

        res = solver.solve(
            t_span=[0.0, float(p.duration)],
            y0=y0,
            t_eval=t,
            signals=[sig],
        )

        states = cast(Any, res).y
        probs = np.array([s.probabilities() for s in states], dtype=float)

        out = DynamicsResult(
            t=t, probs=probs, final_state=states[-1], states=list(states)
        )
        self._last = out
        self._last_key = key
        return out

    def _ensure(self) -> DynamicsResult:
        if self._last is None:
            raise RuntimeError("No dynamics result yet. Call simulate() first.")
        return self._last

    # ----- drawing (как в твоём CircuitParams) -----

    def draw_probs(self) -> None:
        if self._last is None:
            st.info("Нажми «Симулировать поле» слева.")
            return

        r = self._ensure()
        st.subheader("P(|0⟩), P(|1⟩) во времени")

        df = pd.DataFrame(
            {"t": r.t, "P0": r.probs[:, 0], "P1": r.probs[:, 1]}
        ).set_index("t")

        st.line_chart(df)

    def draw_bloch(self) -> None:
        if self._last is None:
            st.info("Нажми «Симулировать поле» слева.")
            return
        r = self._ensure()
        st.subheader("Сфера Блоха (финальное состояние)")
        fig = cast(Figure, plot_bloch_multivector(r.final_state))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_counts(self, shots: int = 2000) -> None:
        if self._last is None:
            st.info("Нажми «Симулировать поле» слева.")
            return
        r = self._ensure()
        st.subheader("Распределение вероятностей")

        # финальные вероятности
        p0 = float(r.probs[-1, 0])
        p1 = float(r.probs[-1, 1])

        # 1) clamp
        p0 = min(max(p0, 0.0), 1.0)
        p1 = min(max(p1, 0.0), 1.0)

        # 2) normalize
        s = p0 + p1
        if not np.isfinite(s) or s <= 0.0:
            st.error(
                f"Некорректные вероятности: P0={p0}, P1={p1} (sum={s}). Попробуй уменьшить dt или выключить шум."
            )
            return

        p0 /= s
        p1 /= s

        # иногда удобно вывести контроль
        st.caption(
            f"Финальные вероятности (норм.): P0={p0:.6f}, P1={p1:.6f}, sum={p0+p1:.6f}"
        )

        samples = np.random.choice(["0", "1"], size=shots, p=[p0, p1])
        counts = {"0": int((samples == "0").sum()), "1": int((samples == "1").sum())}

        fig = cast(Figure, plot_histogram(counts))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    def draw_bloch_components(self, show_final_vector: bool = True) -> None:
        """
        Рисует графики <X>(t), <Y>(t), <Z>(t) по результатам последней симуляции.
        Работает и для Statevector, и для DensityMatrix (при шуме).
        """
        if self._last is None:
            st.info("Нажми «Симулировать поле» слева.")
            return

        r = self._ensure()

        # Операторы Паули как Operator (как у тебя в simulate)
        X = Operator.from_label("X")
        Y = Operator.from_label("Y")
        Z = Operator.from_label("Z")

        # Посчитаем ожидания во времени
        x_data = np.array(
            [float(s.expectation_value(X).real) for s in r.states], dtype=float
        )
        y_data = np.array(
            [float(s.expectation_value(Y).real) for s in r.states], dtype=float
        )
        z_data = np.array(
            [float(s.expectation_value(Z).real) for s in r.states], dtype=float
        )

        st.subheader("Компоненты вектора Блоха во времени: ⟨X⟩, ⟨Y⟩, ⟨Z⟩")

        # Streamlit line_chart любит DataFrame с индексом
        df = pd.DataFrame(
            {"t": r.t, "<X>": x_data, "<Y>": y_data, "<Z>": z_data}
        ).set_index("t")
        st.line_chart(df)

        if show_final_vector:
            st.caption(
                f"Финальный вектор Блоха: "
                f"(<X>,<Y>,<Z>) = ({x_data[-1]:.4f}, {y_data[-1]:.4f}, {z_data[-1]:.4f})"
            )
