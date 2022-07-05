def water():
    print("Refreshing!")


def p_gen(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func(*args):
            return next(generator)
        return(func)
    return wrapper
