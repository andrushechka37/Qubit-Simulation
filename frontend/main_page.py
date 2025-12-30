import streamlit as st


st.markdown("## Вопрос по выбору для государственного экзамена по физике")
st.markdown("### Тема: исследование поведения кубитов в переменном магнитном поле")


import streamlit as st

st.markdown(
    """
### Навигация

1. **Сфера Блоха** — демонстрация положения кубитов на сфере Блоха.
2. **Распределение вероятностей** — симуляция распределения при измерении состояния кубитов (AerSimulator).
3. **Теория** — введение в предмет исследования.
4. **Принцип работы** — описание принципа работы симулятора.
5. **Схема** — какими операциями с кубитами достигнуто данное положение.
"""
)

st.page_link("frontend/bloch_sphere.py", label="➡️ Сфера Блоха")
st.page_link("frontend/stats.py", label="➡️ Распределение вероятностей")
st.page_link("frontend/theory.py", label="➡️ Теория")
# st.page_link("frontend/principle.py", label="➡️ Принцип работы")  # если есть файл
st.page_link("frontend/scheme.py", label="➡️ Схема")

st.markdown("#### [Исходники](https://github.com/andrushechka37/Qubit-Simulation)")
