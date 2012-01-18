# -*- coding: utf-8 -*-

from django.conf import settings

from pyhs import Manager
from pyhs.exceptions import OperationalError

shards_by_table = {}

for shard in settings.HS_SHARDS:
    for table in shard['TABLES']:
        try:
            shards_by_table[table].append(shard)
        except KeyError:
            shards_by_table[table] = [shard]

#manager_instance = Manager()

def manager(table, shard_seed):
    shards = shards_by_table[table]
    shard = shards[shard_seed % len(shards)]
    return Manager(shard['READ_SERVERS'], shard['WRITE_SERVERS']), shard['DATABASE']

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


def insert(table, columns, values, index_name=None, shard_seed=0):
    fields = zip(columns, encode_values(values))
    man, db = manager(table, shard_seed)
    return man.insert(db, table, fields, index_name)


def update(table, columns, operation, old_values, new_values, \
        index_name=None, limit=0, offset=0, return_original=False, shard_seed=0):
    man, db = manager(table, shard_seed)
    return man.update(db, table, operation, columns,
            encode_values(old_values), encode_values(new_values),
            index_name, limit, offset, return_original)


def find(table, columns, operation, values,
        index_name=None, limit=0, offset=0, shard_seed=0):
    man, db = manager(table, shard_seed)
    rows = man.find(db, table, operation, columns, encode_values(values),
                        index_name, limit, offset)
    return [decode_row(row) for row in rows]


def get(table, columns, value, index_name=None, shard_seed=0):
    man, db = manager(table, shard_seed)
    rows = man.find(db, table, '=', columns, (encode_value(value), ), index_name, 1, 0)
    if rows:
        return decode_row(rows[0])
    else:
        return None


def delete(table, columns, operation, values,  \
        index_name=None, limit=0, offset=0, return_original=False, shard_seed=0):
    man, db = manager(table, shard_seed)
    return man.delete(db, table, operation, columns, encode_values(values),
            index_name, limit, offset, return_original)

def incr(table, columns, operation, values, steps=(1, ), index_name=None, limit=0, offset=0, return_original=False,
        shard_seed=0):
    man, db = manager(table, shard_seed)
    result = man.incr(db, table, operation, columns, encode_values(values), encode_values(steps),
        index_name, limit, offset, return_original)
    if return_original:
        return [decode_row(row) for row in result]
    else:
        return result
