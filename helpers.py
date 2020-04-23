import random
import string


def string_generator(size=6, chars=string.ascii_lowercase):
    name = ''.join(random.choice(chars) for _ in range(size))
    return name
