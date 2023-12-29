import datetime
from telegram import InputFile
from io import BytesIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from tg_bot.build_map import building_map_and_exel

import re
# Установите свой токен от BotFather
TOKEN = ""

# Определение стадий разговора
SELECT_LANGUAGE, START_YEAR, FINISH_YEAR, INDEX, QUERY_TERMS, WAIT_QUERY_CONFIRMATION, FORMULATE_QUERY, BUILD_MAP = range(8)

years = [str(year) for year in range(1990, 2024)]

indices_index = ['Медиа']

from telegram import Update

from telegram import KeyboardButton, ReplyKeyboardMarkup




def add_start_over_button(keyboard: ReplyKeyboardMarkup, context: CallbackContext) -> ReplyKeyboardMarkup:
    # Create a "Start Over" button
    start_over_button = KeyboardButton("Сбросить все и начать сначала")

    keyboard.keyboard.append([start_over_button])

    return keyboard


def reset_user_data(context: CallbackContext):
    context.user_data.clear()

def start(update, context):
    languages_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton('🇨🇳 Chinese'), KeyboardButton('🇷🇺 Russian'), KeyboardButton('🇬🇧 English')],
    ], one_time_keyboard=True)

    update.message.reply_text("Выбери язык карты:", reply_markup=languages_keyboard)
    return SELECT_LANGUAGE

def select_language(update, context):
    # Get the selected language from the user's input
    selected_language = update.message.text.lower()

    if selected_language == '🇨🇳 chinese':
        context.user_data['language'] = 'zh'
    elif selected_language == '🇷🇺 russian':
        context.user_data['language'] = 'ru'
    elif selected_language == '🇬🇧 english':
        context.user_data['language'] = 'en'
    else:
        update.message.reply_text("Invalid language selection. Please choose a valid language.")
        return SELECT_LANGUAGE

    # Create a keyboard with buttons for selecting the initial year
    years_start = [str(y) for y in range(1990, 2024)]
    keyboard_start = [[year] for year in years_start]
    reply_markup = add_start_over_button(ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=True), context)

    update.message.reply_text(f"выбранный язык: {context.user_data['language']}. Пожалуйста выбери начало анализа:", reply_markup=reply_markup)
    return START_YEAR


def formulate_query(update: Update, context: CallbackContext) -> int:
    query = context.user_data.get('query', '')
    context.user_data.clear()
    update.message.reply_text("Запрос выполнен. Чтобы начать новый запрос, используйте /start.")
    return ConversationHandler.END

