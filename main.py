import streamlit as st


def set_pages_st():
    st.title("Симуляция поведения кубитов в переменном магнитном поле")

    main_page = st.Page("frontend/main_page.py", title="Главная страница")
    theory = st.Page("frontend/theory.py", title="Теоретическое введение")
    how_it_works = st.Page("frontend/how_work.py", title="Реализация")
    static = st.Page("frontend/static.py", title="Статическая модель")
    dyn = st.Page("frontend/dyn.py", title="Динамеческая модель")

    pg = st.navigation([main_page, theory, how_it_works, static, dyn])
    return pg


def main():
    pg = set_pages_st()
    pg.run()


if __name__ == "__main__":
    main()
