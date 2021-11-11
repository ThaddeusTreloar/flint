from oslash import *

def sd(x):
    return Just(x)

def ric(y):
    return Just(y)

def mos(x, y):

    return x, y

Just(lambda x,y: x*y) % Just(5) * Just(3)