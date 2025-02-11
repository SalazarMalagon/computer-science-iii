import re

class Token:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"

TOKEN_TYPES = [
    ('KEYWORD', r'\b(ENTITY|RELATIONSHIP|GO|ONE_TO_MANY)\b'),
    ('PROPERTY', r'\b(PK|NON_NULL|INT|AUT|NON_PK|CHAR|NON_AUT)\b'),
    ('IDENTIFIER', r'\b[a-z_]+\b'),
    ('SEPARATOR', r':|,'),
    ('TERMINATOR', r';'),
    ('COMMENT', r'//.*'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.')  # Caracter no reconocido
]


def checker (code: str):
    tokens = []
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_TYPES)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "MISMATCH":
            # throws an error if the character is not recognized
            raise RuntimeError(f"Unexpected character: {value}")
        if kind == "SKIP":
            # ignores spaces and tabs
            continue
        # if all validations are fine, just add as a new token
        tokens.append(Token(kind, value))

    return tokens

