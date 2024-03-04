import streamlit as st

def main():
    st.sidebar.title("Навигация")

    # Создание словаря страниц
    pages = {
        "Тренд-карта": "/trend_map_page",
        "Семантическая карта": "/semantic_map_page",
        # Добавьте новые страницы с их ссылками сюда
    }

    # Изменение названий файлов на названия страниц
    for page_title, page_link in pages.items():
        sidebar_nav_link = st.sidebar.markdown(f"<a href='http://localhost:8501{page_link}' class='st-emotion-cache-nziaof eczjsme6'><span class='st-emotion-cache-pkbazv eczjsme5'>{page_title}</span></a>", unsafe_allow_html=True)


