import re

# (i) Identifiers (variable and function names)
identifier_regex = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

# (ii) Integer literals
integer_literal_regex = r'^\d+$'

# (iii) Floating point literals
float_literal_regex = r'^\d+\.\d+$'

# (iv) String literals (in double quotes)
string_literal_regex = r'^".*?"$'

# (v) One-line comments (start with //)
single_line_comment_regex = r'^//.*$'

# (vi) Multi-line comments (between /* and */)
multi_line_comment_regex = r'/\*[\s\S]*?\*/'

# (vii) Whitespace (spaces, tabs, line breaks)
whitespace_regex = r'\s+'

# (viii) Common operators (+, -, *, /, ==, !=, etc.)
operators_regex = r'(\+|\-|\*|\/|==|!=)'

# (ix) Keywords (if, else, while, return)
keywords_regex = r'\b(if|else|while|return)\b'

# (x) Hexadecimal literals (example: 0x1A3F)
hex_literal_regex = r'^0x[0-9A-Fa-f]+$'

test_cases = [
    ("x", identifier_regex), 
    ("123", integer_literal_regex), 
    ("3.14", float_literal_regex), 
    ('"Hello, world!"', string_literal_regex), 
    ("// Esto es un comentario", single_line_comment_regex), 
    ("/* Comentario \n de varias líneas */", multi_line_comment_regex),  
    ("  \t\n", whitespace_regex),
    ("if", keywords_regex),
    ("0xFF", hex_literal_regex),
]

for text, pattern in test_cases:
    match = re.match(pattern, text)
    print(f"{text}: {'Coincide' if match else 'No coincide'}")
