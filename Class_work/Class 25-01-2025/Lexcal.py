import re

TOKEN_TYPES=[
    ('KEYWORD', r'\b[A-Z_]+\b'),
    ('IDENTIFIER', r'\b[a-z_]+\b'),
    ('SEPARATOR', r':|,'),
    ('WHITESPACE', r'\s'),
    ('COMENT', r'//')
    ]

tokens = []
position = 0
code="""
ENTITY libro :
    codigo: PK, NON_NULL, INT, AUT, NULL
    autor: NON_PK, NON_NULL, CHAR, NON_AUT
 """

while position < len(code):
    match = None
    for token_type, pattern in TOKEN_TYPES:
        regex  = re.compile(pattern)
        match = regex.match(code, position)
        if match:
            text = match.group(0)
            if token_type != 'WHITESPACE' and token_type != 'COMENT':
                tokens.append((token_type,text)) #token, lexeme
                print(tokens)
            position = match.end(0)
            break

    if not match:
        raise SyntaxError(f'Unexpected character: {code[position]}')