import functools
import time


def handle_exceptions(func):
    """ This function is used as a decorator to wrap the implemented method avoiding weird crashes"""
    @functools.wraps(func)  # supports introspection
    def wrapper_decorator(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            print("Something went wrong ...")
            print(e)
    return wrapper_decorator


def timeit(text):
    """ Meauring function execution time and printing it."""
    def decorator_timeit(func):
        @functools.wraps(func)
        def timed(*args, **kw):
            ts = time.time()
            result = func(*args, **kw)
            te = time.time()

            print(text + "::time spent " + str(te-ts) + " seconds")
            return result

        return timed
    return decorator_timeit
