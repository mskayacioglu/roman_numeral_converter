# converter.py
import re

_ROMAN_RE = re.compile(r"""
    M{0,3}
    (CM|CD|D?C{0,3})
    (XC|XL|L?X{0,3})
    (IX|IV|V?I{0,3})
""", re.VERBOSE)

_ROMAN_TABLE = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

def int_to_roman(n: int) -> str:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Decimal value must be an integer")
    if not (1 <= n <= 3999):
        raise ValueError("Decimal value out of range (1–3999)")
    result = []
    for val, sym in _ROMAN_TABLE:
        while n >= val:
            result.append(sym)
            n -= val
    return "".join(result)

def roman_to_int(s: str) -> int:
    if not isinstance(s, str):
        raise TypeError("Roman numeral must be a string")
    if not s:
        raise ValueError("Empty Roman numeral")
    s = s.upper()
    if not _ROMAN_RE.fullmatch(s):
        raise ValueError("Invalid Roman numeral")
    i, total = 0, 0
    for val, sym in _ROMAN_TABLE:
        while s[i:i+len(sym)] == sym:
            total += val
            i += len(sym)
            if i >= len(s):
                return total
    raise ValueError("Invalid Roman numeral parsing")
