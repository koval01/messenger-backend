import re
from string import punctuation

from config import EMOJI as emoji


class Init:
    def __init__(self, text: str) -> None:
        self.text = text.lstrip().rstrip()
        self.cyrillic_letters = "йцукенгшщзхъёфывапролджэячсмитьбюіїґє"
        self.emoji = emoji

    def default(self) -> str:
        pattern = self.cyrillic_letters + self.cyrillic_letters.upper() \
                  + punctuation + self.emoji
        return re.sub(r"[^A-Za-z0-9\s%s]" % pattern, "", self.text)

    def wide(self) -> str:
        special = " _\-"
        pattern = self.cyrillic_letters + self.cyrillic_letters.upper() \
                  + special + self.emoji
        return re.sub(r"[^A-Za-z0-9%s]" % pattern, "", self.text)
