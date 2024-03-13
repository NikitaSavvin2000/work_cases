import pandas as pd
import streamlit as st



import streamlit as st



indexes = {
    'media': "*md_*_v1.*",
    'science': "sti_science_mag_latest",
    'patents_ru': "sti_patents_rospatent_latest",
    'patents_en': "sti_patents_patstat_latest",
    'grants': "sti_grants_*_v1.*",
    'clinicals': "sti_science_clinicaltrials_v0.*",
    'social_media': "social_media_telegram*",
    'rinc': "sti_science_rinc_v1.0.1",
    'crunchbase': "dir_crunchbase_v0.1.1",
    'onto_companies': "onto_companies_verified",
    'rinc_full_texts_v1.0.1': 'rinc_full_texts_v1.0.1',
    'sti_science_rinc_meta_v1.4': 'sti_science_rinc_meta_v1.4',
}


def check_csv(file_url):
    try:
        df = pd.read_csv(file_url)
        if 'keyword' not in df.columns or 'area' not in df.columns:
            current_col = df.columns.tolist()
            return False, f"CSV файл должен содержать колонки 'keyword' и 'area'. Ваши текущие колонки - {current_col}"
        if df.empty:
            return False, "CSV файл пустой."
        return True, df
    except Exception as e:
        return False, f"Ошибка при загрузке файла: {e}"

def input_csv():
    st.subheader("🔑 Ключевые слова")
    google_sheets_url = st.text_input("URL Google Sheets файла", st.session_state.get('google_sheets_url', ''))

    if google_sheets_url:
        is_valid, data = check_csv(google_sheets_url)
        if is_valid:
            st.session_state['google_sheets_url'] = google_sheets_url
            st.session_state['data'] = data
            if data is not None:
                st.write("Успешно загружен файл CSV из Google Sheets:")

            return data
        else:
            st.error(data)
            st.stop()
    else:
        st.warning("Пожалуйста, введите URL Google Sheets файла.")
        st.stop()

def select_index():
    st.subheader("📚 Выбор индекса")

    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = "media"

    selected_index = st.session_state.selected_index
    index_options = indexes.keys()
    index_index = list(index_options).index(selected_index) if selected_index in index_options else 0
    selected_index = st.selectbox("Выберите индекс", index_options, index=index_index)
    if selected_index != st.session_state.selected_index:
        st.session_state.selected_index = selected_index

    st.write(f"Выбранный индекс: {selected_index}")

    index = indexes[selected_index]
    return index, selected_index


# def select_search_field():
#     st.subheader("📚 Выбор поле поиска")
#
#     if 'selected_ашудв' not in st.session_state:
#         st.session_state.selected_index = "article_body"
#
#     selected_field = st.session_state.selected_field
#     field_options = fields.keys()
#     field_index = list(field_options).index(field_index) if field_index in field_options else 0
#     selected_field = st.selectbox("Выберите поле поиска", field_options, index=field_index)
#     if selected_index != st.session_state.selected_index:
#         st.session_state.selected_index = selected_index
#
#     st.write(f"Выбранный индекс: {selected_index}")
#
#     index = indexes[selected_index]
#     return index, selected_index


def choose_significant_terms():
    st.subheader('✂️ "Significant terms"')

    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = False

    selected_option = st.session_state.selected_option

    selected_option = st.radio("Выберите 'Significant terms':", [False, True], index=selected_option)

    # Если значение изменилось, обновляем session_state
    if selected_option != st.session_state.selected_option:
        st.session_state.selected_option = selected_option

    if selected_option:
        st.write("Significant terms: True")
    else:
        st.write("Significant terms: False")

    return selected_option


import streamlit as st

def input_num_points():
    st.subheader("📍Количество точек")

    if 'num_points' not in st.session_state:
        st.session_state.num_points = 100

    selected_num_points = st.session_state.num_points

    num_points = st.slider("Выберите количество точек", min_value=1, max_value=1000, step=1,  value=selected_num_points)

    if num_points != st.session_state.num_points:
        st.session_state.num_points = num_points

    st.write(f"Выбранное количество точек: {num_points}")

    return num_points

def min_score():
    st.subheader('🧨 "Min Score"️')

    if 'min_score' not in st.session_state:
        st.session_state.min_score = 21

    current_min_score = st.session_state.min_score

    min_score = st.slider("Выберите Min Score", min_value=5, max_value=30, value=current_min_score, step=1)

    if min_score != st.session_state.min_score:
        st.session_state.min_score = min_score

    st.write(f"Min Score: {min_score}")

    return min_score




import streamlit as st

import streamlit as st

def input_date_range():
    st.subheader("🌚 Выбор диапазона дат")

    if 'start_date' not in st.session_state:
        st.session_state.start_date = 2018

    if 'end_date' not in st.session_state:
        st.session_state.end_date = 2024

    start_date_options_list = list(range(1991, st.session_state.end_date + 1))
    end_date_options_list = list(range(st.session_state.start_date, 2025))

    current_start_index = start_date_options_list.index(st.session_state.start_date)
    end_start_index = end_date_options_list.index(st.session_state.end_date)

    start_date = st.selectbox(
        "Выберите начальный год",
        start_date_options_list,
        index=current_start_index
    )

    if start_date != st.session_state.start_date:
        st.session_state.start_date = start_date


    end_date = st.selectbox(
        "Выберите конечный год",
        end_date_options_list,
        index=end_start_index
    )

    if end_date != st.session_state.end_date:
        st.session_state.end_date = end_date

    st.write(f"Диапазон дат с: {start_date} по {end_date}")

    return start_date, end_date





def select_language():
    st.subheader("🇷🇺🇬🇧🇨🇳 Выбор языка")

    if 'language' not in st.session_state:
        st.session_state.language = 'ru'

    language_index = ['ru', 'en', 'zh'].index(st.session_state.language)
    language = st.selectbox("Выберите язык", ['ru', 'en', 'zh'], index=language_index)
    st.session_state.language = language
    st.write(f"Язык: {language}")

    return language

def count_words_in_term():
    st.subheader('🗿 Количество слов в термине')

    if 'ngram_size' not in st.session_state:
        st.session_state.ngram_size = 1

    step = 1
    ngram_size = st.slider("Введите количество слов в термине", min_value=1, max_value=5,
                                 value=st.session_state.ngram_size, step=step)

    st.session_state.ngram_size = ngram_size
    st.write(f"Количество слов в термине: {ngram_size}")

    return ngram_size

