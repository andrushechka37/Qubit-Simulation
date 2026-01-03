import streamlit as st
from pathlib import Path

st.markdown("### Вопрос по выбору для государственного экзамена по физике")

img_path = Path(__file__).resolve().parent / "images" / "1.webp"
st.image(str(img_path), caption="...", use_container_width=True)

st.markdown(
    """
# Навигация: 
### (рекомендуется идти по порядку объявления вкладок)
"""
)
st.page_link("frontend/theory.py", label="➡️ Теоретическое введение")
st.markdown("Введение в предмет исследования")

st.page_link("frontend/how_work.py", label="➡️ Реализация")
st.markdown("Объяснение нюансов реализации симуляции")

st.page_link("frontend/static.py", label="➡️ Статическая модель")
st.markdown(
    "Симуляция распределения вероятностей при статическом задании положения кубитов"
)

st.page_link("frontend/dyn.py", label="➡️ Динамическая модель")
st.markdown("Симуляция распределения кубитов при воздействии на них поля")

st.markdown(
    "#### [Исходные файлы симулятора](https://github.com/andrushechka37/Qubit-Simulation)"
)
