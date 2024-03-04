import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px


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

    google_sheets_url = st.sidebar.text_input("URL Google Sheets файла",
                                              st.session_state.get('google_sheets_url', ''))

    if google_sheets_url:
        is_valid, data = check_csv(google_sheets_url)
        if is_valid:

            st.session_state['google_sheets_url'] = google_sheets_url
            st.session_state['data'] = data
            if data is not None:
                st.write("Успешно загружен файл CSV из Google Sheets:")
                st.write(data)
            return data
        else:
            st.error(data)
            st.stop()
    else:
        st.warning("Пожалуйста, введите URL Google Sheets файла.")
        st.stop()



def choose_significant_terms():
    st.sidebar.subheader('Выбор "Significant terms"')

    option = st.sidebar.radio("Выберите значимый термин:", ["True", "False"], index=None)

    if option == "True":
        st.write("Significant terms: True")
        return True
    elif option == "False":
        st.write("Significant terms: False")
        return False
    else:
        st.sidebar.warning("Пожалуйста, выберите один из вариантов")
        st.stop()
