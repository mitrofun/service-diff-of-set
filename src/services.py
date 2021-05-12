from typing import Optional, Union

from loguru import logger
import xlrd
from openpyxl import load_workbook


def _get_target_list(col_title: str, sheet, table_titles: tuple) -> list:
    result = []
    col_number = table_titles.index(col_title) + 1
    for row_number in range(2, sheet.max_row + 1):
        result.append(sheet.cell(row_number, col_number).value)
    return result


def get_list_for_comparison_with_xlrd(filename: str):
    before_list = []
    after_list = []
    wb = xlrd.open_workbook(filename)
    for sheet in wb.sheets():
        ws = wb[sheet.name]
        try:
            table_titles = list(map(lambda x: x.value, ws.row(0)))
            if 'before' and 'after' not in table_titles:
                return
            index_before = table_titles.index('before')
            before_list = [int(i) for i in ws.col_values(index_before)[1:] if i != '']
            index_after = table_titles.index('after')
            after_list = [int(i) for i in ws.col_values(index_after)[1:] if i != '']
        except IndexError:
            logger.warning(f'Clear worksheet "{sheet.name}" in file: {filename}.')
    return before_list, after_list


def get_list_for_comparison_with_openpyxl(filename: str) -> \
        Optional[tuple[list[Union[int, None]], list[Union[int, None]]]]:
    before_list = []
    after_list = []
    wb = load_workbook(filename=filename)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        try:
            table_titles = next(ws.values)
            if 'before' and 'after' not in table_titles:
                return
            before_list = _get_target_list('before', ws, table_titles)
            after_list = _get_target_list('after', ws, table_titles)
        except StopIteration:
            logger.warning(f'Clear worksheet "{sheet_name}" in file: {filename}.')
    wb.close()
    return before_list, after_list


use_method = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': get_list_for_comparison_with_openpyxl,
    'application/vnd.ms-excel': get_list_for_comparison_with_xlrd,
}


def get_lists_for_comparison(content_type: str, filename: str) -> \
        Optional[tuple[list[Union[int, None]], list[Union[int, None]]]]:
    try:
        return use_method[content_type](filename)
    except KeyError:
        logger.warning(f'Not supported content type "{content_type}" in file: {filename}.')
