import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px

from input import input_csv, choose_significant_terms, input_num_points, min_score, \
    input_date_range, select_language, count_words_in_term, select_index


st.set_page_config(page_title="Семантическая-карта", page_icon="📊", layout="wide")

import streamlit as st
import pandas as pd



st.markdown("# Ввод данных")
st.sidebar.header("Ввод данных")


col1, col2 = st.columns([1, 1])  # Разделение экрана на два столбца
with col2:
    df = input_csv()
    with col1:
        st.write(f'🔑 Ключевые слова')
        st.write(df)
    index = select_index()
    with col1:
        st.write(f'📚 Индекс - {index}')
    selected_option = choose_significant_terms()
    with col1:
        st.write(f'✂️  "Significant terms" - {selected_option}')
    num_points = input_num_points()
    with col1:
        st.write(f'📍 Количество точек - {num_points}')
    min_score = min_score()
    with col1:
        st.write(f'🧨  "Min Score"️ - {min_score}')
    start_date, end_date = input_date_range()
    with col1:
        st.write(f'🌚  Диапазона дат - c {start_date} по {end_date}')
    language = select_language()
    with col1:
        your_lang_dict = {
            'ru': '🇷🇺',
            'en': '🇬🇧',
            'zh': '🇨🇳',
        }
        st.write(f'{your_lang_dict[language]}  Язык - {language}')
    ngram_size = count_words_in_term()
    with col1:
        st.write(f'🗿 Количество слов в термине - {ngram_size}')

    with col1:

        # Обработка нажатия кнопки
        if st.button("  🚀  Поехали  🌎  "):
            print()




