import requests
from bs4 import BeautifulSoup
import os.path
import csv
import pandas as pd


def get_save():
    # Путь к папке с CSV файлами
    folder_path = 'files/'

    # Создаем новый Excel файл
    excel_file = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Получаем список файлов в папке
    file_list = os.listdir(folder_path)

    # Проходимся по каждому файлу
    for file_name in file_list:
        # Проверяем расширение файла (допустим, что все файлы в папке - CSV)
        if file_name.endswith('.csv'):
            # Читаем CSV файл в DataFrame
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, delimiter=';')

            # Имя листа в Excel соответствует имени файла без расширения
            sheet_name = os.path.splitext(file_name)[0]

            # Записываем DataFrame в Excel лист
            df.to_excel(excel_file, sheet_name=sheet_name, index=False)

    # Сохраняем и закрываем Excel файл
    excel_file._save()
    excel_file.close()


def get_data(url, city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
    req = requests.get(url + 'catalog/', headers=headers)

    # Проверяем на наличие папки с городом, если нет, то создаем. folder_name - Обрезаем ссылку, чтобы получить название папки.
    folder_name = url.split('/')[2].split('.')[0]
    if url == 'https://www.russteels.ru/':
        folder_name = 'moscow'
        if os.path.exists(f'data/{folder_name}'):
            print("Папка уже существует!")
        else:
            os.mkdir(f'data/{folder_name}')
    else:
        if os.path.exists(f'data/{folder_name}'):
            print("Папка уже существует!")
        else:
            os.mkdir(f'data/{folder_name}')

    with open(f"data/{folder_name}/{folder_name}.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open(f"data/{folder_name}/{folder_name}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    # Получаем актуальный каталог категорий товаров.
    catalog_content = soup.find(class_='wraps', id='content').find('div', class_='catalog_section_list row items margin0 flexbox type_sections_3')
    amount_categories = catalog_content.find_all('li', class_='name')
    amount = 0 # Создаем количество категорий. Блоком кода ниже за каждую ссылку прибавляем к значению +1.
    # Заходим в каждую категорию и начинаем парсить.
    for amount_category in amount_categories:
        href = url + amount_category.find('a').get('href').replace('/', '', 1)
        try:
            if 'tsvetnoy_metall' in href:
                req = requests.get(url=href, headers=headers)
                folder_name_category = href.split('/')[-2]
                if os.path.exists(f'data/{folder_name}/{folder_name_category}'):
                    print("Папка уже существует!")
                else:
                    os.mkdir(f'data/{folder_name}/{folder_name_category}')

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html", "w",
                          encoding="utf-8") as file:
                    file.write(req.text)

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html",
                          encoding="utf-8") as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')
                all_products = soup.find_all('div', class_='simple-item')
                for product in all_products:
                    info_list = []
                    main_section = ''
                    two_section = ''
                    three_section = ''
                    product_size = ''
                    try:
                        product_name = product.find('div', class_='simple-item_name').text
                        product_full_price = product.find('div', class_='simple-item_price').text
                    except:
                        product_name = ''
                        product_full_price = ''
                    product_marka = ''
                    product_lenght = ''
                    availability = ''
                    product_measure = ''
                    product_gost = ''
                    product_weight = ''
                    product_hight = ''
                    product_width = ''
                    product_surface = ''
                    product_delivery = ''
                    product_type = ''
                    product_side = ''
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
                    with open(f'files/{city}.csv', 'a', encoding='utf-8', newline="") as file:
                        writer = csv.writer(file, delimiter=";")
                        writer.writerow(info_list)
                continue


            if 'truby_nerzhaveyushchie' in href:

                amount += 1

                req = requests.get(url=href, headers=headers)
                folder_name_category = href.split('/')[-2]
                if os.path.exists(f'data/{folder_name}/{folder_name_category}'):
                    print("Папка уже существует!")
                else:
                    os.mkdir(f'data/{folder_name}/{folder_name_category}')

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html", "w", encoding="utf-8") as file:
                    file.write(req.text)

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html", encoding="utf-8") as file:
                    src = file.read()


                soup = BeautifulSoup(src, 'lxml')
                # Определяем последнюю страницу с товаром в каталоге.
                if 'provoloka_svarochnaya/' in href:
                    page_last = '1'
                else:
                    try:
                        page_last = soup.find('div', class_='module-pagination').find_all('a', class_='dark_link')[-1].text
                    except Exception as ex:
                        page_last = '1'

                # Создаем цикл с товаром и начинаем парсить.

                for i in range(1, int(page_last) + 1):
                    req = requests.get(url=href + f'?PAGEN_1={i}', headers=headers)

                    if os.path.exists(f'data/{folder_name}/{folder_name_category}/{i}'):
                        print("Папка уже существует!")
                    else:
                        os.mkdir(f'data/{folder_name}/{folder_name_category}/{i}')


                    with open(f"data/{folder_name}/{folder_name_category}/{i}/{i}.html", "w", encoding="utf-8") as file:
                        file.write(req.text)

                    with open(f"data/{folder_name}/{folder_name_category}/{i}/{i}.html", encoding="utf-8") as file:
                        src = file.read()

                    soup = BeautifulSoup(src, 'lxml')

                    # Остановился на доставании href из товаров.
                    products_href = soup.find_all('div', class_='item-foto__picture')

                    page_products = len(products_href)
                    product_counters = 0
                    for product_href in products_href:
                        product_counters += 1
                        product_href = url + product_href.find('a').get('href').replace('/', '', 1)

                        req = requests.get(url=product_href, headers=headers)
                        folder_name_product = product_href.split('/')[-2]


                        with open(f"data/{folder_name}/{folder_name_category}/{i}/{folder_name_product}.html", "w", encoding="utf-8") as file:
                            file.write(req.text)

                        with open(f"data/{folder_name}/{folder_name_category}/{i}/{folder_name_product}.html", encoding="utf-8") as file:
                            src = file.read()


                        soup = BeautifulSoup(src, 'lxml')
                        try:
                            # Получаем текст основной категории
                            main_section = soup.find('div', id='navigation').find('div', id='bx_breadcrumb_2').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            main_section = ''

                        try:
                            # Подраздел 2
                            two_section = soup.find('div', id='bx_breadcrumb_3').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            two_section = ''

                        try:
                            # Подраздел 3
                            three_section = soup.find('div', id='bx_breadcrumb_4').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            three_section = ''



                        # Блок с продуктами. (Их может быть больше 1)
                        try:
                            products_block = soup.find('div', class_='flexbox flexbox--row flex-wrap align-items-normal product-action-container').find('div', class_='table-view flexbox flexbox--row').find_all('div', class_='table-view__item item bordered box-shadow main_item_wrapper table-view__item--has-stores')
                        except Exception:
                            continue

                        product_count = -1 # Необходим для подбора размера к определенному товару по индексу.

                        for product_block in products_block:
                            info_list = []
                            product_gost = ''
                            product_weight = ''
                            product_hight = ''
                            product_width = ''
                            product_surface = ''
                            product_delivery = ''
                            product_type = ''
                            product_side = ''
                            try:
                                # Название продукта
                                product_name = product_block.find('div', class_='item-title font_sm').text
                            except Exception:
                                product_name = ''

                            try:
                                # Цена
                                product_price = product_block.find('div', class_='item-price').find('span', class_='values_wrapper').find('span', class_='price_value').text
                            except Exception:
                                product_price = ''

                            try:
                                # Валюта
                                product_currency = product_block.find('div', class_='item-price').find('span', class_='values_wrapper').find('span', class_='price_currency').text
                            except Exception:
                                product_currency = ''

                            try:
                                # Единици измерения
                                product_measure = product_block.find('div', class_='item-price').find('span', class_='price_measure').text
                            except Exception:
                                product_measure = ''

                            try:
                                # Склейка ценника.
                                product_full_price = product_price + product_currency + product_measure
                            except Exception:
                                product_full_price = ''

                            try:
                                # Наличие.
                                availability = product_block.find('div', class_='quantity_block_wrapper').find('span', class_='value font_sxs').text
                            except Exception:
                                availability = ''


                            # Определяем длинну, размер и тип сплава.
                            soup = BeautifulSoup(src, 'lxml')
                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Размер' in title.text:
                                            product_size = value.text.strip()
                            except Exception:
                                product_size = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Марка стали' in title.text:
                                            product_marka = value.text.strip()
                            except Exception:
                                product_marka = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')

                                    if title and value:
                                        if 'Длина' in title.text:
                                            lengths = value.text.strip().split(', ')
                                            product_count += 1
                                            product_lenght = lengths[product_count] # Длинна продукта.

                            except Exception:
                                product_lenght = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'ГОСТ' in title.text:
                                            product_gost = value.text.strip()
                            except Exception:
                                product_gost = ''
                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Вес' in title.text:
                                            product_weight = value.text.strip()
                            except Exception:
                                product_weight = ''


                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Высота' in title.text:
                                            product_hight = value.text.strip()
                            except Exception:
                                product_hight = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Ширина' in title.text:
                                            product_width = value.text.strip()
                            except Exception:
                                product_width = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Стандартная поверхность' in title.text:
                                            product_surface = value.text.strip()
                            except Exception:
                                product_surface = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Поставка' in title.text:
                                            product_delivery = value.text.strip()
                            except Exception:
                                product_delivery = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Тип' in title.text:
                                            product_type = value.text.strip()
                            except Exception:
                                product_type = ''

                            try:
                                properties = soup.find_all('div', class_='properties__item--compact')
                                for prop in properties:
                                    title = prop.find('div', class_='properties__title')
                                    value = prop.find('div', class_='properties__value')
                                    if title and value:
                                        if 'Поверхность' in title.text:
                                            product_side = value.text.strip()
                            except Exception:
                                product_side = ''


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



                            with open (f'files/{city}.csv', 'a', encoding='utf-8', newline="") as file:
                                writer = csv.writer(file, delimiter=";")
                                writer.writerow(info_list)

                            print(f'Категория: {amount}. Страница {i} из {page_last}. Продукт номер {product_counters} из {page_products}')

                            # Ниже для остальных
            else:
                amount += 1

                req = requests.get(url=href, headers=headers)
                folder_name_category = href.split('/')[-2]
                if os.path.exists(f'data/{folder_name}/{folder_name_category}'):
                    print("Папка уже существует!")
                else:
                    os.mkdir(f'data/{folder_name}/{folder_name_category}')

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html", "w", encoding="utf-8") as file:
                    file.write(req.text)

                with open(f"data/{folder_name}/{folder_name_category}/{folder_name_category}.html", encoding="utf-8") as file:
                    src = file.read()

                soup = BeautifulSoup(src, 'lxml')
                if 'provoloka_svarochnaya/' in href:
                    page_last = '1'
                else:
                    try:
                        page_last = soup.find('div', class_='module-pagination').find_all('a', class_='dark_link')[-1].text
                    except Exception as ex:
                        page_last = '1'

                # Создаем цикл с товаром и начинаем парсить.

                for i in range(1, int(page_last) + 1):
                    req = requests.get(url=href + f'?PAGEN_1={i}', headers=headers)

                    if os.path.exists(f'data/{folder_name}/{folder_name_category}/{i}'):
                        print("Папка уже существует!")
                    else:
                        os.mkdir(f'data/{folder_name}/{folder_name_category}/{i}')

                    with open(f"data/{folder_name}/{folder_name_category}/{i}/{i}.html", "w", encoding="utf-8") as file:
                        file.write(req.text)

                    with open(f"data/{folder_name}/{folder_name_category}/{i}/{i}.html",encoding="utf-8") as file:
                        src = file.read()

                    soup = BeautifulSoup(src, 'lxml')

                    # Остановился на доставании href из товаров.
                    products_href = soup.find_all('div', class_='item-foto__picture')

                    page_products = len(products_href)
                    product_counters = 0
                    for product_href in products_href:
                        product_counters += 1
                        product_href = url + product_href.find('a').get('href').replace('/', '', 1)

                        req = requests.get(url=product_href, headers=headers)
                        folder_name_product = product_href.split('/')[-2]

                        with open(f"data/{folder_name}/{folder_name_category}/{i}/{folder_name_product}.html",
                                  "w", encoding="utf-8") as file:
                            file.write(req.text)

                        with open(f"data/{folder_name}/{folder_name_category}/{i}/{folder_name_product}.html",
                                  encoding="utf-8") as file:
                            src = file.read()

                        soup = BeautifulSoup(src, 'lxml')
                        try:
                            # Получаем текст основной категории
                            main_section = soup.find('div', id='navigation').find('div', id='bx_breadcrumb_2').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            main_section = ''

                        try:
                            # Подраздел 2
                            two_section = soup.find('div', id='bx_breadcrumb_3').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            two_section = ''

                        try:
                            # Подраздел 3
                            three_section = soup.find('div', id='bx_breadcrumb_4').find('a', class_='breadcrumbs__link colored_theme_hover_bg-el-svg').find('span').text
                        except Exception:
                            three_section = ''


                        product_count = -1  # Необходим для подбора размера к определенному товару по индексу.

                        info_list = []
                        product_gost = ''
                        product_weight = ''
                        product_hight = ''
                        product_width = ''
                        product_surface = ''
                        product_delivery = ''
                        product_type = ''
                        product_side = ''
                        product_size = ''
                        product_marka = ''
                        try:
                            # Название продукта
                            product_name = soup.find('h1', id='pagetitle').text
                        except Exception:
                            product_name = ''

                        try:
                            # Цена
                            product_price = soup.find('div', class_='prices_block').find('span', class_='values_wrapper').find('span', class_='price_value').text
                        except Exception:
                            product_price = ''

                        try:
                            # Валюта
                            product_currency = soup.find('div', class_='prices_block').find('span',class_='values_wrapper').find('span', class_='price_currency').text
                        except Exception:
                            product_currency = ''

                        try:
                            # Единици измерения
                            product_measure = soup.find('div', class_='prices_block').find('span', class_='price_measure').text
                        except Exception:
                            product_measure = ''

                        try:
                            # Склейка ценника.
                            product_full_price = product_price + product_currency + product_measure
                        except Exception:
                            product_full_price = ''

                        try:
                            # Наличие.
                            availability = soup.find('div', class_='item-stock quantity-more').find('span', class_='value font_sxs').text
                        except Exception:
                            availability = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Размер' in title.text:
                                        product_size = value.text.strip()
                        except Exception:
                            product_size = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Марка стали' in title.text:
                                        product_marka = value.text.strip()
                        except Exception:
                            product_marka = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')

                                if title and value:
                                    if 'Длина' in title.text:
                                        lengths = value.text.strip().split(', ')
                                        product_count += 1
                                        product_lenght = lengths[product_count]  # Длинна продукта.

                        except Exception:
                            product_lenght = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'ГОСТ' in title.text:
                                        product_gost = value.text.strip()
                        except Exception:
                            product_gost = ''
                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Вес' in title.text:
                                        product_weight = value.text.strip()
                        except Exception:
                            product_weight = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Высота' in title.text:
                                        product_hight = value.text.strip()
                        except Exception:
                            product_hight = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Ширина' in title.text:
                                        product_width = value.text.strip()
                        except Exception:
                            product_width = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Стандартная поверхность' in title.text:
                                        product_surface = value.text.strip()
                        except Exception:
                            product_surface = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Поставка' in title.text:
                                        product_delivery = value.text.strip()
                        except Exception:
                            product_delivery = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Тип' in title.text:
                                        product_type = value.text.strip()
                        except Exception:
                            product_type = ''

                        try:
                            properties = soup.find_all('div', class_='properties__item--compact')
                            for prop in properties:
                                title = prop.find('div', class_='properties__title')
                                value = prop.find('div', class_='properties__value')
                                if title and value:
                                    if 'Поверхность' in title.text:
                                        product_side = value.text.strip()
                        except Exception:
                            product_side = ''

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

                        with open(f'files/{city}.csv', 'a', encoding='utf-8', newline="") as file:
                            writer = csv.writer(file, delimiter=";")
                            writer.writerow(info_list)

                        print(
                            f'Категория: {amount}. Страница {i} из {page_last}. Продукт номер {product_counters} из {page_products}')
        except Exception:
            continue

