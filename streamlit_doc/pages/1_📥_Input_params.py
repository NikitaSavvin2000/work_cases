import time

import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container


from input import input_csv, choose_significant_terms, input_num_points, min_score, \
    input_date_range, select_language, count_words_in_term, select_index

build_map = False

st.set_page_config(page_title="Семантическая-карта", page_icon="📊", layout="wide")

st.markdown("# Ввод данных")
st.sidebar.header("Ввод данных")

font_size = "20px"


col1, col2 = st.columns([1, 1])
with col2:
    df_init = input_csv()

    with col1:
        st.write(f'<span style="font-size:{font_size}">🔑 Ключевые слова</span>',
                 unsafe_allow_html=True)
        st.write(df_init)
    index, selected_index = select_index()
    with col1:
        st.write(f'<span style="font-size:{font_size}">📚 Индекс - {selected_index}</span>',
                 unsafe_allow_html=True)
    selected_option = choose_significant_terms()
    with col1:
        st.write(f'<span style="font-size:{font_size}">✂️  "Significant terms" - {selected_option}</span>',
                 unsafe_allow_html=True)
    num_points = input_num_points()
    with col1:
        st.write(f'<span style="font-size:{font_size}">📍 Количество точек - {num_points}</span>',
                 unsafe_allow_html=True)
    min_score = min_score()
    with col1:
        st.write(f'<span style="font-size:{font_size}">🧨  "Min Score"️ - {min_score}</span>',
                 unsafe_allow_html=True)
    start_date, end_date = input_date_range()
    with col1:
        st.write(f'<span style="font-size:{font_size}">🌚  Диапазона дат - c {start_date} по {end_date}</span>',
                 unsafe_allow_html=True)
    language = select_language()
    with col1:
        your_lang_dict = {
            'ru': '🇷🇺',
            'en': '🇬🇧',
            'zh': '🇨🇳',
        }
        st.write(f'<span style="font-size:{font_size}">{your_lang_dict[language]}  Язык - {language}</span>',
                 unsafe_allow_html=True)
    ngram_size = count_words_in_term()
    with col1:
        st.write(f'<span style="font-size:{font_size}">🗿 Количество слов в термине - {ngram_size}</span>',
                 unsafe_allow_html=True)

    with col1:
        col1_left, col1_middle, col1_right = col1.columns([0.2, 0.6, 0.2])
        with col1_middle:
            st.write(f'')
            with stylable_container(key="my_unique_button", css_styles="""
                /* Стили для кнопок с фоновым цветом green */
                [data-testid="baseButton-secondary"] {
                    font-size: 20px !important; /* Задаем размер шрифта */
                    background-color: green; /* Задаем фоновый цвет */
                    padding: 10px 30px; /* Задаем отступы вокруг кнопки */
                    display: flex; /* Устанавливаем flex-контейнер */
                    justify-content: center; /* Выравниваем содержимое по центру по горизонтали */
                    text-align: center; /* Выравниваем текст по центру по горизонтали */
                    align-items: center; /* Выравниваем содержимое по центру по вертикали */
                    margin: auto;
                }

                /* Стили для блока div внутри блока с сообщением */
                [data-testid="stAlert"] div {
                    font-size: 20px !important; /* Задаем размер шрифта */
                    display: flex; /* Устанавливаем flex-контейнер */
                    justify-content: center; /* Выравниваем содержимое по центру по горизонтали */
                    align-items: center; /* Выравниваем содержимое по центру по вертикали */
                }

                /* Стили для блока div внутри кнопки */
                [data-testid="stButton"] div {
                    font-size: 20px !important; /* Задаем размер шрифта */
                    display: flex; /* Устанавливаем flex-контейнер */
                    justify-content: center; /* Выравниваем содержимое по центру по горизонтали */
                    align-items: center; /* Выравниваем содержимое по центру по вертикали */
                }

                /* Стили для блока span внутри кнопки */
                [data-testid="stButton"] span {
                    font-size: 20px !important; /* Задаем размер шрифта */
                    display: flex; /* Устанавливаем flex-контейнер */
                    align-items: center; /* Выравниваем содержимое по центру по вертикали */
                }
                
                /* Стили для блока div внутри блока с сообщением */
                [data-testid="stSpinner"] div {
                    font-size: 20px !important; /* Задаем размер шрифта */
                    display: flex; /* Устанавливаем flex-контейнер */
                    justify-content: center; /* Выравниваем содержимое по центру по горизонтали */
                    align-items: center; /* Выравниваем содержимое по центру по вертикали */
                }
            """, ):
                if st.button("🚀 Построить карты 🌎"):
                    st.write(
                        f'<div style="display: flex; justify-content: center;"><span style="font-size:{font_size}; text-align: center;">🥷 Начинаем строить карты. Обычно это занимает 3-5 минут...</span></div>',
                        unsafe_allow_html=True)
                    st.write('')
                    with st.spinner('📈 Строим карты... 📉'):
                        finish_calculate = False
                        st.session_state.finish_calculate = finish_calculate
                        # Здесь будет код получения trend_map_df пока он подставлен
                        trend_map_df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRuKlvnZ01eveM-x0jRkDYKu8mkqQwPhVIb0V1K8PjBoN3zEgi69QR2JB8PLTSLjE7O4VkFOJNFXjZN/pub?gid=1103843369&single=true&output=csv')
                        time.sleep(3)
                        finish_calculate = True
                        st.session_state.finish_calculate = finish_calculate
                        st.success(' 🏄 Карты построились! 🤸')
                        st.session_state.trend_map_df = trend_map_df
