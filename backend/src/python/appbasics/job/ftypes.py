import logging

log = logging.getLogger(__name__)

# def mainType(dataField):
#     dtype = None
#     stype = str(dataField.type)
#     if stype.startswith('list'):
#         dtype = list
#     elif stype.find('typing.Optional')>=0:
#         mg = re.search(r'typing.Optional[(.*?)]', stype)
#         if mg:
#             stype2 = mg.group(1)
#             dtype = stype2
#     else:
#         dtype = str
#     if dtype is None:
#         log.warning(f'Cannot find the main type of {dataField}, use str')
#         dtype = str
#     return dtype

# def typesOfField(dataField):
#     return typing.get_args(dataField)

# def elementTypesOfListField(listField):
#     return typing.get_args(listField)


def typedValue(value: str):
    x = None
    for T in (int, float, str):
        try:
            x = T(value)
        except ValueError:
            pass
        if x is not None:
            break
    if x is None:
        x = value
    return x

def keyValueToTuple(kv_word):
    key, value = None, None
    i = kv_word.find(':')
    if i>0:
        key = kv_word[0:i]
        value = typedValue(kv_word[i+1:])
    else:
        log.warning(f'Key:Value from word {kv_word} cannot be decoded')
    return (key, value)
