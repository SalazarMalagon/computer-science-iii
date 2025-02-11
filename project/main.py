from Lexcal import checker

def lexical_analysis(code: str):
    tokens = checker(code)
    # code = remove_comments(code)
    # code = remove_spaces(code)
    # code = remove_punctuation(code)
    return tokens


if __name__ == '__main__':
    code = """

ENTITY libro :
    codigo: PK, NON_NULL, INT, AUT
    autor: NON_PK, NON_NULL, CHAR, NON_AUT


RELATIONSHIP escribir :
    autor GO libro : ONE_TO_MANY

"""
    new_code = lexical_analysis(code)
    print(new_code)