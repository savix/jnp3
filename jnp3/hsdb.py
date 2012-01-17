# -*- coding: utf-8 -*-

from django.conf import settings

from pyhs import Manager
from pyhs.exceptions import OperationalError


#manager_instance = Manager()

def manager():
    #return manager_instance
    return Manager()

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


def insert(table, columns, values, index_name=None, shard = ''):
    fields = zip(columns, encode_values(values))
    return manager().insert(settings.HS_DBNAME + str(shard), table, fields, index_name)


def update(table, columns, operation, old_values, new_values, \
        index_name=None, limit=0, offset=0, return_original=False, shard = ''):
    return manager().update(settings.HS_DBNAME + str(shard), table, operation, columns,
            encode_values(old_values), encode_values(new_values),
            index_name, limit, offset, return_original)


def find(table, columns, operation, values,
        index_name=None, limit=0, offset=0, shard = ''):
    rows = manager().find(settings.HS_DBNAME + str(shard), table, operation, columns, encode_values(values),
                        index_name, limit, offset)
    return [decode_row(row) for row in rows]


def get(table, columns, value, index_name=None, shard = ''):
    rows = manager().find(settings.HS_DBNAME + str(shard), table, '=', columns, (encode_value(value), ), index_name, 1, 0)
    if rows:
        return decode_row(rows[0])
    else:
        return None


def delete(table, columns, operation, values,  \
        index_name=None, limit=0, offset=0, return_original=False, shard = ''):
    return manager().delete(settings.HS_DBNAME + str(shard), table, operation, columns, encode_values(values),
            index_name, limit, offset, return_original)

def incr(table, columns, operation, values, steps=(1, ), index_name=None, limit=0, offset=0, return_original=False, shard = ''):
    result = manager().incr(settings.HS_DBNAME + str(shard), table, operation, columns, encode_values(values), encode_values(steps),
        index_name, limit, offset, return_original)
    if return_original:
        return [decode_row(row) for row in result]
    else:
        return result
