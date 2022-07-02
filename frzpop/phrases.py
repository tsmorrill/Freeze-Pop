def p_gen(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func(*args):
            return next(generator)
        return(func)
    return wrapper


@p_gen
def make_plain_hunt(phrase):
    """Return a phrase generator which outputs plain hunt method
    permutations of phrase."""
    length = len(phrase)
    l_mod_2 = length % 2
    phrase_copy = phrase.copy()

    pairs_count = length // 2
    period = 2*length

    phrase_list = [phrase_copy]
    for t in range(period - 1):
        t_mod_2 = t % 2
        pairs_adjust = t_mod_2 * (1 - l_mod_2)  # don't adjust if length is odd
        for n in range(pairs_count - pairs_adjust):
            index = 2*n + t_mod_2
            phrase[index], phrase[index + 1] = phrase[index + 1], phrase[index]
        phrase_copy = phrase.copy()
        phrase_list.append(phrase_copy)

    i = 0
    while True:
        yield phrase_list[i]
        i += 1
        i %= period


if __name__ == "__main__":
    phrase = [4, 3, 2, 1]
    generator = make_plain_hunt(phrase)
    for i in range(10):
        print(i, generator())
