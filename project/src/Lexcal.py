import re

# ==========================
# Token Class Definition
# ==========================
class Token:
    """Class representing a token identified during lexical analysis."""
    def __init__(self, type_, value, line, column):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type_}, {self.value}, Line: {self.line}, Column: {self.column})"

# ==========================
# Token Type Definitions
# ==========================
TOKEN_TYPES = [
    ('KEYWORD', r'\b(ENTITY|RELATIONSHIP|GO)\b'),  # Keywords
    ('CARDINALITY', r'\b(ONE_TO_ONE|ONE_TO_MANY|MANY_TO_MANY)\b'),  # Relationship cardinality
    ('PROPERTY', r'\b(PK|NON_PK|NON_NULL|NULL|INT|CHAR|AUT|NON_AUT)\b'),  # Entity properties
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identifiers
    ('TERMINATOR', r':'),  # Declaration terminator
    ('SEPARATOR', r','),  # Property separator
    ('SEMITERMINATOR', r';'),  # Expression terminator
    ('COMMENT', r'//.*'),  # Inline comments
    ('WHITESPACE', r'[ \t]+'),  # Whitespace
    ('NEWLINE', r'\n'),  # New lines
    ('MISMATCH', r'.')  # Unrecognized characters
]

# ==========================
# Lexical Analysis Function
# ==========================

def checker(code: str):
    """Function that analyzes the source code and returns a list of tokens."""
    tokens = []
    line_num = 1
    line_start = 0
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_TYPES)
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        
        if kind == "MISMATCH":
            # Report an error if an unexpected character is found
            raise RuntimeError(f"Lexical error: Unexpected character '{value}' at line {line_num}, column {column}")
        elif kind in ["COMMENT", "WHITESPACE", "NEWLINE"]:
            if kind == "NEWLINE":
                line_start = mo.end()
                line_num += 1
            continue  # Ignore comments, whitespace, and new lines
        
        # Add token to the list
        tokens.append(Token(kind, value, line_num, column))
    
    return tokens