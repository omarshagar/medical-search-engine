import os

__all__ = ['Unit', 'file_size']


class Unit:

    Bits = 0
    Bytes = 1
    KB = 2
    MB = 3
    GB = 4

    @staticmethod
    def get(unit: str):

        return getattr(Unit, unit)


def file_size(path, unit: Unit):

    size = os.path.getsize(path)

    if unit == Unit.Bytes:

        return size

    elif unit == Unit.KB:

        return size >> 10

    elif unit == Unit.MB:

        return size >> 20

    elif unit == Unit.GB:

        return size >> 30

    else:

        raise ValueError(f'Unsupported unit type, unit={str(unit)}')