def set_start_year(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text

    if input_text == "Сбросить все и начать сначала":
        reset_user_data(context)
        return start(update, context)
    try:
        year = int(input_text)
        if 1990 <= year <= datetime.datetime.now().year + 10:  # You can adjust the range
            context.user_data['start_year'] = year  # Store the chosen start year
            years_finish = [str(y) for y in range(context.user_data['start_year'], 2024)]
            keyboard_finish = [[year] for year in years_finish]
            reply_markup = add_start_over_button(ReplyKeyboardMarkup(keyboard_finish, one_time_keyboard=True), context)

            update.message.reply_text("Отлично! Теперь выберите конечный год:", reply_markup=reply_markup)
            return FINISH_YEAR
        else:
            update.message.reply_text("Введенный год некорректен. Пожалуйста, выберите год из предложенных кнопок.")
            return START_YEAR
    except ValueError:
        update.message.reply_text("Введенный текст не является годом. Пожалуйста, выберите год из предложенных кнопок.")
        return START_YEAR


def set_finish_year(update, context: CallbackContext) -> int:
    input_text = update.message.text

    if input_text == "Сбросить все и начать сначала":
        reset_user_data(context)
        return start(update, context)

    try:
        year = int(input_text)
        if 1990 <= year <= datetime.datetime.now().year + 10:  # You can adjust the range
            context.user_data['finish_year'] = input_text

            keyboard_index = [[index] for index in indices_index]
            reply_markup = add_start_over_button(ReplyKeyboardMarkup(keyboard_index, one_time_keyboard=True), context)

            update.message.reply_text("Хорошо! Теперь выберите индекс:", reply_markup=reply_markup)
            return INDEX
        else:
            update.message.reply_text("Введенный год некорректен. Пожалуйста, выберите год из предложенных кнопок.")
            return FINISH_YEAR
    except ValueError:
        update.message.reply_text("Введенный текст не является годом. Пожалуйста, выберите год из предложенных кнопок.")
        return FINISH_YEAR


def set_index(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text

    if input_text == "Сбросить все и начать сначала":
        reset_user_data(context)
        return start(update, context)

    predefined_indices = indices_index  # Replace with your actual indices

    if input_text not in predefined_indices:
        update.message.reply_text("Выбран некорректный индекс. Пожалуйста, выберите индекс из предложенных кнопок.")
        return INDEX

    context.user_data['index'] = input_text

    keyboard = ReplyKeyboardMarkup([["Сформировать термины"]], one_time_keyboard=True)
    reply_markup = add_start_over_button(keyboard, context)

    update.message.reply_text("Отлично! Теперь введите термины для запроса. Когда закончите, нажмите 'Сформировать запрос'.", reply_markup=reply_markup)
    return QUERY_TERMS

FINALIZED_QUERY = 'finalized_query'
TERMS_FINALIZED = 'terms_finalized'
TERMS_FINALIZED = 'terms_finalized'
WAIT_ADDITIONAL_ACTION = 4
TERMS_FINALIZED = 'terms_finalized'
WAIT_ADDITIONAL_ACTION = 4


def format_query_terms(query):
    # Match terms with optional AND, OR, notAND operators
    terms_with_operators = re.findall(r'\w+\s*(?:AND|OR|notAND)?', query)

    formatted_terms = []
    for term_with_operator in terms_with_operators:
        term = re.match(r'\w+', term_with_operator).group()
        formatted_term = f'"{term}"'
        formatted_terms.append(formatted_term)

    return f'({" OR ".join(formatted_terms)})'

def set_query(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text
    if input_text == "Сбросить все и начать сначала":
        reset_user_data(context)
        return start(update, context)

    if input_text == "Сформировать термины":
        terms = context.user_data.get('query_terms', [])
        if terms:
            keyboard = ReplyKeyboardMarkup([["Сформировать запрос"]],
                                           one_time_keyboard=True)
            reply_markup = add_start_over_button(keyboard, context)
            query = ' OR '.join(f'("{term}")' if 'AND' in term else f'"{term}"' for term in terms)
            context.user_data['query'] = query
            formatted_query = ' OR '.join(f'("{term}")' for term in terms)
            update.message.reply_text(f"Сформированные термины: {formatted_query}",
                                      reply_markup=reply_markup)
            context.user_data[TERMS_FINALIZED] = True
            return FORMULATE_QUERY
        elif not terms:
            keyboard = ReplyKeyboardMarkup([["Сформировать термины"]],
                                           one_time_keyboard=True)
            reply_markup = add_start_over_button(keyboard, context)
            update.message.reply_text(f"Пустые термины! Введите термины!!!",
                                      reply_markup=reply_markup)
            return QUERY_TERMS

    elif context.user_data.get(TERMS_FINALIZED, False):
        update.message.reply_text("Термины уже сформированы. Выберите действие из предложенных кнопок.")
        return QUERY_TERMS

    query_terms = context.user_data.get('query_terms', [])
    query_terms.append(input_text)
    context.user_data['query_terms'] = query_terms

    current_terms = ' OR '.join(f'("{term}")' for term in query_terms)
    update.message.reply_text(f"Текущие термины: {current_terms}")
    return QUERY_TERMS


def formulate_query(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text

    if not context.user_data.get(TERMS_FINALIZED, False):
        update.message.reply_text("Термины не сформированы. Выберите действие из предложенных кнопок.")
        return WAIT_ADDITIONAL_ACTION

    if input_text == "Сбросить все и начать сначала":
        reset_user_data(context)
        return start(update, context)

    if input_text == "Сформировать запрос":
        language = context.user_data.get('language', 'Not specified')
        start_year = context.user_data.get('start_year', 'Not specified')
        finish_year = context.user_data.get('finish_year', 'Not specified')
        index = context.user_data.get('index', 'Not specified')
        query = context.user_data.get('query', 'Not specified')

        update.message.reply_text(
            f"Параметры:\n\n"
            f"Язык: {language}\n"
            f"Начальный год: {start_year}\n"
            f"Конечный год: {finish_year}\n"
            f"Индекс: {index}\n"
            f"Запрос: {query}\n"
        )

        keyboard = ReplyKeyboardMarkup([["Построить карту"], ["Сбросить все и начать сначала"]],
                                       one_time_keyboard=True)
        update.message.reply_text("Выберите дальнейшие действия:", reply_markup=keyboard)

        return BUILD_MAP

    return BUILD_MAP


def send_materials(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text

    if input_text == "Миша, давай по новой, все плохо...":
        reset_user_data(context)
        return start(update, context)

    if input_text == "Построить карту":
        language = context.user_data.get('language', 'Not specified')
        start_year = context.user_data.get('start_year', 'Not specified')
        finish_year = context.user_data.get('finish_year', 'Not specified')
        index = context.user_data.get('index', 'Not specified')
        query = context.user_data.get('query', 'Not specified')

        keyboard = ReplyKeyboardMarkup([["Миша, давай по новой, все плохо..."]],
                                       one_time_keyboard=True)
        text, map_png_data, map_svg_data, excel_data = building_map_and_exel(language, start_year, finish_year, index, query)
        update.message.reply_text(text, reply_markup=keyboard)
        update.message.reply_photo(photo=InputFile(BytesIO(map_png_data), filename='map.png'))
        update.message.reply_document(document=InputFile(BytesIO(map_png_data), filename='map.png'))
        update.message.reply_document(document=InputFile(BytesIO(map_svg_data), filename='map.svg'))
        update.message.reply_document(document=InputFile(BytesIO(excel_data), filename='data.xlsx'))
        update.message.reply_text("К сожалению, мои полномочия на этом все...\n")
        return BUILD_MAP  # Return a state when the condition is met

    else:
        update.message.reply_text("Выберите один из вариантов, используя кнопки.")
        return BUILD_MAP

    return BUILD_MAP


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Отменено.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, select_language)],
            START_YEAR: [MessageHandler(Filters.text & ~Filters.command, set_start_year)],
            FINISH_YEAR: [MessageHandler(Filters.text & ~Filters.command, set_finish_year)],
            INDEX: [MessageHandler(Filters.text & ~Filters.command, set_index)],
            QUERY_TERMS: [MessageHandler(Filters.text & ~Filters.command, set_query)],
            FORMULATE_QUERY: [MessageHandler(Filters.text & ~Filters.command, formulate_query)],
            BUILD_MAP: [MessageHandler(Filters.text & ~Filters.command, send_materials)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
