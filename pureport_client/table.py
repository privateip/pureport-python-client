# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import


def get_property(path, obj):
    for item in path.split('.'):

        if isinstance(obj, (list, dict)):
            obj = obj.get(item)

        elif isinstance(obj, list):
            try:
                item = int(item)
                obj = obj[item]
            except (IndexError, ValueError):
                obj = None

        else:
            obj = getattr(obj, item, None)

        if obj is None:
            break
    return obj


def truncate(value, width):
    if len(value) > width - 4:
        value = value[:width - 4]
        value += '...'
    return value


def column(width, path, label=None):
    label = label or path.title()
    label = truncate(label, width)
    return (width, path, label)


def render(columns, data):
    assert isinstance(data, list), "table data must be of type list"

    columns = tuple([column(*item) for item in columns])
    rows = list()

    header_row = ""
    for width, path, label in columns:
        header_row += "{0:<{1}}".format(label.upper(), width)
    rows.append(header_row)

    data_rows = list()
    for item in data:
        data_row = ""
        for width, path, _ in columns:
            value = get_property(path, item)
            value = truncate(str(value), width)
            data_row += "{0:<{1}}".format(value, width)
        data_rows.append(data_row)
    rows.extend(data_rows)
    return "\n".join(rows)
