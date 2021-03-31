from functools import wraps
from time import perf_counter


def elapsed(*args, mut={}):
    try:
        mut[args[0]] = args[1]
    except IndexError:
        return mut[args[0]]


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.pop('timed', False):
            start = perf_counter()
            res = f(*args, **kwargs)
            elapsed(res, format_time(perf_counter() - start))
            return res
        else:
            return f(*args, **kwargs)

    return wrapper


def format_time(time):
    if time < 10 ** -3:
        return f"{time * (10 ** 6):.2f} µs"
    elif 10 ** -3 < time <= 10 ** -1:
        return f"{time * (10 ** 3):.2f} ms"
    else:
        if time < 60:
            return f"{time:.2f} s"
        else:
            return f"{time / 60:.2f} min"
