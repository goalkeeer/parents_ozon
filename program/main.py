import csv
import traceback
from collections import defaultdict
from itertools import islice

import openpyxl
import xlsxwriter
from tqdm import tqdm

from browsers import BrowserException
from services import TradeLockService
from utils import write_log, write_interim_result


def get_item_from_products_csv() -> dict:
    items = defaultdict(dict)
    with open('products.csv') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in islice(csv_reader, 1, None):
            name = row[0]
            stock_count = row[4]
            reserve_count = row[5]
            items[name] = {'stock_count': stock_count,
                           'reserve_count': reserve_count}
    return items


def get_items_from_excel():
    workbook = openpyxl.load_workbook('products.csv')
    worksheet = workbook.worksheets[1]

    return [worksheet.cell(r, 1).value for r in range(5, worksheet.max_row+1)]


def write_excel_result(items):
    headers = ('Наименование', 'Кол-во на озоне', 'Зарезервировано на озоне',
               'Кол-во на сайте', 'Цена на сайте')
    workbook = xlsxwriter.Workbook('result.xlsx', {'constant_memory': True})
    bold = workbook.add_format({'bold': True})

    bg_red = workbook.add_format()
    bg_red.set_pattern(1)
    bg_red.set_bg_color('red')

    bg_yellow = workbook.add_format()
    bg_yellow.set_pattern(1)
    bg_yellow.set_bg_color('yellow')

    worksheet = workbook.add_worksheet()

    for i, header in enumerate(headers):
        worksheet.write(0, i, header, bold)

    for i, (name, values) in enumerate(items.items()):
        bg = None
        if 'error' in values:
            row = (name, values['error'])
            bg = bg_red
        else:
            row = (name, values['stock_count'], values['reserve_count'],
                   values['count'], values['price'])
            if int(values['stock_count']) > (int(values['count']) / 1.5):
                bg = bg_yellow
        for n, value in enumerate(row):
            worksheet.write(i + 1, n, value, bg)

    workbook.close()


if __name__ == '__main__':
    items = get_item_from_products_csv()

    service = TradeLockService(user, password)
    for item_name in tqdm(items.keys()):
        try:
            data = service.get_item_data(item_name)
        except BrowserException as error:
            data = {'error': str(error)}
        except Exception as error:
            print(error)
            tb = traceback.format_exc()
            write_log(str(tb))
            data = {'error': 'непонятная ошибка'}

        items[item_name].update(data)
        write_interim_result(f'{item_name}: {items[item_name]}')
    service.quit()

    write_excel_result(items)
