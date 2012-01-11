# -*- coding: utf-8 -*-

from django.conf import settings

from pyhs import Manager
from pyhs.exceptions import OperationalError


manager = Manager()


def encode_value(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return str(value)


def encode_values(values):
    return [encode_value(value) for value in values]


def decode_value(value):
    return value.decode('utf-8')


def decode_values(values):
    return [decode_value(value) for value in values]


def decode_row(row):
    return {column: decode_value(value) for column, value in row}


def insert(table, columns, values, index_name=None):
    fields = zip(columns, encode_values(values))
    return manager.insert(settings.HS_DBNAME, table, fields, index_name)


def update(table, columns, operation, old_values, new_values, \
        index_name=None, limit=0, offset=0, return_original=False):
    manager = Manager()
    return manager.update(settings.HS_DBNAME, table, operation, columns,
            encode_values(old_values), encode_values(new_values),
            index_name, limit, offset, return_original)


def get(table, columns, value):
    row = manager.get(settings.HS_DBNAME, table, columns, encode_value(value))
    if row:
        return decode_row(row)
    else:
        return None


def delete(table, columns, operation, values,  \
        index_name=None, limit=0, offset=0, return_original=False):
    return manager.delete(settings.HS_DBNAME, table, operation, columns, encode_values(values),
            index_name, limit, offset, return_original)
