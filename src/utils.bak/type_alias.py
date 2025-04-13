"""Type Aliases.

Type aliases for custom data types.
"""


__all__ = [
    'JSON_DICT',
    'JSON_LIST',
    'JSON_TYPE',
    'JSON_UNITS',
    'JSON_VALUE'
]

type JSON_UNITS = None | bool | int | float | str
type JSON_VALUE = JSON_UNITS | 'JSON_LIST' | 'JSON_DICT'
type JSON_LIST = list[JSON_VALUE]
type JSON_DICT = dict[str, JSON_VALUE]
# noinspection PyUnresolvedReferences
type JSON_TYPE = 'JSON_LIST' | 'JSON_DICT'
