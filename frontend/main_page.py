import streamlit as st
from pathlib import Path

st.markdown("### Вопрос по выбору для государственного экзамена по физике")

img_path = Path(__file__).resolve().parent / "images" / "1.webp"
st.image(str(img_path), caption="...", use_container_width=True)

st.page_link("frontend/theory.py", label="➡️ Теоретическое введение")
st.markdown("введение в предмет исследования")

st.page_link("frontend/how_work.py", label="➡️ Реализация")
st.markdown("объяснение нюансов реализации")

st.page_link("frontend/bloch_sphere.py", label="➡️ Сфера Блоха")
st.markdown("демонстрация положения кубитов на сфере Блоха")



st.page_link("frontend/stats.py", label="➡️ Распределение вероятностей")
st.markdown("симуляция распределения при измерении состояния кубитов")

st.page_link("frontend/scheme.py", label="➡️ Логическая схема")
st.markdown("схема, демонстрирующая, какими оперциями достигнуто положение кубитов")


st.markdown("#### [Исходники](https://github.com/andrushechka37/Qubit-Simulation)")
