
def Functor(f, g):
    return lambda x: g(f(x))

def coupler(cls, att, default):
    if hasattr(cls, att):
        return getattr(cls, att)
    else:
        return default

def coupler_func(cls, func, *args):
    if hasattr(cls, func):
        return getattr(cls, func)(args)
    else:
        return None