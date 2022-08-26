from typing import Any, Callable


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
