import re


def capitalize(string):
    return string.capitalize()


def title(string):
    return string.title()


def lower(string):
    return string.lower()


def lcfirst(string):
    return string[0].lower() + string[1:]


def upper(string):
    return string.upper()


def camelcase(string):
    return string.title().replace(' ', '').replace('-', '').replace('_', '')


def snakecase(string):
    return re.sub('([A-Z])', '_\\1', string).lower().replace('-', '_').lstrip('_')


def kebabcase(string):
    return re.sub('([A-Z])', '-\\1', string).lower().replace('_', '-').lstrip('-')


def remove(string, part):
    return string.replace(part, '')


def replace(string, old, new):
    return string.replace(old, new)


def escape_backslash(string):
    return string.replace('\\', '\\\\')
