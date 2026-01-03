import streamlit as st
from pathlib import Path

st.markdown(
    """
#### Для реализации симулятора была выбрана библиотека qiskit от IBM

## Статическая модель

### Пример использования: 


Для наглядности приведем пример работы данной библиотеки на примере программирования логического сумматора


"""
)

img_path = Path(__file__).resolve().parent / "images" / "5.png"
st.image(str(img_path), caption="...", use_container_width=True)

st.markdown(
    """

```python
qc_ha = QuantumCircuit(4,2)
# encode inputs in qubits 0 and 1
qc_ha.x(0) # For a=0, remove the this line. For a=1, leave it.
qc_ha.x(1) # For b=0, remove the this line. For b=1, leave it.
qc_ha.barrier()
# use cnots to write the XOR of the inputs on qubit 2
qc_ha.cx(0,2)
qc_ha.cx(1,2)
# use ccx to write the AND of the inputs on qubit 3
qc_ha.ccx(0,1,3)
qc_ha.barrier()
# extract outputs
qc_ha.measure(2,0) # extract XOR value
qc_ha.measure(3,1) # extract AND value

qc_ha.draw()
```

### Что делает код?

```python
qc_ha.x(0)
```

`.x` - операция NOT над выбранным номером кубита в массиве

то есть
```python
qc_ha.x(0) 
qc_ha.x(1) 
```

задает нам 2 кубита со значением один(для простоты, можно задавать не только дискретные значения, как мы увидим позже)


Вместо классического XOR над измеренными битами мы используем CX — унитарную операцию, которая записывает XOR в таргет без измерения.

в quiskit CNOT это операция `.cx`

Пример ее работы:

```python
qc_cnot = QuantumCircuit(2)
qc_cnot.cx(0,1)
qc_cnot.draw()
```


"""
)

img_path = Path(__file__).resolve().parent / "images" / "10.png"
st.image(str(img_path), caption="...", use_container_width=True)

st.markdown(
    """
Он применяется к паре кубитов: один работает как контрольный(q0), а таргет кубит (q1)

Можно его воспринимать как: если контролируюший 0, то ничего не делаем с таргетом, а если 1, то применяем NOT к таргету

CX не измеряет ни control, ни target: это обратимая унитарная операция. Измерение происходит только когда мы явно вызываем .measure(...).

Далее идет

```python
qc_ha.ccx(0,1,3)
```

`ccx` - тот же controlled not, но для его "активации" нужно чтоб оба бита были выставлены в 1

Таким образом получается схема сумматора:

"""
)

img_path = Path(__file__).resolve().parent / "images" / "5.png"
st.image(str(img_path), caption="...", use_container_width=True)

st.markdown(
    """
Берем q0 = 0, q1 = 1, q2 = q3 = 0
1) q0 = 0, q1 = 1, q2 = q3 = 0
2) q0 = 0, q1 = 1, q2 = 1, q3 = 0
3) q0 = 0, q1 = 1, q2 = 1, q3 = 0

получаем 01 в битах = 1

Берем q0 = 1, q1 = 1, q2 = q3 = 0
1) q0 = 1, q1 = 1, q2 = 1, q3 = 0
2) q0 = 1, q1 = 1, q2 = 0, q3 = 0
3) q0 = 1, q1 = 1, q2 = 0, q3 = 1

получаем 10 в битах = 2, все правильно

Вероятность распределения:
"""
)

img_path = Path(__file__).resolve().parent / "images" / "6.png"
st.image(str(img_path), caption="...", use_container_width=True)

st.markdown(
    """
Таким образом данные операции позволяют влиять на вероятности кубитов и конечного результата
как обсуждалось в теории.

Попробовать самому это можно во вкладке "Статическая модель"


"""
)

st.page_link("frontend/static.py", label="➡️ Статическая модель")

