import csv
import random
import string

import openpyxl

from django.core.paginator import Paginator

from .models import Link


def generate_short_hash(length=6):
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


def save_url_mapping(url):
    while True:
        short_hash = generate_short_hash()
        if not Link.objects.filter(short_hash=short_hash).exists():
            break
    Link.objects.create(original_url=url, short_hash=short_hash)
    return short_hash


def get_sorted_links(sort_by='views_counter'):
    links = Link.objects.all().order_by(sort_by)
    return links


def get_paginated_links(links, page_size=10, page_number=1):
    paginator = Paginator(links, page_size)
    links = paginator.get_page(page_number)
    return links


def create_csv_file(links):
    with open('statistics.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Оригинальная ссылка', 'Хеш ссылки', 'Количество переходов']
        )
        for link in links:
            writer.writerow(
                [link.original_url, link.short_hash, link.views_counter]
            )


def create_xlsx_file(data):
    wb = openpyxl.Workbook()
    ws = wb.active

    header_row = [
        'id',
        'Оригинальная ссылка',
        'Хеш ссылки',
        'Количество переходов',
    ]
    for col_num, header_title in enumerate(header_row, 1):
        ws.cell(row=1, column=col_num, value=header_title)

    for row_num, data_row in enumerate(data, 2):
        ws.cell(row=row_num, column=1, value=data_row.id)
        ws.cell(row=row_num, column=2, value=data_row.original_url)
        ws.cell(row=row_num, column=3, value=data_row.short_hash)
        ws.cell(row=row_num, column=4, value=data_row.views_counter)

    wb.save("statistics.xlsx")
