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

    if 'index_changed' not in st.session_state:
        st.session_state.index_changed = False

    current_index = st.session_state.get('index')

    index_options = indexes.keys()
    index_index = 0 if current_index == "media" else 1

    selected_index = st.selectbox("Выберите индекс", index_options, index=index_index)

    if st.session_state.index_changed:
        st.session_state.index = indexes[selected_index]
        st.session_state.index_changed = False

    st.write(f"Выбранный индекс: {selected_index}")
    index = indexes[selected_index]
    return index, selected_index

def choose_significant_terms():
    st.subheader('✂️ "Significant terms"')

    option = st.radio('Выберите "Significant terms":', ["True", "False"], index=None)

    if option == "True":
        st.write("Significant terms: True")
        return True
    elif option == "False":
        st.write("Significant terms: False")
        return False
    else:
        st.warning("Пожалуйста, выберите один из вариантов")
        st.stop()

def input_num_points():
    st.subheader('📍Количество точек')

    if 'num_points_changed' not in st.session_state:
        st.session_state.num_points_changed = False

    current_num_points = st.session_state.get('num_points', 0)
    step = 100
    num_points = st.number_input("Введите количество точек", min_value=0, max_value=1000,
                                 value=current_num_points, step=step, key="num_points")

    if st.session_state.num_points_changed:
        st.write(f"Количество точек: {num_points}")
        st.session_state.num_points = num_points
        st.session_state.num_points_changed = False
    st.write(f"Количество точек: {num_points}")
    return num_points

def min_score():
    st.subheader('🧨 "Min Score"️')

    if 'min_score_changed' not in st.session_state:
        st.session_state.min_score_changed= False

    current_min_score = st.session_state.get('min_score', 21)
    step = 1
    min_score = st.number_input("Введите свой Min Score", min_value=5, max_value=30,
                                 value=current_min_score, step=step, key="min_score")

    if st.session_state.min_score_changed:
        st.write(f"Min Score: {min_score}")
        st.session_state.min_score = min_score
        st.session_state.min_score_changed = False
    st.write(f"Min Score: {min_score}")
    return min_score


def input_date_range():
    st.subheader("🌚 Выбор диапазона дат")

    if 'date_range_changed' not in st.session_state:
        st.session_state.date_range_changed = False

    current_start_year = st.session_state.get('start_year', 1991)
    current_end_year = st.session_state.get('end_year', 2024)

    start_year = st.selectbox("Выберите начальный год", list(range(1991, 2025)), index=current_start_year-1991, key="start_year")

    end_year = st.selectbox("Выберите конечный год", list(range(start_year, 2025)), index=current_end_year-start_year, key="end_year")

    if st.session_state.date_range_changed:
        st.session_state.start_year = start_year
        st.session_state.end_year = end_year
        st.session_state.date_range_changed = False
    st.write(f"Диапазон дат с: {start_year} по {end_year}")

    return start_year, end_year

def select_language():
    st.subheader("🇷🇺🇬🇧🇨🇳 Выбор языка")

    if 'language_changed' not in st.session_state:
        st.session_state.language_changed = False

    current_language = st.session_state.get('language')

    language_index = 0
    if current_language in ['ru', 'en', 'zh']:
        language_index = ['ru', 'en', 'zh'].index(current_language)

    language = st.selectbox("Выберите язык", ['ru', 'en', 'zh'], index=language_index)

    if st.session_state.language_changed:
        st.session_state.language = language
        st.session_state.language_changed = False

    st.write(f"Язык: {language}")

    return language

def count_words_in_term():
    st.subheader('🗿 Количество слов в термине')

    if 'ngram_size_changed' not in st.session_state:
        st.session_state.ngram_size_changed = False

    ngram_size = st.session_state.get('ngram_size', 1)
    step = 1
    ngram_size = st.number_input("Введите количество слов в термине", min_value=1, max_value=5,
                                 value=ngram_size, step=step, key="ngram_size")

    if st.session_state.ngram_size_changed:
        st.session_state.ngram_size = ngram_size
        st.session_state.ngram_size_changed = False
    st.write(f"Количество слов в термине: {ngram_size}")
    return ngram_size