st.markdown(
    """
## Динамическая модель(вся вот эта часть написана плохо, я сам не до конца понимаю че тут написано):

При ее симуляции использовался пакет `qiskit_dynamics`

[Документация к `qiskit_dynamics`](https://qiskit-community.github.io/qiskit-dynamics/tutorials/Rabi_oscillations.html)

[Теория к ней](https://github.com/Qiskit/platypus/blob/main/notebooks/v2/quantum-hardware-pulses/transmon-physics.ipynb)


Мы рассматриваем кубит как двухуровневую систему (может быть 0 и 1)

Другая двухуровневая система была обнаружена в сверхпроводящих кубитах: [Cooper-pair box](https://arxiv.org/pdf/cond-mat/9904003v1)


Cooper-pair box состоит из сверхпроводящих островов которые или имеют заряд 2e (0) или не имеют (1)

Кубиты закодированы как заряды, и поэтому они чувствительны к charge noise и это также верно для Cooper Pair Box

И решение этой проблемы - [трансмон](https://arxiv.org/pdf/cond-mat/0703002)(transmission-line shunted plasma oscillation qubit) 


Про трансмон!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

КОРОЧЕ Я ВООБЩЕ НЕ ПОНЯЛ ОТКУДА они это берут, но в итоге получается

"""
)

st.latex(
    r"""
H = \frac{1}{2}\, 2\pi \nu_z\, Z \;+\; 2\pi \nu_x \cos\!\left(2\pi \nu_d t\right)\, X"""
)

st.latex(
    r"\{X, Y, Z\} \text{ --- матрицы Паули } \bigl(\sigma^a,\; a\in\{x,y,z\}\bigr)."
)

st.latex(
    r"""
X=\begin{pmatrix}0&1\\[2pt]1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\[2pt]i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\[2pt]0&-1\end{pmatrix}.

"""
)

st.markdown(
    """

Для удобства возьмем h с чертой = 1

```python
nu_z = 10.
nu_x = 1.
nu_d = 9.98  # Almost on resonance with the Hamiltonian's energy levels difference, nu_z

X = Operator.from_label('X')
Y = Operator.from_label('Y')
Z = Operator.from_label('Z')
s_p = 0.5 * (X + 1j * Y)

solver = Solver(
    static_hamiltonian=.5 * 2 * np.pi * nu_z * Z,
    hamiltonian_operators=[2 * np.pi * nu_x * X],
```

Далее We now define the initial state for the simulation, the time span to simulate for, and the intermediate times for which the solution is requested, and solve the evolution.

```python
t_final = .5 / nu_x
tau = .005

y0 = Statevector([1., 0.])

n_steps = int(np.ceil(t_final / tau)) + 1
t_eval = np.linspace(0., t_final, n_steps)
signals = [Signal(envelope=1., carrier_freq=nu_d)]

sol = solver.solve(t_span=[0., t_final], y0=y0, signals=signals, t_eval=t_eval)
```

Состояение кубита можно обозначить через матрицы паули

### Шумы

"""
)


st.markdown(
    """
Теперь мы добавляем к нашей симуляции окружение, моделируемое как “без-памяти” (марковская) ванна,
и решаем мастер-уравнение Линдблада с тем же гамильтонианом, что и раньше, но дополнительно учитывая
термины энергетической релаксации и декогеренции. Мы моделируем динамику на временах, которые больше,
чем типичные времена релаксации.
Состояние кубита теперь нужно описывать матрицей плотности, которая эволюционирует согласно мастер-уравнению Линдблада:
"""
)

st.latex(r"\partial_t \rho = -\frac{i}{\hbar}[H,\rho] + \mathcal{D}[\rho].")

st.markdown("Мы считаем, что диссипатор Линдблада состоит из двух слагаемых:")

st.latex(r"\mathcal{D}[\rho] = \mathcal{D}_1[\rho] + \mathcal{D}_2[\rho].")

st.markdown(
    """
Действие членов энергетической релаксации, описывающих затухание в окружение со скоростью \\(\\Gamma_1\\),
задаётся выражением:
"""
)

st.latex(
    r"\mathcal{D}_1[\rho] = \Gamma_1\left(\sigma^{+}\rho\sigma^{-}-\frac{1}{2}\{\sigma^{-}\sigma^{+},\rho\}\right),"
)

st.markdown("где")

st.latex(r"\sigma^{\pm}=\frac{1}{2}(X\pm iY).")

st.markdown(
    """
Второй диссипатор описывает (“чистую”) дефазировку со скоростью \\(\\Gamma_2\\) и имеет вид:
"""
)

st.latex(r"\mathcal{D}_2[\rho] = \Gamma_2\,(Z\rho Z-\rho).")


st.page_link("frontend/dyn.py", label="➡️ Динамическая модель")
