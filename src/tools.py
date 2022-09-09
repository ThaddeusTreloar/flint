from typing import Any, Callable, List, no_type_check, Dict, Union, Type, Optional


def Functor(f: Any, g: Any) -> Callable[[Any], Any]:
    '''
    Returns g( f() ) as h(x)
    '''
    return lambda x: g(f(x))


def coupler(cls: Any, att: Any, default: Any) -> Any:
    if hasattr(cls, att):
        return getattr(cls, att)
    else:
        return default


def coupler_func(cls: Any, func: Any, *args: Any) -> Any:
    if hasattr(cls, func):
        return getattr(cls, func)(args)
    else:
        return None


def flatten(list: List):

    flat = []

    for item in list:

        if isinstance(item, List):
            flat.extend(flatten(item))
        else:
            flat.append(item)

    return flat


@no_type_check
def issubclassNoType(object: Any, class_: Any) -> bool:
    return issubclass(object, class_)


@no_type_check
def isinstanceNoType(object: Any, class_: Any) -> bool:
    return isinstance(object, class_)


def recursiveDictionaryFold(a: Dict, b: Dict) -> Dict:

    for key, value in b.items():
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                a[key] = recursiveDictionaryFold(a[key], b[key])
            elif isinstance(a[key], dict):
                a[key] = recursiveDictionaryFold(a[key], {key: value})
            elif isinstance(b[key], dict):
                a[key] = recursiveDictionaryFold(b[key], {key: a[key]})
            else:
                a[key] = value

        else:
            a[key] = value

    return a
