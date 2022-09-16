from scre.core.pattern import Pattern
from scre.core.compile import compile

def match(pattern, string, flags=0):
    if isinstance(pattern, Pattern):
        return pattern.match(string, flags=flags)
    else:
        return compile(pattern, flags).match(string)

def fullmatch(pattern, string, flags=0):
    if isinstance(pattern, Pattern):
        return pattern.fullmatch(string, flags=flags)
    else:
        return compile(pattern, flags).fullmatch(string)

def search(pattern, string, flags=0):
    return compile(pattern, flags).search(string)

def sub(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).sub(repl, string, count)

def subn(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).subn(repl, string, count)

def split(pattern, string, maxsplit=0, flags=0):
    return compile(pattern, flags).split(string, maxsplit)

def findall(pattern, string, flags=0):
    return compile(pattern, flags).findall(string)

def finditer(pattern, string, flags=0):
    return compile(pattern, flags).finditer(string)

# SPECIAL_CHARS
# closing ')', '}' and ']'
# '-' (a range in character set)
# '&', '~', (extended character set operations)
# '#' (comment) and WHITESPACE (ignored) in verbose mode
_special_chars_map = {i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}

def escape(pattern):
    """
    Escape special characters in a string.
    """
    if isinstance(pattern, str):
        return pattern.translate(_special_chars_map)
    else:
        pattern = str(pattern, 'latin1')
        return pattern.translate(_special_chars_map).encode('latin1')