def main():

    # Список городов
    city_list = []
    with open('urls.txt', 'r') as file:
        # Читаем файл построчно
        for line in file:
            line = line.strip()
            city_list.append(line)

    if os.path.exists(f'files'):
        print("Папка уже существует!")
    else:
        os.mkdir(f'files')
    if os.path.exists(f'data'):
        print("Папка уже существует!")
    else:
        os.mkdir(f'data')
    print(city_list)

    for j in range(0, len(city_list)):
        if city_list[j] == 'https://chelyabinsk.russteels.ru/':
            city = 'Челябинск'
        elif city_list[j] == 'https://voronezh.russteels.ru/':
            city = 'Воронеж'
        elif city_list[j] == 'https://krasnodar.russteels.ru/':
            city = 'Краснодар'
        elif city_list[j] == 'https://novorossijsk.russteels.ru/':
            city = 'Новороссийск'
        elif city_list[j] == 'https://nalchik.russteels.ru/':
            city = 'Нальчик'
        elif city_list[j] == 'https://nn.russteels.ru/':
            city = 'Нижний Новгород'
        elif city_list[j] == 'https://novosibirsk.russteels.ru/':
            city = 'Новосибирск'
        elif city_list[j] == 'https://pyatigorsk.russteels.ru/':
            city = 'Пятигорск'
        elif city_list[j] == 'https://samara.russteels.ru/':
            city = 'Самара'
        elif city_list[j] == 'https://spb.russteels.ru/':
            city = 'Санкт-Петербург'
        elif city_list[j] == 'https://ufa.russteels.ru/':
            city = 'Уфа'
        elif city_list[j] == 'https://cheboksary.russteels.ru/':
            city = 'Чебоксары'
        elif city_list[j] == 'https://russteels.ru/':
            city = 'Москва'



        with open(f'files/{city}.csv', 'w', encoding='utf-8', newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                ("Основной раздел", "Подраздел", "Подраздел2", "Размер", "Наименование", "Сплав","Длинна", "Цена","Наличие", "Мера", "ГОСТ", "Масса", "Высота", "Ширина", "Стандартная поверхность", "Доставка", "Тип", "Поверхность")
            )


        print(f'Начал парсить город: {city}')

        get_data(f'{city_list[j]}', city)
    get_save()
    print('Парсинг завершен.')

if __name__ == '__main__':
    main()