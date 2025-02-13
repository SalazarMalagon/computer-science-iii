import re

# Agregar manejo de comentarios y ajustar propiedades
class Token:
    def __init__(self, type_, value, line, column):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type_}, {self.value}, Línea: {self.line}, Columna: {self.column})"

TOKEN_TYPES = [
    ('KEYWORD', r'\b(ENTITY|RELATIONSHIP|GO)\b'),
    ('CARDINALITY', r'\b(ONE_TO_ONE|ONE_TO_MANY|MANY_TO_MANY)\b'),
    ('PROPERTY', r'\b(PK|NON_PK|NON_NULL|NULL|INT|CHAR|AUT|NON_AUT)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('TERMINATOR', r':'),
    ('SEPARATOR', r','),
    ('SEMITERMINATOR', r';'),
    ('COMMENT', r'//.*'),
    ('WHITESPACE', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('MISMATCH', r'.')
]

def checker(code: str):
    tokens = []
    line_num = 1
    line_start = 0
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_TYPES)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == "MISMATCH":
            raise RuntimeError(f"Error léxico: Carácter inesperado '{value}' en línea {line_num}, columna {column}")
        elif kind == "COMMENT" or kind == "WHITESPACE" or kind == "NEWLINE":
            if kind == "NEWLINE":
                line_start = mo.end()
                line_num += 1
            continue
        tokens.append(Token(kind, value, line_num, column))
    return tokens