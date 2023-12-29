from io import BytesIO


def building_map_and_exel(language, start_year, finish_year, index, query):
    fake = 'WARNING MASSAGE!!!\n it test materials, this doesnt match with your request!!!'

    # Replace these paths with the actual paths to your files
    map_png_path = '/Users/nikitasavvin/Desktop/Учеба/work_cases/tg_bot/result/en_ru_year_semantic_map.png'
    map_svg_path = '/Users/nikitasavvin/Desktop/Учеба/work_cases/tg_bot/result/en_ru_year_semantic_map.svg'
    excel_path = '/Users/nikitasavvin/Desktop/Учеба/work_cases/tg_bot/result/result_table_formatted_headers_ru.xlsx'

    # Read file contents as bytes
    with open(map_png_path, 'rb') as map_png_file:
        map_png_data = map_png_file.read()

    with open(map_svg_path, 'rb') as map_svg_file:
        map_svg_data = map_svg_file.read()

    with open(excel_path, 'rb') as excel_file:
        excel_data = excel_file.read()

    return fake, map_png_data, map_svg_data, excel_data

