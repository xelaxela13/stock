def float_format(value):
    return '{0:.2f}'.format(value)


def generate_cache_key(prefix, key):
    return f'{prefix}_{key}'
