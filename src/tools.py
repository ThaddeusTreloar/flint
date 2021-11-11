def Functor(f, g):
    return lambda x: g(f(x))