import math


def get_pretty_file_size(size_in_bytes: int) -> str:
    exponent = math.floor(math.log(size_in_bytes, 1024))
    unit = {
        0: 'B',
        1: 'KB',
        2: 'MB',
        3: 'GB',
    }[exponent]
    size = size_in_bytes / (1024 ** exponent)
    return '{size} {unit}'.format(size=size, unit=unit)
