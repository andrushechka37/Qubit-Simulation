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
