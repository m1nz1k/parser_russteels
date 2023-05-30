# import os
# import pandas as pd
# import xlsxwriter
#
# def merge_csv_excel_files(folder_path, output_file):
#     # Создаем пустой файл Excel с помощью XlsxWriter
#     writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
#     workbook = writer.book
#
#     # Читаем все файлы в заданной папке
#     for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         if file_name.endswith('.csv'):
#             # Обрабатываем файлы CSV
#             sheet_name = os.path.splitext(file_name)[0]  # Используем имя файла без расширения в качестве имени листа
#             df = pd.read_csv(file_path)
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#         elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
#             # Обрабатываем файлы Excel
#             sheet_name = os.path.splitext(file_name)[0]  # Используем имя файла без расширения в качестве имени листа
#             df = pd.read_excel(file_path)
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#
#     # Закрываем созданный файл Excel
#     writer._save()
#     print("Объединение файлов завершено. Результат сохранен в", output_file)
#
# # Пример использования
#
#
# # Пример использования
# folder_path = f'files/'  # Укажите путь к папке, содержащей CSV и Excel файлы
# output_file = 'result.xlsx'  # Укажите путь и имя выходного файла
#
# merge_csv_excel_files(folder_path, output_file)
import os
import pandas as pd

def merge_csv_excel_files(folder_path, output_file):
    # Список для хранения объединенных данных
    merged_data = []

    # Читаем все файлы в заданной папке
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.csv'):
            # Обрабатываем файлы CSV
            df = pd.read_csv(file_path)
            merged_data.append(df)
        elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Обрабатываем файлы Excel
            df = pd.read_excel(file_path)
            merged_data.append(df)

    # Объединяем данные
    merged_df = pd.concat(merged_data, ignore_index=True)

    # Сохраняем объединенные данные в формате CSV
    merged_df.to_csv(output_file, index=False)
    print("Объединение файлов завершено. Результат сохранен в", output_file)

# Пример использования
folder_path = '/путь/к/папке'  # Укажите путь к папке, содержащей CSV и Excel файлы
output_file = '/путь/к/выходному/файлу.csv'  # Укажите путь и имя выходного файла в формате CSV

merge_csv_excel_files(folder_path, output_file)

info_list.append(main_section)
info_list.append(two_section)
info_list.append(three_section)
info_list.append(product_size)
info_list.append(product_name)
info_list.append(product_marka)
info_list.append(product_lenght)
info_list.append(product_full_price)
info_list.append(availability)
info_list.append(product_measure)
info_list.append(product_gost)
info_list.append(product_weight)
info_list.append(product_hight)
info_list.append(product_width)
info_list.append(product_surface)
info_list.append(product_delivery)
info_list.append(product_type)
info_list.append(product_side)
