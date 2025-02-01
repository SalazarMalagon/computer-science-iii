import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

TOKEN_TYPES=[
    ('KEYWORD', r'\b[A-Z_]+\b'),
    ('IDENTIFIER', r'\b[a-z_]+\b'),
    ('SEPARATOR', r':|,'),
    ('COMENT', r'//'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
    ]

def checker (code: str):
    tokens = []
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_TYPES)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        else:
            tokens.append(Token(kind, value))
    return tokens
