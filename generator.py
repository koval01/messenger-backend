from random import choice
from string import printable


def replacer(s: str) -> str:
    for i in ['/', '?', '#', '"', '\\']:
        s = s.replace(i, '')
    return s


def generate_token() -> str:
    return replacer("".join([choice(printable[:-6]) for _ in range(255)]))
