import re
from string import Formatter

class Style:
    RESET_ALL = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    HIDE = 8
    STRIKE = 9
    NORMAL = 22

class Fore:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97

class Back:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107

class TokenType:
    TEXT = 1
    ANSI = 2
    LEVEL = 3
    CLOSING = 4

class AnsiParser:
    _style = ansi_escape({'b': Style.BOLD, 'd': Style.DIM, 'n': Style.NORMAL, 'h': Style.HIDE, 'i': Style.ITALIC, 'l': Style.BLINK, 's': Style.STRIKE, 'u': Style.UNDERLINE, 'v': Style.REVERSE, 'bold': Style.BOLD, 'dim': Style.DIM, 'normal': Style.NORMAL, 'hide': Style.HIDE, 'italic': Style.ITALIC, 'blink': Style.BLINK, 'strike': Style.STRIKE, 'underline': Style.UNDERLINE, 'reverse': Style.REVERSE})
    _foreground = ansi_escape({'k': Fore.BLACK, 'r': Fore.RED, 'g': Fore.GREEN, 'y': Fore.YELLOW, 'e': Fore.BLUE, 'm': Fore.MAGENTA, 'c': Fore.CYAN, 'w': Fore.WHITE, 'lk': Fore.LIGHTBLACK_EX, 'lr': Fore.LIGHTRED_EX, 'lg': Fore.LIGHTGREEN_EX, 'ly': Fore.LIGHTYELLOW_EX, 'le': Fore.LIGHTBLUE_EX, 'lm': Fore.LIGHTMAGENTA_EX, 'lc': Fore.LIGHTCYAN_EX, 'lw': Fore.LIGHTWHITE_EX, 'black': Fore.BLACK, 'red': Fore.RED, 'green': Fore.GREEN, 'yellow': Fore.YELLOW, 'blue': Fore.BLUE, 'magenta': Fore.MAGENTA, 'cyan': Fore.CYAN, 'white': Fore.WHITE, 'light-black': Fore.LIGHTBLACK_EX, 'light-red': Fore.LIGHTRED_EX, 'light-green': Fore.LIGHTGREEN_EX, 'light-yellow': Fore.LIGHTYELLOW_EX, 'light-blue': Fore.LIGHTBLUE_EX, 'light-magenta': Fore.LIGHTMAGENTA_EX, 'light-cyan': Fore.LIGHTCYAN_EX, 'light-white': Fore.LIGHTWHITE_EX})
    _background = ansi_escape({'K': Back.BLACK, 'R': Back.RED, 'G': Back.GREEN, 'Y': Back.YELLOW, 'E': Back.BLUE, 'M': Back.MAGENTA, 'C': Back.CYAN, 'W': Back.WHITE, 'LK': Back.LIGHTBLACK_EX, 'LR': Back.LIGHTRED_EX, 'LG': Back.LIGHTGREEN_EX, 'LY': Back.LIGHTYELLOW_EX, 'LE': Back.LIGHTBLUE_EX, 'LM': Back.LIGHTMAGENTA_EX, 'LC': Back.LIGHTCYAN_EX, 'LW': Back.LIGHTWHITE_EX, 'BLACK': Back.BLACK, 'RED': Back.RED, 'GREEN': Back.GREEN, 'YELLOW': Back.YELLOW, 'BLUE': Back.BLUE, 'MAGENTA': Back.MAGENTA, 'CYAN': Back.CYAN, 'WHITE': Back.WHITE, 'LIGHT-BLACK': Back.LIGHTBLACK_EX, 'LIGHT-RED': Back.LIGHTRED_EX, 'LIGHT-GREEN': Back.LIGHTGREEN_EX, 'LIGHT-YELLOW': Back.LIGHTYELLOW_EX, 'LIGHT-BLUE': Back.LIGHTBLUE_EX, 'LIGHT-MAGENTA': Back.LIGHTMAGENTA_EX, 'LIGHT-CYAN': Back.LIGHTCYAN_EX, 'LIGHT-WHITE': Back.LIGHTWHITE_EX})
    _regex_tag = re.compile('\\\\?</?((?:[fb]g\\s)?[^<>\\s]*)>')

    def __init__(self):
        self._tokens = []
        self._tags = []
        self._color_tokens = []

class ColoringMessage(str):
    __fields__ = ('_messages',)

    def __format__(self, spec):
        return next(self._messages).__format__(spec)

class ColoredMessage:

    def __init__(self, tokens):
        self.tokens = tokens
        self.stripped = AnsiParser.strip(tokens)

class ColoredFormat:

    def __init__(self, tokens, messages_color_tokens):
        self._tokens = tokens
        self._messages_color_tokens = messages_color_tokens

class Colorizer:
    def __init__(self):
        self.ansi_parser = AnsiParser()
        self.formatter = Formatter()
