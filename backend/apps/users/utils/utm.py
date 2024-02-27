def get_utm_dict(cookies_str, prefix=None):
    utm_dict = {}
    for val in cookies_str.split():
        if prefix:
            if val.startswith(f'{prefix}utm_') and not val.endswith(
                    '=;') and not val.endswith('='):
                value = val.replace(prefix, '')
            else:
                continue

        elif (val.startswith('utm_') and not val.endswith(
                '=;') and not val.endswith('=')):
            value = val
        else:
            continue
        if value.endswith(';'):
            value, sep, end = value.rpartition(';')
        key, val, *other = value.split('=')
        utm_dict[key] = val
    return utm_dict
